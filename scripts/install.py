#!/usr/bin/env python3
"""Install Prompt Forge; optionally migrate a recognized, unmodified legacy copy."""
import argparse
import hashlib
import json
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


# Exact canonical v0.2.0 manifest; unknown additions or customizations refuse upgrade.
CANONICAL_V020 = {'LICENSE': '8e51a3d1476cb7497704932e1511fc78c46c12ee900a121907ec178321cf7d28', 'SKILL.md': '567dea1703a23a650327930106ab2e5aec4e65d684da9fe85998fc14bf44d006', 'references/skill-forge-handoff.md': '933e13c91922d392a33c04f29a1ed030de18b0353215ee358b104a44908a2038', 'references/artifact-contracts.md': '49bc2b8a352d75cb4cf4216d7d661b469bb8caf234142b7ee16304b66c311b76', 'templates/brief.md': '5aec6b992f94dced5920e766583553c4e612c26ba3fd26917ddb23533b9dfce8'}

# Generated standalone v0.2.0 alias remains a recognized migration source.
ALIAS_V020 = {'LICENSE': '8e51a3d1476cb7497704932e1511fc78c46c12ee900a121907ec178321cf7d28',
 'SKILL.md': '3ee45d77d192aabc67c91374b62480c75fec488125f10fc23b917fdcfef3c589',
 'references/artifact-contracts.md': '49bc2b8a352d75cb4cf4216d7d661b469bb8caf234142b7ee16304b66c311b76',
 'references/skill-forge-handoff.md': '933e13c91922d392a33c04f29a1ed030de18b0353215ee358b104a44908a2038',
 'templates/brief.md': '5aec6b992f94dced5920e766583553c4e612c26ba3fd26917ddb23533b9dfce8'}

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


def install(root, migrate=False, upgrade=False):
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
    previous = installed_hashes(canonical) if canonical_present else None
    needs_upgrade = canonical_present and previous != canonical_hashes
    if needs_upgrade:
        if previous != CANONICAL_V020:
            refuse(canonical)
        if not upgrade:
            raise ValueError('Recognized v0.2.0 installation: rerun with --upgrade for a verified backup and upgrade')
    if legacy_present:
        if installed_hashes(legacy) not in (LEGACY_V010, ALIAS_V020, alias_hashes):
            refuse(legacy)
        if not migrate:
            raise ValueError('A recognized legacy installation exists. Run again with --migrate '
                             'to back it up and replace discovery with Prompt Forge.')
    if canonical_present and not legacy_present and not needs_upgrade:
        print('Already installed, unchanged: ' + str(canonical))
        return

    # Prepare a complete copy before any existing directory is moved.
    root.mkdir(parents=True, exist_ok=True)
    backup = None
    upgrade_backup = None
    with tempfile.TemporaryDirectory(prefix='.prompt-forge-stage-', dir=str(root.parent)) as stage:
        staged = Path(stage) / 'prompt-forge'
        staged.mkdir()
        for name, data in files.items():
            path = staged / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if installed_hashes(staged) != canonical_hashes:
            raise ValueError('Staged installation failed verification')
        if legacy_present or needs_upgrade:
            backups = root.parent / '.prompt-forge-backups'
            if backups.is_symlink() or (backups.exists() and not backups.is_dir()):
                raise ValueError('Backup location must be a real directory: ' + str(backups))
            backups.mkdir(mode=0o700, exist_ok=True)
        try:
            if needs_upgrade:
                upgrade_backup = next_backup(backups, 'prompt-forge-v0.2.0')
                record = {'root': str(root), 'before': previous, 'after': canonical_hashes}
                record_path = Path(str(upgrade_backup) + '.json')
                with record_path.open('x') as stream:
                    stream.write(json.dumps(record, indent=2) + '\n')
                record_path.chmod(0o600)
                canonical.rename(upgrade_backup)
            if legacy_present:
                backup = next_backup(backups, 'adaptive-prompt-builder')
                legacy.rename(backup)
            if not canonical_present or needs_upgrade:
                staged.rename(canonical)
        except OSError:
            if upgrade_backup is not None and upgrade_backup.is_dir() and not present(canonical):
                upgrade_backup.rename(canonical)
            if upgrade_backup is not None and not present(upgrade_backup):
                Path(str(upgrade_backup) + '.json').unlink(missing_ok=True)
            if backup is not None and backup.is_dir() and not present(legacy):
                backup.rename(legacy)
            raise
    print('Installed: ' + str(canonical))
    if upgrade_backup is not None:
        print('Upgrade backup outside discovery: ' + str(upgrade_backup))
    if backup is not None:
        print('Legacy backup outside skill discovery: ' + str(backup))


def next_backup(backups, name):
    index = 1
    result = backups / (name + '-' + str(index))
    while present(result) or present(Path(str(result) + '.json')):
        index += 1
        result = backups / (name + '-' + str(index))
    return result


def rollback(root, backup):
    root = root.expanduser().absolute()
    backup = backup.expanduser().absolute()
    if root.is_symlink() or backup.is_symlink() or backup.parent.is_symlink() or backup.parent != root.parent / '.prompt-forge-backups':
        raise ValueError('Rollback requires an owned backup outside this skills root')
    record_path = Path(str(backup) + '.json')
    if record_path.is_symlink():
        raise ValueError('Rollback record must not be a symlink')
    record = json.loads(record_path.read_text())
    canonical = root / 'prompt-forge'
    if record.get('root') != str(root) or record.get('before') != CANONICAL_V020:
        raise ValueError('Rollback backup ownership or version mismatch')
    if installed_hashes(backup) != record['before'] or installed_hashes(canonical) != record.get('after'):
        raise ValueError('Rollback refuses changed installation or backup; preserve and merge customizations')
    if present(root / 'adaptive-prompt-builder'):
        raise ValueError('Rollback refuses competing alias')
    displaced = next_backup(backup.parent, 'prompt-forge-v0.3.0-rollback')
    canonical.rename(displaced)
    try:
        backup.rename(canonical)
    except OSError:
        displaced.rename(canonical)
        raise
    record_path.unlink()
    print('Restored v0.2.0: ' + str(canonical))
    print('Displaced installation outside discovery: ' + str(displaced))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.home() / '.agents' / 'skills',
                        help='Skills discovery directory (default: ~/.agents/skills)')
    parser.add_argument('--migrate', action='store_true',
                        help='Back up a recognized unchanged legacy installation outside discovery')
    parser.add_argument('--upgrade', action='store_true', help='Upgrade only exact recognized v0.2.0, with backup')
    parser.add_argument('--rollback', type=Path, help='Restore the exact owned upgrade backup; refuses later edits')
    args = parser.parse_args()
    if args.rollback:
        if args.migrate or args.upgrade:
            parser.error('--rollback cannot be combined with --migrate or --upgrade')
        rollback(args.root, args.rollback)
    else:
        install(args.root, args.migrate, args.upgrade)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
