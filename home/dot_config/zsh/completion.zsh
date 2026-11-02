# Completar con Tab también en una Mac sin Oh My Zsh.
[[ -o interactive ]] || return
if (( ! $+functions[compdef] )); then
  autoload -Uz compinit
  compinit
fi
zstyle ':completion:*' menu select

# Se usan los completados oficiales de las herramientas instaladas.
(( $+commands[npm] )) && source <(npm completion)
(( $+commands[uv] )) && eval "$(uv generate-shell-completion zsh)"
(( $+commands[uvx] )) && eval "$(uvx --generate-shell-completion zsh)"

# Homebrew en Apple Silicon o Intel, sin depender del SSD.
for _dotfiles_autosuggest in /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh \
                            /usr/local/share/zsh-autosuggestions/zsh-autosuggestions.zsh; do
  if [[ -r "$_dotfiles_autosuggest" ]]; then
    source "$_dotfiles_autosuggest"
    break
  fi
done
unset _dotfiles_autosuggest
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#888888'
ZSH_AUTOSUGGEST_STRATEGY=(history completion)

if (( $+commands[atuin] )); then
  export ATUIN_CONFIG_DIR="$HOME/.config/atuin"
  # fzf conserva Ctrl-r; las flechas mantienen su comportamiento habitual.
  eval "$(atuin init zsh --disable-up-arrow --disable-ctrl-r --disable-ai)"
  _zsh_autosuggest_strategy_directory() {
    suggestion=$(ATUIN_QUERY="$1" atuin search --filter-mode directory \
      --search-mode prefix --cmd-only --limit 1 2>/dev/null)
  }
  ZSH_AUTOSUGGEST_STRATEGY=(directory history completion)
fi
