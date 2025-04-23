selected=$(awk '/^Host / { print $2 }' ~/.ssh/config | fzf)
clear
ssh $(echo "$selected" | tr -d '\r')
