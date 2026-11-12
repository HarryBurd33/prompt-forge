#!/usr/bin/env python3
"""Build/check the synchronized legacy alias, portable prompts and deterministic ZIP."""
import argparse
import hashlib
import io
import posixpath
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'prompt-forge'
ALIAS = ROOT / 'skills' / 'adaptive-prompt-builder'
VERSION = '0.4.0'
ARCHIVE = ROOT / 'dist' / ('prompt-forge-v' + VERSION + '.zip')
CHECKSUMS = ROOT / 'dist' / 'SHA256SUMS'
LEGACY_ARCHIVE = ROOT / 'dist' / 'adaptive-prompt-builder-v0.1.0.zip'
LEGACY_ARCHIVE_SHA256 = '2467a25967aca798aaa89c0581fe60951320131d9f046c752ac35460446ed043'
V020_ARCHIVE = ROOT / 'dist/prompt-forge-v0.2.0.zip'
V020_ARCHIVE_SHA256 = 'a6ff4d6a137b33292664c71b2e93093dfd20d42ce49018e871076502be6b25c3'
V030_ARCHIVE = ROOT / 'dist/prompt-forge-v0.3.0.zip'
V030_ARCHIVE_SHA256 = '362217c008ab0867e10068eed39c0b017ad337bb92e4bf05896a68a0ddd09de3'
LINKS = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
ALIAS_NOTE = ('> Legacy alias: Adaptive Prompt Builder is now Prompt Forge. '
              'This standalone compatibility copy contains the same instructions; '
              'install only one name to avoid duplicate discovery.\n\n')


def local_target(target):
    target = target.strip().strip('<>')
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith('#'):
        return None
    return unquote(parsed.path)


def sources(directory=None):
    directory = SKILL if directory is None else directory
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('Missing skill directory or symlink: ' + str(directory))
    entries = sorted(directory.rglob('*'))
    if any(p.is_symlink() for p in entries):
        raise ValueError('Skill source must not contain symlinks')
    paths = [p for p in entries if p.is_file()]
    for p in paths:
        if p.suffix == '.md':
            for target in LINKS.findall(p.read_text(encoding='utf-8')):
                relative = local_target(target)
                if relative is None:
                    continue
                resolved = (p.parent / relative).resolve()
                try:
                    resolved.relative_to(directory.resolve())
                except ValueError:
                    raise ValueError('Escaping skill link: ' + str(p) + ': ' + target)
                if not resolved.is_file():
                    raise ValueError('Broken skill link: ' + str(p) + ': ' + target)
    return paths


def canonical_files():
    files = {p.relative_to(SKILL).as_posix(): p.read_bytes() for p in sources()}
    primary = files.get('SKILL.md', b'').decode('utf-8')
    parts = primary.split('---', 2)
    if not primary.startswith('---\n') or len(parts) != 3:
        raise ValueError('Unexpected canonical skill metadata')
    if not re.search(r'^name: prompt-forge\s*$', parts[1], re.M):
        raise ValueError('Unexpected canonical skill name')
    version = re.search(r'^  version: [\"\']?([^\s\"\']+)[\"\']?\s*$', parts[1], re.M)
    if not version or version.group(1) != VERSION:
        raise ValueError('Canonical metadata version must equal package version ' + VERSION)
    if 'LICENSE' not in files:
        raise ValueError('Canonical skill requires LICENSE')
    return files


def alias_files(files=None):
    files = canonical_files() if files is None else files
    result = dict(files)
    text = files['SKILL.md'].decode('utf-8')
    text = text.replace('name: prompt-forge\n', 'name: adaptive-prompt-builder\n', 1)
    text, count = re.subn(r'^# [^\n]+\n', '# Adaptive Prompt Builder (legacy alias)\n\n' + ALIAS_NOTE,
                          text, count=1, flags=re.M)
    if count != 1:
        raise ValueError('Canonical skill requires a top-level title')
    result['SKILL.md'] = text.encode('utf-8')
    return result


