#!/usr/bin/env python3
"""Integrar configuraciones sin versionar el .zshrc ni las identidades laborales."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

MANAGED = [
    ".config/ghostty/config", ".config/starship.toml",
    ".config/zsh/dotfiles.zsh", ".config/git/dotfiles.gitconfig",
    ".config/zsh/completion.zsh", ".config/atuin/config.toml",
    "Library/Application Support/lazygit/config.yml", ".tmux.conf",
]
LOCAL = [".zshrc", ".gitconfig", ".config/git/personal.gitconfig",
         ".config/chezmoi/chezmoi.toml"]
MARKER = "# >>> riosinda/dotfiles >>>"
END_MARKER = "# <<< riosinda/dotfiles <<<"


def git_config(file, *args, check=True):
    return subprocess.run(["git", "config", "--file", str(file), *args],
                          text=True, capture_output=True, check=check).stdout.strip()


def update_zsh(text):
    # Only remove known prompt initialization; preserve tool paths and plugins.
    text = re.sub(r"# >>> riosinda/dotfiles >>>\n.*?# <<< riosinda/dotfiles <<<\n?",
                  "", text, flags=re.S)
    text = re.sub(r'^if \[\[[^\n]*p10k-instant-prompt[^\n]*\n.*?^fi[ \t]*\n',
                  '', text, flags=re.M | re.S)
    lines = []
    for line in text.splitlines():
        if not line.lstrip().startswith('#') and (
            'powerlevel10k.zsh-theme' in line or 'source ~/.p10k.zsh' in line
        ):
            continue
        if line.startswith('ZSH_THEME='):
            line = 'ZSH_THEME="" # Prompt gestionado por Starship'
        lines.append(line)
    return '\n'.join(lines).rstrip() + '\n\n' + MARKER + '\n' + (
        '[[ -r "$HOME/.config/zsh/dotfiles.zsh" ]] && '
        'source "$HOME/.config/zsh/dotfiles.zsh"\n'
    ) + END_MARKER + '\n'


def backup(home):
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + f'-{os.getpid()}'
    folder = home / '.local/state/dotfiles/backups' / stamp
    folder.mkdir(parents=True, mode=0o700)
    existed = []
    for relative in MANAGED + LOCAL:
        path = home / relative
        if path.exists() or path.is_symlink():
            target = folder / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target, follow_symlinks=False)
            existed.append(relative)
    (folder / 'manifest.json').write_text(json.dumps({
        'existed': existed, 'managed': MANAGED + LOCAL,
    }, indent=2) + '\n')
    print(f'Respaldo local: {folder}')


def configure(home, repo):
    # Identity is collected before changing any local startup / Git files.
    personal = home / '.config/git/personal.gitconfig'
    legacy = home / '.gitconfig-personal'
    identity = {}
    for key, variable, label in [
        ('user.name', 'DOTFILES_GIT_NAME', 'Nombre para commits personales'),
        ('user.email', 'DOTFILES_GIT_EMAIL', 'Correo para commits personales'),
    ]:
        value = os.environ.get(variable, '')
        for file in [personal, legacy]:
            if not value and file.exists():
                value = git_config(file, '--get', key, check=False)
        if not value:
            value = input(f'{label}: ').strip()
        if not value or '\n' in value:
            raise SystemExit(f'Valor inválido para {key}')
        identity[key] = value

    zshrc = home / '.zshrc'
    text = zshrc.read_text() if zshrc.exists() else ''
    zshrc.write_text(update_zsh(text))
    personal.parent.mkdir(parents=True, exist_ok=True)
    for key, value in identity.items():
        git_config(personal, key, value)
        subprocess.run(['git', '-C', str(repo), 'config', '--local', key, value], check=True)
    global_config = home / '.gitconfig'
    common = '~/.config/git/dotfiles.gitconfig'
    includes = git_config(global_config, '--get-all', 'include.path', check=False).splitlines()
    if common not in includes:
        git_config(global_config, '--add', 'include.path', common)
    personal_key = 'includeIf.gitdir:~/Documents/personal-github/.path'
    personal_include = '~/.config/git/personal.gitconfig'
    paths = git_config(global_config, '--get-all', personal_key, check=False).splitlines()
    if personal_include not in paths:
        git_config(global_config, '--add', personal_key, personal_include)
    git_config(global_config, 'user.useConfigOnly', 'true')
    print('Git personal configurado para Documents/personal-github; reglas restantes conservadas.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['backup', 'configure'])
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--home', type=Path, default=Path.home())
    args = parser.parse_args()
    if args.action == 'backup':
        backup(args.home)
    else:
        configure(args.home, args.repo)


if __name__ == '__main__':
    main()
