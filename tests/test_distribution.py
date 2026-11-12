"""Distribution checks use disposable copies and never touch personal skills."""
import hashlib
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def hashes(directory):
    return {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob('*') if p.is_file()}


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repository'
        shutil.copytree(REPO, self.repo, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        self.root = self.base / 'personal' / 'skills'

    def command(self, script, *args, success=True):
        result = subprocess.run([sys.executable, str(self.repo / 'scripts' / script), *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def install(self, *args, success=True):
        return self.command('install.py', '--root', self.root, *args, success=success)

    def test_clean_install_and_repeat(self):
        self.install()
        self.assertEqual(hashes(self.root / 'prompt-forge'), hashes(self.repo / 'skills/prompt-forge'))
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['prompt-forge'])
        before = hashes(self.root)
        self.install()
        self.assertEqual(before, hashes(self.root))
        self.assertFalse((self.root.parent / '.prompt-forge-backups').exists())

    def test_known_old_migration(self):
        self.root.mkdir(parents=True)
        with zipfile.ZipFile(self.repo / 'dist/adaptive-prompt-builder-v0.1.0.zip') as archive:
            archive.extractall(self.root)
        old = hashes(self.root / 'adaptive-prompt-builder')
        self.install('--migrate')
        self.assertFalse((self.root / 'adaptive-prompt-builder').exists())
        backups = list((self.root.parent / '.prompt-forge-backups').iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(old, hashes(backups[0]))
        self.assertEqual(hashes(self.root / 'prompt-forge'), hashes(self.repo / 'skills/prompt-forge'))
        self.install('--migrate')
        self.assertEqual(len(list((self.root.parent / '.prompt-forge-backups').iterdir())), 1)

    def test_current_alias_migration(self):
        shutil.copytree(self.repo / 'skills/adaptive-prompt-builder', self.root / 'adaptive-prompt-builder')
        before = hashes(self.root)
        self.install(success=False)
        self.assertEqual(before, hashes(self.root))
        self.install('--migrate')
        self.assertFalse((self.root / 'adaptive-prompt-builder').exists())
        self.assertEqual(hashes(self.root / 'prompt-forge'), hashes(self.repo / 'skills/prompt-forge'))

    def test_custom_legacy_refused_without_mutation(self):
        shutil.copytree(self.repo / 'skills/adaptive-prompt-builder', self.root / 'adaptive-prompt-builder')
        (self.root / 'adaptive-prompt-builder/SKILL.md').write_text('private custom instructions')
        before = hashes(self.root)
        result = self.install('--migrate', success=False)
        self.assertIn('manual merge', result.stderr.lower())
        self.assertEqual(before, hashes(self.root))
        self.assertFalse((self.root / 'prompt-forge').exists())

    def test_extra_legacy_file_and_symlink_refused(self):
        legacy = self.root / 'adaptive-prompt-builder'
        shutil.copytree(self.repo / 'skills/adaptive-prompt-builder', legacy)
        extra = legacy / 'private-notes.md'
        extra.write_text('preserve this')
        before = hashes(self.root)
        self.install('--migrate', success=False)
        self.assertEqual(before, hashes(self.root))
        extra.unlink()
        (legacy / 'linked-reference').symlink_to(self.repo / 'LICENSE')
        self.install('--migrate', success=False)
        self.assertTrue((legacy / 'linked-reference').is_symlink())
        self.assertFalse((self.root / 'prompt-forge').exists())

    def test_custom_canonical_and_extra_files_refused(self):
        self.install()
        (self.root / 'prompt-forge/notes.txt').write_text('keep me')
        before = hashes(self.root)
        self.install('--migrate', success=False)
        self.assertEqual(before, hashes(self.root))
        (self.root / 'prompt-forge/notes.txt').unlink()
        (self.root / 'prompt-forge/SKILL.md').write_text('custom canonical')
        before = hashes(self.root)
        self.install(success=False)
        self.assertEqual(before, hashes(self.root))

    def test_alias_is_standalone_and_synchronized(self):
        spec = importlib.util.spec_from_file_location('distribution_package', self.repo / 'scripts/package.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        expected = module.alias_files()
        self.assertEqual(set(expected), set(hashes(self.repo / 'skills/adaptive-prompt-builder')))
        for name, data in expected.items():
            self.assertEqual(data, (self.repo / 'skills/adaptive-prompt-builder' / name).read_bytes())
        shutil.rmtree(self.repo / 'skills/prompt-forge')
        module.sources(self.repo / 'skills/adaptive-prompt-builder')

    def test_broken_link_and_drift_detection(self):
        self.command('package.py', '--check')
        skill = self.repo / 'skills/prompt-forge/SKILL.md'
        original = skill.read_text()
        skill.write_text(original + '\n[missing](references/missing.md)\n')
        self.assertIn('link', self.command('package.py', '--check', success=False).stderr.lower())
        skill.write_text(original + '\n[outside](../../LICENSE)\n')
        self.assertIn('escaping', self.command('package.py', '--check', success=False).stderr.lower())
        skill.write_text(original)
        alias = self.repo / 'skills/adaptive-prompt-builder/SKILL.md'
        alias.write_text(alias.read_text() + '\ndrift\n')
        self.assertIn('drift', self.command('package.py', '--check', success=False).stderr.lower())

    def test_portable_resolves_nested_resource_links(self):
        self.command('package.py')
        for name in ('prompt-forge', 'adaptive-prompt-builder'):
            text = (self.repo / 'portable' / (name + '.md')).read_text()
            self.assertNotIn('](routing-and-companions.md', text)
            self.assertIn('bounded build outline (included in this prompt)', text)
            self.assertEqual(text.count('## Bounded cost-aware routing'), 1)

    def test_historical_archives_preserved_and_drift_refused(self):
        historical = [self.repo / 'dist/adaptive-prompt-builder-v0.1.0.zip',
                      self.repo / 'dist/prompt-forge-v0.2.0.zip',
                      self.repo / 'dist/prompt-forge-v0.3.0.zip']
        before = {p: p.read_bytes() for p in historical}
        self.command('package.py')
        for path in historical:
            self.assertEqual(path.read_bytes(), before[path])
        historical[1].write_bytes(before[historical[1]] + b'drift')
        self.assertIn('frozen v0.2.0', self.command('package.py', '--check', success=False).stderr.lower())

    def test_zip_is_safe_complete_deterministic_and_versioned(self):
        archive = self.repo / 'dist/prompt-forge-v0.4.0.zip'
        original = archive.read_bytes()
        self.command('package.py')
        self.assertEqual(original, archive.read_bytes())
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(set(z.namelist()), {'prompt-forge/' + p for p in hashes(self.repo / 'skills/prompt-forge')})
            for info in z.infolist():
                self.assertFalse(info.filename.startswith('/'))
                self.assertNotIn('..', Path(info.filename).parts)
                self.assertEqual(info.external_attr >> 16, 0o100644)
        for line in (self.repo / 'dist/SHA256SUMS').read_text().splitlines():
            digest, name = line.split('  ', 1)
            self.assertEqual(digest, hashlib.sha256((self.repo / 'dist' / name).read_bytes()).hexdigest())
        skill = self.repo / 'skills/prompt-forge/SKILL.md'
        skill.write_text(skill.read_text().replace('0.4.0', '9.9.9'))
        self.assertIn('version', self.command('package.py', '--check', success=False).stderr.lower())


if __name__ == '__main__':
    unittest.main()
