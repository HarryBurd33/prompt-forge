#!/usr/bin/env python3
"""Manage only Prompt Forge's exact owned Codex recommendation block (Python 3.9+)."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

TEMPLATE = Path(__file__).resolve().parents[1] / 'skills/prompt-forge/resources/recommendation-rule.md'
BEGIN = b'<!-- BEGIN prompt-forge managed recommendation v1 -->'
END = b'<!-- END prompt-forge managed recommendation v1 -->'
MARKER = b'prompt-forge managed recommendation'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('Refusing symlink path: ' + str(part))
    if path.exists() and not path.is_file():
        raise ValueError('Expected regular file: ' + str(path))


def read(path):
    safe(path)
    return path.read_bytes() if path.exists() else b''


def atomic(path, data):
    safe(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, name = tempfile.mkstemp(prefix='.prompt-forge-rule-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def target_for(home):
    # Codex global instruction precedence: nonempty AGENTS.override.md wins.
    override = home / 'AGENTS.override.md'
    fallback = home / 'AGENTS.md'
    return override if read(override).strip() else fallback


def block_bounds(data):
    if MARKER not in data:
        return None
    if data.count(MARKER) != 2 or data.count(BEGIN) != 1 or data.count(END) != 1:
        raise ValueError('Duplicate or malformed Prompt Forge block; preserved unchanged')
    start = data.index(BEGIN)
    end = data.index(END) + len(END)
    if end < start:
        raise ValueError('Malformed Prompt Forge block; preserved unchanged')
    if end < len(data) and data[end:end + 1] == b'\n':
        end += 1
    return start, end


def save_state(path, record):
    atomic(path, (json.dumps(record, indent=2) + '\n').encode())


def recover_pending(state_path, state, target, data):
    if state.get('phase') != 'pending':
        return state
    if state.get('target') != str(target):
        raise ValueError('Pending rule target precedence changed; inspect preserved receipt')
    current = digest(data)
    if current == state['pending_after_sha256']:
        final = state.get('final')
        if final is None:
            state_path.unlink()
        else:
            save_state(state_path, final)
        return final
    if current == state['pending_before_sha256']:
        prior = state.get('prior')
        if prior is None:
            state_path.unlink()
        else:
            save_state(state_path, prior)
        return prior
    raise ValueError('Uncertain interrupted rule update; preserved receipt and concurrent instructions for inspection')


def mutate_with_receipt(state_path, target, before, after, prior, final):
    # Save rollback evidence before any instruction mutation. A failed final receipt
    # leaves this pending record, whose hashes permit a bounded recovery next call.
    pending = {'schema': 1, 'phase': 'pending', 'target': str(target),
               'pending_before_sha256': digest(before), 'pending_after_sha256': digest(after),
               'before_bytes': base64.b64encode(before).decode(), 'prior': prior, 'final': final}
    save_state(state_path, pending)
    if read(target) != before:
        raise ValueError('Instructions changed concurrently; preserved pending receipt, no overwrite')
    if after != before:
        atomic(target, after)
    if final is None:
        state_path.unlink()
    else:
        save_state(state_path, final)


def manage(home, skill, remove=False):
    home = home.expanduser().absolute()
    if home.is_symlink():
        raise ValueError('Codex home must not be a symlink')
    # Normalize platform ancestors such as macOS /var -> /private/var before checks.
    home = home.resolve()
    state_path = home / '.prompt-forge-recommendation-state.json'
    state_bytes = read(state_path)
    state = json.loads(state_bytes) if state_bytes else None
    target = target_for(home)
    if state is not None:
        state = recover_pending(state_path, state, target, read(target))
    if state is not None and state.get('target') != str(target):
        raise ValueError('Global instruction precedence changed; reconcile owned rule before retrying')
    data = read(target)
    bounds = block_bounds(data)
    if state is not None:
        owned = base64.b64decode(state['block'], validate=True)
        if not bounds or data[bounds[0]:bounds[1]] != owned:
            raise ValueError('Owned block changed or missing; preserving customization')
    elif bounds:
        raise ValueError('Existing block has no ownership record; preserve and reconcile manually')
    if remove:
        if state is None:
            print('No owned recommendation rule to remove')
            return
        start, end = bounds
        # Remove our separating newline only when still adjacent and owned.
        separator = base64.b64decode(state['separator'], validate=True)
        if separator and data[max(0, start-len(separator)):start] == separator:
            start -= len(separator)
        output = data[:start] + data[end:]
        mutate_with_receipt(state_path, target, data, output, state, None)
        print('Removed unchanged owned rule: ' + str(target))
        return
    skill = skill.expanduser().absolute()
    if '\n' in str(skill) or '\r' in str(skill) or '{{' in str(skill):
        raise ValueError('Invalid skill path')
    if not (skill / 'SKILL.md').is_file():
        raise ValueError('Expected installed skill directory with SKILL.md')
    block = TEMPLATE.read_bytes().replace(b'{{SKILL_PATH}}', str(skill / 'SKILL.md').encode())
    separator = b'' if not data else (b'\n' if data.endswith(b'\n') else b'\n\n')
    if state is not None:
        start, end = bounds
        output = data[:start] + block + data[end:]
        separator = base64.b64decode(state['separator'], validate=True)
        original = state['original']
        original_hash = state['pre_sha256']
    else:
        output = data + separator + block
        original = base64.b64encode(data).decode()
        original_hash = digest(data)
    record = {'schema': 1, 'target': str(target), 'block': base64.b64encode(block).decode(),
              'separator': base64.b64encode(separator).decode(), 'original': original,
              'pre_sha256': original_hash, 'post_sha256': digest(output)}
    if output != data or state != record:
        mutate_with_receipt(state_path, target, data, output, state, record)
    print('Managed recommendation rule: ' + str(target))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['install', 'remove'])
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
    parser.add_argument('--skill-path', type=Path, default=Path.home() / '.codex/skills/prompt-forge')
    args = parser.parse_args()
    manage(args.codex_home, args.skill_path, args.action == 'remove')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
