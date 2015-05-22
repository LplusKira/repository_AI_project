// **************************************************************************
//  File       [type.cpp]
//  Author     [where's our source?]
//  Synopsis   [The cpp file of Player and Judge]
//  Modify     [2015/05/22 where's our source?]
// **************************************************************************

#include "type.h"

//constructor
Judge::Judge()
{
}

Judge::rand4Cards(int p1_cards[], int p2_cards[], int p3_cards[], int p4_cards[], vector<int> mountain)
{
	srand(time(NULL));
	
	int i, pick, counter;
	vector<int> original_cards;
	for(i = 0;i<cardNum; i++)
		original_cards.push_back(i + 1);

	for(i = 0;i< _TotalPlayerNum_; i++)
	{
		for(counter = 0; counter< _InitCardsPerPlayer_; counter++)
		{
			pick = rand() % original_cards.size();
			if(i == 0)
				p1_cards[counter] = original_cards[pick];
			else if(i == 1)
				p2_cards[counter] = original_cards[pick];
			else if(i == 2)
				p3_cards[counter] = original_cards[pick];
			else
				p4_cards[counter] = original_cards[pick];

			swap(original_cards[pick], original_cards[original_cards.size() - 1]);
			original_cards.pop_back();
		}
	}

	//	TODO:	set mountain
	for(i = 0; i< original_cards.size(); i++)
	{
		pick = rand() % original_cards.size();
		mountain.push_back(original_cards[pick]);

		swap(original_cards[pick], original_cards[original_cards.size() - 1]);
			original_cards.pop_back();
	}
}

void Judge::giveCard(int changeMode, int user, int cards_user[5], int victim, int cards_victim[5])
{
}

void Judge::GameStart()
{
	srand(time(NULL));
	Player player_List[_TotalPlayerNum_];

	int current_player = 1;
	int next_player[_TotalPlayerNum_ + 1];
	for(i = 1; i< _TotalPlayerNum_ +1; i++)
		next_player[i] = i % _TotalPlayerNum_;
	while(next_player != 0)
	{
		if(player_List[current_player].getAction(current_player, player_state[current_player]) == _IamDead_)
	}
}