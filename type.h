// **************************************************************************
//  File       [type.h]
//  Author     [where's our source?]
//  Synopsis   [The header file of Player and Judge]
//  Modify     [2015/05/22 where's our source?]
// **************************************************************************
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <sys/time.h>
#include <vector>
#include <string>
#include <iostream>

#ifndef _TYPE_H
#define _TYPE_H
using namespace std;

const int _InitCardsPerPlayer_ = 5;
const int _TotalPlayerNum_ = 4;
const int _cardNum_ = 52;
const int _MaxCombCardNum_ = 5;
const int _MaxActionLength_ = 20;
const int _MaxComb_ = 32;
const char _PlayerExecName_[] = "./player";
const char _ReadFilePath_[] = "./playerLog";
int Player_cards[_TotalPlayerNum_][_MaxCombCardNum_];
//const int _IamDead_ = -1;

typedef struct Action{
	int user;
	int cards_used[_MaxCombCardNum_];
	int victim;
}action;

typedef struct PossibleCombination{
	int combination[5];
}possible_comb;

typedef struct State{
	vector<action> one_run_history;
    vector<action> what_player_can_do;
	vector<int> what_player_canNOT_do;
	int 1st, 2nd, 3rd, 4th, mountain_remaining, points, clock_wise;
}state;

class Judge
{
	public:
		Judge();
		void rand4Cards();
		void GameStart();
		//void TellAgent(int which_agent, state what_happened);
		//void giveCard(int changeMode, int user, int cards_user[5], int victim, int cards_victim[5]);
		state player_state[_TotalPlayerNum_];
		bool checkRule(action);
		vector<action> getAction();
	private:
		vector<action> history;
		vector<action> _possibleActions_;
		vector< vector<int> > card;//sort big->small
		vector<int> mountain;
		int point;
		int clock_wise;
		int current_player;
};

#endif
