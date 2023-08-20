#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

setleds -D +num

if [[ "$(tty)" = /dev/tty1 ]]; then
	exec startx
fi