def portable_text(files):
    text = files['SKILL.md'].decode('utf-8').split('---', 2)[2].lstrip()
    sections = []
    included = set()

    def inline(match, parent=PurePosixPath('.')):
        target = local_target(match.group(1))
        if target is None:
            return match.group(0)
        target = posixpath.normpath(str(parent / target))
        if target not in files:
            raise ValueError('Unsupported portable link: ' + target)
        if target not in included:
            included.add(target)
            body = files[target].decode('utf-8').strip()
            body = LINKS.sub(lambda nested: inline(nested, PurePosixPath(target).parent), body)
            sections.append(body)
        label = match.group(0).split('](', 1)[0][1:]
        return label + ' (included in this prompt)'

    text = LINKS.sub(inline, text)
    return ('<!-- Generated from the canonical skill by scripts/package.py. -->\n'
            'Use these instructions to refine my idea into a standalone prompt.\n\n'
            + text.rstrip() + '\n\n'
            + '\n\n'.join('---\n\n' + body for body in sections)
            + '\n\n---\n\n## License\n\n' + files['LICENSE'].decode('utf-8').strip() + '\n')


def archive_bytes(files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            parts = PurePosixPath(name)
            if parts.is_absolute() or '..' in parts.parts or '\\' in name:
                raise ValueError('Unsafe archive path: ' + name)
            info = zipfile.ZipInfo('prompt-forge/' + name, date_time=(2026, 10, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    data = output.getvalue()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if z.testzip() is not None or len(z.namelist()) != len(files):
            raise ValueError('Archive integrity failure')
        for name in z.namelist():
            if z.read(name) != files[name[len('prompt-forge/'):]]:
                raise ValueError('Archive content mismatch: ' + name)
    return data


def expected_outputs():
    files = canonical_files()
    alias = alias_files(files)
    if not LEGACY_ARCHIVE.is_file() or hashlib.sha256(LEGACY_ARCHIVE.read_bytes()).hexdigest() != LEGACY_ARCHIVE_SHA256:
        raise ValueError('Frozen v0.1.0 archive is missing or changed')
    if not V020_ARCHIVE.is_file() or hashlib.sha256(V020_ARCHIVE.read_bytes()).hexdigest() != V020_ARCHIVE_SHA256:
        raise ValueError('Frozen v0.2.0 archive is missing or changed')
    if not V030_ARCHIVE.is_file() or hashlib.sha256(V030_ARCHIVE.read_bytes()).hexdigest() != V030_ARCHIVE_SHA256:
        raise ValueError('Frozen v0.3.0 archive is missing or changed')
    outputs = {ALIAS / name: data for name, data in alias.items()}
    generated = {
        ROOT / 'portable/prompt-forge.md': portable_text(files).encode('utf-8'),
        ROOT / 'portable/adaptive-prompt-builder.md': portable_text(alias).encode('utf-8'),
        ARCHIVE: archive_bytes(files),
    }
    checksum = ''
    for historical in sorted(CHECKSUMS.parent.glob('*.zip')):
        if historical != ARCHIVE:
            checksum += hashlib.sha256(historical.read_bytes()).hexdigest() + '  ' + historical.name + '\n'
    for path, data in sorted(generated.items()):
        name = path.name if path.parent == CHECKSUMS.parent else '../portable/' + path.name
        checksum += hashlib.sha256(data).hexdigest() + '  ' + name + '\n'
    outputs.update(generated)
    outputs[CHECKSUMS] = checksum.encode('utf-8')
    extras = [p for p in ALIAS.rglob('*') if p.is_file() and p not in outputs]
    if ALIAS.is_symlink() or any(p.is_symlink() for p in ALIAS.rglob('*')) or extras:
        raise ValueError('Unexpected files or symlinks in generated alias; inspect before rebuilding')
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check without rewriting generated files')
    args = parser.parse_args()
    expected = expected_outputs()
    if args.check:
        drift = [str(p.relative_to(ROOT)) for p, data in expected.items()
                 if not p.is_file() or p.read_bytes() != data]
        if drift:
            raise ValueError('Generated file drift: ' + ', '.join(drift))
        sources(ALIAS)
    else:
        for path, data in expected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print(('Checked' if args.check else 'Built') + ': Prompt Forge ' + VERSION + ', legacy alias, portable prompts, ZIP, SHA256SUMS')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, IndexError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
