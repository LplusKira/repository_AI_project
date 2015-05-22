#include "type.h"
#include <alogrithm>
const int buffSize = 1000;
int const cardNum = 52;
int const one = 1;

int main(int argc, char *argv[])
{
	int whichPlayer, i, j;
	int Nplayer = _TotalPlayerNum_;

		Judge ourJudge();

		//	TODO: 	set 4 piles of cards
		ourJudge.rand4Cards(p1_cards, p2_cards, p3_cards, p4_cards, mountain);
		
		//	TODO:	game start
		ourJudge.GameStart();
	exit(0);
}