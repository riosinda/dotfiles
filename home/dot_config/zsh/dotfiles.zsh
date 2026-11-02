# Se carga al final de ~/.zshrc; las rutas y configuraciones locales se conservan.
[[ -o interactive ]] || return

if [[ -x /opt/homebrew/bin/brew && ":$PATH:" != *:/opt/homebrew/bin:* ]]; then
  path=(/opt/homebrew/bin /opt/homebrew/sbin $path)
elif [[ -x /usr/local/bin/brew && ":$PATH:" != *:/usr/local/bin:* ]]; then
  path=(/usr/local/bin /usr/local/sbin $path)
fi
typeset -U path

[[ -r "$HOME/.config/zsh/completion.zsh" ]] && source "$HOME/.config/zsh/completion.zsh"

if (( $+commands[fzf] )); then
  export FZF_DEFAULT_OPTS='--height=40% --layout=reverse --border'
  if (( $+commands[fd] )); then
    export FZF_DEFAULT_COMMAND='fd --type f --hidden --exclude .git'
    export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
    export FZF_ALT_C_COMMAND='fd --type d --hidden --exclude .git'
  fi
  source <(fzf --zsh)
fi
(( $+commands[zoxide] )) && eval "$(zoxide init zsh)"
(( $+commands[starship] )) && eval "$(starship init zsh)"

alias lg='lazygit'
alias tl='tmux list-sessions'
alias ta='tmux attach-session -t'
alias dots='cd "$HOME/Documents/personal-github/dotfiles"'

# Sesión identificada por nombre + ruta: dos carpetas iguales no se mezclan.
function tp() {
  local base_name="${PWD:t}"
  base_name="${base_name//[^[:alnum:]_-]/-}"
  local session_name="${1:-${base_name}-$(printf '%s' "$PWD" | cksum | cut -d ' ' -f 1)}"
  if [[ "$session_name" != [[:alnum:]_]* || "$session_name" == *[^[:alnum:]_-]* ]]; then
    print -u2 'Usa un nombre de sesión con letras, números, guiones o guiones bajos.'
    return 1
  fi
  if [[ -n "$TMUX" ]]; then
    tmux has-session -t "=$session_name" 2>/dev/null ||
      tmux new-session -d -s "$session_name" -c "$PWD" || return
    tmux switch-client -t "=$session_name"
  else
    tmux new-session -A -s "$session_name" -c "$PWD"
  fi
}
