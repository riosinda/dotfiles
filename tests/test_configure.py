import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    'configure', Path(__file__).resolve().parents[1] / 'scripts/configure.py')
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


class ConfigureTests(unittest.TestCase):
    def test_prompt_migration_preserves_other_startup_code_and_is_idempotent(self):
        text = '''if [[ -d /local/tool ]]; then
  export CUSTOM_TOOL=1
fi
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
ZSH_THEME="robbyrussell"
plugins=(git)
source $ZSH/oh-my-zsh.sh
source ~/powerlevel10k/powerlevel10k.zsh-theme
source ~/powerlevel10k/powerlevel10k.zsh-theme
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
export PATH="$HOME/.local/opt/node/bin:$PATH"
'''
        result = config.update_zsh(text)
        self.assertNotIn('source ~/powerlevel10k', result)
        self.assertNotIn('p10k-instant-prompt', result)
        self.assertIn('export CUSTOM_TOOL=1', result)
        self.assertIn('source $ZSH/oh-my-zsh.sh', result)
        self.assertIn('export PATH="$HOME/.local/opt/node/bin:$PATH"', result)
        self.assertEqual(config.update_zsh(result), result)

    def test_preserves_work_rules_and_personal_ssh_include(self):
        with tempfile.TemporaryDirectory() as root:
            home = Path(root)
            repo = home / 'repo'
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (home / '.gitconfig').write_text('''[user]
    email = work@example.test
[includeIf "gitdir:~/Documents/personal-github/"]
    path = ~/.gitconfig-personal
[includeIf "gitdir:/Volumes/test/work/"]
    path = ~/.gitconfig-work
''')
            (home / '.gitconfig-personal').write_text('''[user]
    name = Test Person
    email = personal@example.test
[url "git@github-personal:"]
    insteadOf = https://github.com/
''')
            original = (home / '.gitconfig-personal').read_text()
            config.backup(home)
            config.configure(home, repo)
            once = (home / '.gitconfig').read_text()
            config.configure(home, repo)
            self.assertEqual((home / '.gitconfig').read_text(), once)
            self.assertIn('work@example.test', once)
            self.assertIn('~/.gitconfig-work', once)
            self.assertIn('~/.gitconfig-personal', once)
            self.assertEqual((home / '.gitconfig-personal').read_text(), original)
            self.assertEqual(config.git_config(repo / '.git/config', '--get', 'user.email'),
                             'personal@example.test')
            saved = list((home / '.local/state/dotfiles/backups').glob('*/.gitconfig'))
            self.assertEqual(len(saved), 1)
            self.assertIn('work@example.test', saved[0].read_text())


if __name__ == '__main__':
    unittest.main()
