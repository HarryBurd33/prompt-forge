#!/usr/bin/env python3
"""Install Prompt Forge; optionally migrate a recognized, unmodified legacy copy."""
import argparse
import hashlib
import sys
import tempfile
from pathlib import Path

import package

# Captured from committed v0.1.0 before generating the compatibility alias.
LEGACY_V010 = {
    'LICENSE': '8e51a3d1476cb7497704932e1511fc78c46c12ee900a121907ec178321cf7d28',
    'SKILL.md': '15ad0aa8713027f6ba8d0f3c78c0c2630b4b857375db0d9e4056f3599eb78f71',
    'references/artifact-contracts.md': '49bc2b8a352d75cb4cf4216d7d661b469bb8caf234142b7ee16304b66c311b76',
    'references/skill-forge-handoff.md': '933e13c91922d392a33c04f29a1ed030de18b0353215ee358b104a44908a2038',
    'templates/brief.md': '5aec6b992f94dced5920e766583553c4e612c26ba3fd26917ddb23533b9dfce8',
}


def byte_hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}


def installed_hashes(directory):
    if directory.is_symlink() or not directory.is_dir():
        return None
    entries = list(directory.rglob('*'))
    if any(p.is_symlink() or (not p.is_file() and not p.is_dir()) for p in entries):
        return None
    return {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in entries if p.is_file()}


def present(path):
    return path.exists() or path.is_symlink()


def refuse(path):
    raise ValueError('Refusing to overwrite customized or unrecognized files at ' + str(path)
                     + '. Make a manual merge into a separate copy of Prompt Forge, '
                     'then move the customized installation outside the skills root before retrying. '
                     'All existing files were preserved.')


def install(root, migrate=False):
    # Validate the repository before inspecting or changing the installation.
    files = package.canonical_files()
    alias_hashes = byte_hashes(package.alias_files(files))
    canonical_hashes = byte_hashes(files)
    root = root.expanduser().absolute()
    if root.is_symlink():
        raise ValueError('Skills root must not be a symlink: ' + str(root))
    if root.exists() and not root.is_dir():
        raise ValueError('Skills root must be a directory: ' + str(root))
    canonical = root / 'prompt-forge'
    legacy = root / 'adaptive-prompt-builder'
    canonical_present = present(canonical)
    legacy_present = present(legacy)
    if canonical_present and installed_hashes(canonical) != canonical_hashes:
        refuse(canonical)
    if legacy_present:
        if installed_hashes(legacy) not in (LEGACY_V010, alias_hashes):
            refuse(legacy)
        if not migrate:
            raise ValueError('A recognized legacy installation exists. Run again with --migrate '
                             'to back it up and replace discovery with Prompt Forge.')
    if canonical_present and not legacy_present:
        print('Already installed, unchanged: ' + str(canonical))
        return

    # Prepare a complete copy before any existing directory is moved.
    root.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix='.prompt-forge-stage-', dir=str(root.parent)) as stage:
        staged = Path(stage) / 'prompt-forge'
        staged.mkdir()
        for name, data in files.items():
            path = staged / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if installed_hashes(staged) != canonical_hashes:
            raise ValueError('Staged installation failed verification')
        if legacy_present:
            backups = root.parent / '.prompt-forge-backups'
            if backups.is_symlink() or (backups.exists() and not backups.is_dir()):
                raise ValueError('Backup location must be a real directory: ' + str(backups))
            backups.mkdir(exist_ok=True)
            index = 1
            backup = backups / ('adaptive-prompt-builder-' + str(index))
            while present(backup):
                index += 1
                backup = backups / ('adaptive-prompt-builder-' + str(index))
            legacy.rename(backup)
        try:
            if not canonical_present:
                staged.rename(canonical)
        except OSError:
            if backup is not None:
                backup.rename(legacy)
            raise
    print('Installed: ' + str(canonical))
    if backup is not None:
        print('Legacy backup outside skill discovery: ' + str(backup))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.home() / '.agents' / 'skills',
                        help='Skills discovery directory (default: ~/.agents/skills)')
    parser.add_argument('--migrate', action='store_true',
                        help='Back up a recognized unchanged legacy installation outside discovery')
    args = parser.parse_args()
    install(args.root, args.migrate)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
