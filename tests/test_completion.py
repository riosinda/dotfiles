"""Integración con herramientas reales; todo el historial de prueba es temporal."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        config = self.home / '.config/atuin'
        config.mkdir(parents=True)
        shutil.copy2(ROOT / 'home/dot_config/atuin/config.toml', config)
        self.env = {
            'HOME': str(self.home), 'PATH': os.environ['PATH'],
            'TERM': 'xterm-256color', 'ATUIN_CONFIG_DIR': str(config),
            'XDG_CONFIG_HOME': str(self.home / '.config'),
            'XDG_DATA_HOME': str(self.home / '.local/share'),
            'XDG_CACHE_HOME': str(self.home / '.cache'),
        }
        for directory in ('frontend', 'backend'):
            (self.home / directory).mkdir()

    def shell(self, script):
        result = subprocess.run(
            ['zsh', '-fic', 'source "$1"\n' + script, 'test',
             str(ROOT / 'home/dot_config/zsh/completion.zsh')],
            env=self.env, cwd=self.home, text=True, capture_output=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        return result.stdout.strip()

    def test_suggestions_persist_and_prefer_current_directory(self):
        self.shell('''
            cd "$HOME/frontend"
            _atuin_preexec 'npm run dev'
            atuin history end --exit 0 "$ATUIN_HISTORY_ID"
            cd "$HOME/backend"
            _atuin_preexec 'npm run build'
            atuin history end --exit 0 "$ATUIN_HISTORY_ID"
        ''')
        output = self.shell('''
            cd "$HOME/frontend"
            _zsh_autosuggest_fetch_suggestion 'npm run '
            print -r -- "$suggestion"
            cd "$HOME/backend"
            _zsh_autosuggest_fetch_suggestion 'npm run '
            print -r -- "$suggestion"
        ''')
        self.assertEqual(output.splitlines(),
                         ['npm run dev', 'npm run build'])


if __name__ == '__main__':
    unittest.main()
