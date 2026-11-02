#!/bin/bash
set -euo pipefail
DOTFILES_REPO="$(cd "$(dirname "$0")" && pwd -P)"
if [[ "$(uname -s)" != Darwin ]]; then
  echo 'Este instalador está validado para macOS. Linux requiere adaptación.' >&2
  exit 1
fi
case "${1:-}" in
  '') install_packages=true ;;
  --skip-packages) install_packages=false ;;
  *) echo "Uso: $0 [--skip-packages]" >&2; exit 1 ;;
esac
if ! command -v brew >/dev/null; then
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  else
    echo 'Instala Homebrew desde https://brew.sh y vuelve a ejecutar este script.' >&2
    exit 1
  fi
fi
command -v python3 >/dev/null || { echo 'Se requiere Python 3 (Command Line Tools o Homebrew).' >&2; exit 1; }
if "$install_packages"; then
  HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 \
    brew bundle install --file "$DOTFILES_REPO/Brewfile" --no-upgrade
fi
command -v chezmoi >/dev/null
python3 "$DOTFILES_REPO/scripts/configure.py" backup --repo "$DOTFILES_REPO"
chezmoi init --source "$DOTFILES_REPO"
chezmoi --source "$DOTFILES_REPO" --no-pager diff
chezmoi --source "$DOTFILES_REPO" apply
python3 "$DOTFILES_REPO/scripts/configure.py" configure --repo "$DOTFILES_REPO"
echo 'Listo. Abre una terminal nueva; en Ghostty recarga con Cmd+Shift+,.'
