"""Upgrade and recommendation ownership checks in disposable host directories."""
import hashlib
import importlib.util
from unittest.mock import patch
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

REPO = Path(__file__).resolve().parents[1]


def tree(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file()}


class UpgradeRuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'codex/skills'
        self.home = self.base / 'codex'
        self.skill = self.root / 'prompt-forge'

    def command(self, script, *args, ok=True):
        result = subprocess.run([sys.executable, str(REPO / 'scripts' / script), *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def install(self, *args, ok=True):
        return self.command('install.py', '--root', self.root, *args, ok=ok)

    def rule(self, action='install', ok=True):
        return self.command('recommendation_rule.py', action, '--codex-home', self.home,
                            '--skill-path', self.skill, ok=ok)

    def old(self):
        self.root.mkdir(parents=True)
        with zipfile.ZipFile(REPO / 'dist/prompt-forge-v0.2.0.zip') as z:
            z.extractall(self.root)

    def test_explicit_upgrade_backup_and_rollback(self):
        self.old()
        before = tree(self.skill)
        self.install(ok=False)
        self.assertEqual(tree(self.skill), before)
        self.install('--upgrade')
        self.assertEqual(tree(self.skill), tree(REPO / 'skills/prompt-forge'))
        backups = self.home / '.prompt-forge-backups'
        backup = next(p for p in backups.iterdir() if p.is_dir())
        self.assertEqual(tree(backup), before)
        self.assertEqual([p.name for p in self.root.iterdir()], ['prompt-forge'])
        self.install('--rollback', backup)
        self.assertEqual(tree(self.skill), before)
        self.install('--rollback', backup, ok=False)

    def test_v030_upgrade_preserves_backup_and_round_trips(self):
        self.root.mkdir(parents=True)
        with zipfile.ZipFile(REPO / 'dist/prompt-forge-v0.3.0.zip') as z:
            z.extractall(self.root)
        before = tree(self.skill)
        self.install(ok=False)
        self.assertEqual(tree(self.skill), before)
        self.install('--upgrade')
        self.assertEqual(tree(self.skill), tree(REPO / 'skills/prompt-forge'))
        backup = next(p for p in (self.home / '.prompt-forge-backups').iterdir() if p.is_dir())
        self.assertTrue(backup.name.startswith('prompt-forge-v0.3.0-'))
        self.assertEqual(tree(backup), before)
        self.install('--upgrade')
        self.assertEqual(len(list((self.home / '.prompt-forge-backups').glob('*.json'))), 1)
        self.install('--rollback', backup)
        self.assertEqual(tree(self.skill), before)

    def test_v030_customization_and_changed_rollback_refused(self):
        self.root.mkdir(parents=True)
        with zipfile.ZipFile(REPO / 'dist/prompt-forge-v0.3.0.zip') as z:
            z.extractall(self.root)
        primary = self.skill / 'SKILL.md'
        original = primary.read_bytes()
        primary.write_bytes(original + b'\nLocal customization\n')
        before = tree(self.skill)
        self.install('--upgrade', ok=False)
        self.assertEqual(tree(self.skill), before)
        primary.write_bytes(original)
        self.install('--upgrade')
        backup = next(p for p in (self.home / '.prompt-forge-backups').iterdir() if p.is_dir())
        primary.write_bytes(primary.read_bytes() + b'\nLater customization\n')
        before = tree(self.skill)
        self.install('--rollback', backup, ok=False)
        self.assertEqual(tree(self.skill), before)

    def test_known_v020_alias_migration_and_customization_refusal(self):
        alias = self.root / 'adaptive-prompt-builder'
        self.root.mkdir(parents=True)
        with zipfile.ZipFile(REPO / 'dist/prompt-forge-v0.2.0.zip') as z:
            z.extractall(self.root)
        self.skill.rename(alias)
        primary = alias / 'SKILL.md'
        text = primary.read_text().replace('name: prompt-forge\n', 'name: adaptive-prompt-builder\n', 1)
        note = ('> Legacy alias: Adaptive Prompt Builder is now Prompt Forge. '
                'This standalone compatibility copy contains the same instructions; '
                'install only one name to avoid duplicate discovery.\n\n')
        text = text.replace('# Prompt Forge\n', '# Adaptive Prompt Builder (legacy alias)\n\n' + note, 1)
        primary.write_text(text)
        before = tree(alias)
        primary.write_text(text + 'customization')
        self.install('--migrate', ok=False)
        self.assertEqual(primary.read_text(), text + 'customization')
        primary.write_text(text)
        self.install('--migrate')
        self.assertFalse(alias.exists())
        self.assertEqual(tree(self.skill), tree(REPO / 'skills/prompt-forge'))
        backup = next(p for p in (self.home / '.prompt-forge-backups').iterdir() if p.is_dir())
        self.assertEqual(tree(backup), before)

    def test_customized_old_extra_file_and_changed_rollback_refuse(self):
        self.old()
        (self.skill / 'SKILL.md').write_text('custom')
        before = tree(self.skill)
        self.install('--upgrade', ok=False)
        self.assertEqual(tree(self.skill), before)
        shutil.rmtree(self.skill)
        with zipfile.ZipFile(REPO / 'dist/prompt-forge-v0.2.0.zip') as z:
            z.extractall(self.root)
        (self.skill / 'extra').write_text('keep')
        self.install('--upgrade', ok=False)
        (self.skill / 'extra').unlink()
        self.install('--upgrade')
        backup = next(p for p in (self.home / '.prompt-forge-backups').iterdir() if p.is_dir())
        (self.skill / 'extra').write_text('later edit')
        before = tree(self.skill)
        self.install('--rollback', backup, ok=False)
        self.assertEqual(tree(self.skill), before)

    def test_rule_idempotent_and_remove_preserves_unrelated_bytes(self):
        self.install()
        target = self.home / 'AGENTS.md'
        original = b'# Mine\r\nExisting\x00 bytes without final newline'
        target.write_bytes(original)
        self.rule()
        first = target.read_bytes()
        self.rule()
        self.assertEqual(first, target.read_bytes())
        self.assertIn(str(self.skill / 'SKILL.md').encode(), first)
        self.assertNotIn(b'{{SKILL_PATH}}', first)
        state = json.loads((self.home / '.prompt-forge-recommendation-state.json').read_text())
        self.assertEqual(state['pre_sha256'], hashlib.sha256(original).hexdigest())
        target.write_bytes(first + b'\nLater unrelated instructions\n')
        self.rule('remove')
        self.assertEqual(target.read_bytes(), original + b'\nLater unrelated instructions\n')
        self.rule('remove')

    def test_override_precedence_empty_override_and_precedence_change(self):
        self.install()
        fallback = self.home / 'AGENTS.md'
        override = self.home / 'AGENTS.override.md'
        fallback.write_text('fallback unchanged')
        override.write_text('override instructions\n')
        self.rule()
        self.assertEqual(fallback.read_text(), 'fallback unchanged')
        self.assertIn('managed recommendation', override.read_text())
        override.unlink()
        before = fallback.read_bytes()
        self.rule(ok=False)
        self.assertEqual(fallback.read_bytes(), before)

    def test_empty_override_uses_fallback(self):
        self.install()
        (self.home / 'AGENTS.override.md').write_text('')
        self.rule()
        self.assertIn('managed recommendation', (self.home / 'AGENTS.md').read_text())
        self.assertEqual((self.home / 'AGENTS.override.md').read_bytes(), b'')

    def test_duplicate_malformed_customized_and_unowned_refused(self):
        self.install()
        target = self.home / 'AGENTS.md'
        template = (REPO / 'skills/prompt-forge/resources/recommendation-rule.md').read_bytes()
        for raw in (template, template + template, template.split(b'<!-- END')[0]):
            target.write_bytes(raw)
            self.rule(ok=False)
            self.assertEqual(target.read_bytes(), raw)
        target.unlink()
        self.rule()
        target.write_bytes(target.read_bytes().replace(b'Name that uncertainty', b'Edited wording'))
        before = target.read_bytes()
        self.rule(ok=False)
        self.rule('remove', ok=False)
        self.assertEqual(target.read_bytes(), before)

    def load_helper(self, name):
        sys.path.insert(0, str(REPO / 'scripts'))
        self.addCleanup(lambda: sys.path.remove(str(REPO / 'scripts')))
        spec = importlib.util.spec_from_file_location(name, REPO / 'scripts' / (name + '.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_failed_second_directory_move_restores_upgrade(self):
        self.old()
        shutil.copytree(REPO / 'skills/adaptive-prompt-builder', self.root / 'adaptive-prompt-builder')
        before = tree(self.root)
        helper = self.load_helper('install')
        original = Path.rename

        def fail_legacy(path, target):
            if path.name == 'adaptive-prompt-builder':
                raise OSError('injected legacy rename failure')
            return original(path, target)

        with patch.object(Path, 'rename', fail_legacy):
            with self.assertRaises(OSError):
                helper.install(self.root, migrate=True, upgrade=True)
        self.assertEqual(tree(self.root), before)
        backups = self.home / '.prompt-forge-backups'
        self.assertEqual(list(backups.iterdir()), [])

    def test_failed_stage_rename_restores_upgrade(self):
        self.old()
        before = tree(self.root)
        helper = self.load_helper('install')
        original = Path.rename

        def fail_stage(path, target):
            if path.parent.name.startswith('.prompt-forge-stage-'):
                raise OSError('injected stage rename failure')
            return original(path, target)

        with patch.object(Path, 'rename', fail_stage):
            with self.assertRaises(OSError):
                helper.install(self.root, upgrade=True)
        self.assertEqual(tree(self.root), before)

    def test_rule_receipt_failures_preserve_or_recover(self):
        self.install()
        helper = self.load_helper('recommendation_rule')
        target = self.home / 'AGENTS.md'
        state = self.home / '.prompt-forge-recommendation-state.json'
        for failure_at in (1, 2, 3):
            with self.subTest(failure_at=failure_at):
                target.write_bytes(b'original instructions')
                state.unlink(missing_ok=True)
                real_atomic = helper.atomic
                calls = [0]

                def fail_write(path, data):
                    calls[0] += 1
                    if calls[0] == failure_at:
                        raise OSError('injected write failure')
                    real_atomic(path, data)

                with patch.object(helper, 'atomic', fail_write):
                    with self.assertRaises(OSError):
                        helper.manage(self.home, self.skill)
                if failure_at == 1:
                    self.assertEqual(target.read_bytes(), b'original instructions')
                    self.assertFalse(state.exists())
                else:
                    self.assertEqual(json.loads(state.read_text())['phase'], 'pending')
                helper.manage(self.home, self.skill)
                self.assertNotEqual(json.loads(state.read_text()).get('phase'), 'pending')
                helper.manage(self.home, self.skill, remove=True)
                self.assertEqual(target.read_bytes(), b'original instructions')

    def test_pending_unknown_concurrent_change_refused(self):
        self.install()
        helper = self.load_helper('recommendation_rule')
        target = self.home / 'AGENTS.md'
        target.write_bytes(b'original')
        real_atomic = helper.atomic
        calls = [0]

        def fail_final(path, data):
            calls[0] += 1
            if calls[0] == 3:
                raise OSError('injected final receipt failure')
            real_atomic(path, data)

        with patch.object(helper, 'atomic', fail_final):
            with self.assertRaises(OSError):
                helper.manage(self.home, self.skill)
        target.write_bytes(target.read_bytes() + b'new unrelated concurrent instructions')
        before = target.read_bytes()
        with self.assertRaises(ValueError):
            helper.manage(self.home, self.skill)
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual(json.loads((self.home / '.prompt-forge-recommendation-state.json').read_text())['phase'], 'pending')

    def test_symlinks_refused(self):
        self.install()
        outside = self.base / 'outside'
        outside.write_text('preserve')
        (self.home / 'AGENTS.md').symlink_to(outside)
        self.rule(ok=False)
        self.assertEqual(outside.read_text(), 'preserve')
        (self.home / 'AGENTS.md').unlink()
        (self.home / '.prompt-forge-recommendation-state.json').symlink_to(outside)
        self.rule(ok=False)
        self.assertEqual(outside.read_text(), 'preserve')


if __name__ == '__main__':
    unittest.main()
