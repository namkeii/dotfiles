#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias dotfile='/usr/bin/git --git-dir=$HOME/.dotfiles.git/ --work-tree=$HOME'

GREEN="\[$(tput setaf 2)\]"
RESET="\[$(tput sgr0)\]"
PS1="${GREEN}[\u@\h \W]\$${RESET} "

#PS1='[\u@\h \W]\$ '
