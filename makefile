all: organizer.c judge.c player.c
	gcc -o organizer organizer.c -Wall
	gcc -o judge judge.c -Wall
	gcc -o player player.c -Wall

