# kphoen.zsh-theme

VIRTUAL_ENV_DISABLE_PROMPT=true

prompt_halt() {
    [[ $(jobs -l | wc -l) -gt 0 ]] && print -n "%{$fg[cyan]%}\u2699 %{$reset_color%}"
}

# Display current virtual environment
prompt_virtualenv() {
  if [[ -n $VIRTUAL_ENV ]]; then
    print -n "%{$FG[145]%} $(basename $VIRTUAL_ENV) %{$reset_color%}"
  fi
}

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg[white]%}\ue0a0"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY=""
ZSH_THEME_GIT_PROMPT_CLEAN=""

PROMPT='$(prompt_virtualenv)$(prompt_halt)%{$fg[cyan]%}%~%{$reset_color%} $(git_prompt_info)$(git_prompt_status)%{$reset_color%}
%(? > %{$fg[red]%}>%{$reset_color%}) '

ZSH_THEME_GIT_PROMPT_ADDED="%{$fg[green]%} ✚"
ZSH_THEME_GIT_PROMPT_MODIFIED="%{$fg[blue]%} ✹"
ZSH_THEME_GIT_PROMPT_DELETED="%{$fg[red]%} ✖"
ZSH_THEME_GIT_PROMPT_RENAMED="%{$fg[magenta]%} ➜"
ZSH_THEME_GIT_PROMPT_UNMERGED="%{$fg[yellow]%} ═"
ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$fg[cyan]%} ✭"
