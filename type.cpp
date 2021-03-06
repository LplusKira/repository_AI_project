// **************************************************************************
//  File       [type.cpp]
//  Author     [where's our source?]
//  Synopsis   [The cpp file of Player and Judge]
//  Modify     [2015/05/22 where's our source?]
// **************************************************************************

#include "type.h"
#include <unistd.h>

//constructor
Judge::Judge()
{
  this.GameStart();
}


void Judge::GameStart()
{
  char ourBuf[_MaxActionLength_];
  char parsingBuf_possibleActions[_MaxComb_ * _MaxActionLength_];
  srand(time(NULL));
  int i, status;
  initBoard();
  rand4Cards();
  while(!isGameFinished())
  {
    this.writeFile();//write state
    //  clear parsingBuf_possibleActions
    for(i = 0;i<_MaxComb_ * _MaxActionLength_; i++)
      parsingBuf_possibleActions[i] = '\0';
    for(i = 0; i < _possibleActions_.size(); i++)
    {
      sprintf(ourBuf, "%d %d %d %d %d %d %d;", _possibleActions_[i].user, _possibleActions_[i].cards_used[0], _possibleActions_[i].cards_used[1], _possibleActions_[i].cards_used[2], _possibleActions_[i].cards_used[3], _possibleActions_[i].cards_used[4], _possibleActions_[i].victim);
      strncat(parsingBuf_possibleActions, ourBuf, strlen(ourBuf));
    }

    //  TODO: call python agent
    if((pid = fork()) == 0) //  child
    {
      //  TODO: transmit history, _possibleActions_
      execlp(_PlayerExecName_, _PlayerExecName_, parsingBuf_possibleActions ,(char*)0);
    }

    //  TODO: wait for your child to be dead...
    waitpid(-1, &status, 0);

    action a = this.readFile();
    this.doAction(a);
  }
  //maybe judge need more precise history for debug usage
}

void Judge::initBoard(){
  current_player = 1;
  clock_wise = 1;//1 and -1
  //cards
}

void Judge::rand4Cards()
{
	srand(time(NULL));
	
	int i, pick, counter;
	vector<int> original_cards;
	for(i = 0;i< _cardNum_; i++)
		original_cards.push_back(i + 1);

	for(i = 0;i< _TotalPlayerNum_; i++)
	{
		for(counter = 0; counter< _InitCardsPerPlayer_; counter++)
		{
			pick = rand() % original_cards.size();
      Player_cards[i][counter] = original_cards[pick];
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

bool Judge::isGameFinished(){
  //return this.card[0].length() == 0...;
}

//  TODO: write possibe combinations to the current player
void Judge::writeFile(){
  generateStateData();
}
void generateStateData(){
  //including legal actions, history, ...
  //different from judge data, only have partial information
  _possibleActions_ = getAction();
}
vector<action> Judge::getAction(){
  vector<int> card = card[current_player];
  int n = card.length();
  vector<bool> isuse(n);
  vector<action> av;
  for(int i = 0; i < n; i++)
    isuse[i] = false;
  action a;
  a.user = current_player;
  while(nextbool(av, n)){
    int nowv = 0;
    a.cards.clear();
    for(int i = 0; i < n; i++)
      if(isuse[i]){
	nowv += card[i]%13;
	a.cards.push_back(card[i]);
      }
    if(nowv > 13)
      continue;
    else
      nowv %= 13;
    switch(nowv){
    case 7: case 9:
      for(int i = 0; i < _TotalPlayerNum_; i++){
	if(i == current_player || this.card[i].length() == 0)//todo: isdead?
	  continue;
	a.victim = i;
	av.push_back(a);
      }
      break;
    case 5:
      for(int i = 0; i < _TotalPlayerNum_; i++){
	if(this.card[i].length() == 0)//can use to user itself
	  continue;
	a.victim = i;
	av.push_back(a);
      }
      break;
    case 10: case 12:
      int value = (nowv == 10)?10:20;
	if(this.point + value <= 99){
	  a.victim = -1;
	  av.push_back(a);
	}
	if(this.point - value >= 0){
	  a.victim = -2;
	  av.push_back(a);
	}
      break;
    case 4: case 11: case 13: default:
      av.push_back(a);//do not consider victim
      break;
    }
  }
  return av;
}
bool nextbool(vector<bool>& vb, int n){
  int nowv = 0;
  for(int i = 0; i < n; i++){
    nowv *= 2;
    nowv += (vb[i])?1:0;
  }
  nowv++;
  if(nowv >= power(2, n)){
    return false;
  }
  for(int i = n;i >= 0; i--){
    vb[i] = (nowv%2)?true:false;
    nowv /= 2;
  }
  return true;
}


//  TODO: readfile written by the current player, assuming the current player always overwrites the file
action Judge::readFile(){
  char ToBeHistory[_MaxActionLength_];
  FILE* fp = fopen(_ReadFilePath_, "r");
  //int user, card[_MaxCombCardNum_], victim;
  action act;

  fscanf(fp, "%d %d %d %d %d %d %d", act.user, act.cards_used[0], act.cards_used[1], act.cards_used[2], act.cards_used[3], act.cards_used[4], act.victim);
  return act;
}

void Judge::doAction(action a){
  //  add in history
  history.push_back(a);

  //  addjust current player
  current_player += clock_wise;
  if(current_player == 0)
    current_player = 4;
  else if(current_player == 5)
    current_player = 1;
}


//  TODO: check whether data has been transmitted well (e.g. human player may do sth. wrong)
bool Judge::checkRule(action a){//assume cards exist
  int cardValue = 0;
  for(int i = 0; i < _MaxCombCardNum_; i++){
    cardValue += a.cards_used[i];
    if(a.cards_used[i] == 1){//space one
      iszero = true;
    }
  }
  if(iszero && cardValue == 1){
    return true;
  }
  switch(cardValue%13){
  case 7:
    if (a.victim > 0 && a.victim <= 4 && a.victim != a.user && this.card[a.victim-1].length() >= 1)//now user id?
      return true;
    break;
  case 9:
    if (a.victim > 0 && a.victim <= 4 && a.victim != a.user)//now user id?
      return true;
    break;
  case 5:
    if (a.victim > 0 && a.victim <= 4)
      return true;
    break;
  case 4:  case 11:  case 13:
    return true;
    break;
  case 12: case 10:
    int value = (cardValue % 13 == 12)?20:10;
    if(a.victim == -1 && this.point + value <= 99 || a.victim == -2 && this.point - value >= 0)
      return true;
    break;
  default:
    if(this.point+cardValue <= 99)
      return true;
  }
  return false;
}
