# ~/.bashrc
case $- in
    *i*) ;;
      *) return;;
esac
HISTCONTROL=ignoreboth
HISTSIZE=1000
PS1='\u@\h:\w\$ '
alias ll='ls -alF'
alias trust='sha256sum'
