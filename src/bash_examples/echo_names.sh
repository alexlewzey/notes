#!/bin/zsh

for NAME in $(cat names.txt); do
	if [ "$NAME" = "moje" ]; then
		echo "hello mr ${NAME}!"
	else
		echo "hi mr ${NAME}!"
	fi
done
