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
const int buffSize = 1000;
int const cardNum = 53;
const char judge[] = "judge";
const char FIFO[] = ".FIFO";
const char AFIFO[] = "_A.FIFO";
const char BFIFO[] = "_B.FIFO";
const char CFIFO[] = "_C.FIFO";
const char DFIFO[] = "_D.FIFO";
const char theEnd[] = "0 0 0 0";
int const one = 1;
void rand4Cards(int pA[], int pB[], int pC[], int pD[], int j_id)
{
	struct timeval t1;
	gettimeofday(&t1, NULL);
	srand(t1.tv_usec * t1.tv_sec);
	
	int i, pick, count, j, k;
	int cards[cardNum];
	for(i = 0;i<cardNum;i++)
		cards[i] = 0;
	for(i = 0;i<4;i++)
	{
		if(i == 0)
		{
			//printf("j_id = %d, ", j_id);
			for(j = 0;j<14;j++)
			{
				pick = (rand()/j_id) % (53 - j);
				count = 0;
				for(k = 0;k<53;k++)
				{
					if(cards[k] == 0)
					{
						if(count == pick)
						{
							cards[k] = 1;
							break;
						}
						else
							count = count + 1;
					}
				}
				pA[j] = k;
				//printf("pA[%d] = %d ", j, pA[j]);
			}
			//printf("\n");
		}
		else
		{
			for(j = 0;j<13;j++)
			{
				pick = (rand()/j_id) % (39 - (j + (i-1)*13));
				count = 0;
				for(k = 0;k<53;k++)
				{
					if(cards[k] == 0)
					{
						if(count == pick)
						{
							cards[k] = 1;
							break;
						}
						else
							count = count + 1;
					}
				}
				if(i == 1)
					pB[j] = k;
				else if(i == 2)
					pC[j] = k;
				else
					pD[j] = k;
			}
		}
	}
}
void PDo1(int tempValue, int ind, int fd[])
{
	char OurBuf[buffSize];
	sprintf(OurBuf, "< %d\n", tempValue);
	write(fd[ind], OurBuf, strlen(OurBuf));
}
void PDo3(int tempValue[], int ind, int fd[], int key)
{
	char OurBuf[buffSize];
	tempValue[0] = 0;
	tempValue[1] = 0;
	tempValue[2] = 0;
	int j;
	for(j = 0;j<3;j++)
	{
		while(1)
		{
			read(fd[5], OurBuf, 1);
			if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
				break;
			else if(OurBuf[0] - 'A' == 0)
				tempValue[j] = 0;
			else if(OurBuf[0] - 'B' == 0)
				tempValue[j] = 1;
			else if(OurBuf[0] - 'C' == 0)
				tempValue[j] = 2;
			else if(OurBuf[0] - 'D' == 0)
				tempValue[j] = 3;
			else
				tempValue[j] = tempValue[j] * 10 + (OurBuf[0] - '0');
		}
	}
	if(key != tempValue[1])
	{
		PDo3(tempValue, ind, fd, key);
		return;
	}
	else
	{
		sprintf(OurBuf, "> %d\n", tempValue[2]);
		write(fd[ind], OurBuf, strlen(OurBuf));
		return;
	}
}
void PDo5(int tempValue[], int ind, int fd[], int key)
{
	char OurBuf[buffSize];
	tempValue[0] = 0;
	tempValue[1] = 0;
	tempValue[2] = 0;
	int j;
	for(j = 0;j<3;j++)
	{
		while(1)
		{
			read(fd[5], OurBuf, 1);
			if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
				break;
			else if(OurBuf[0] - 'A' == 0)
				tempValue[j] = 0;
			else if(OurBuf[0] - 'B' == 0)
				tempValue[j] = 1;
			else if(OurBuf[0] - 'C' == 0)
				tempValue[j] = 2;
			else if(OurBuf[0] - 'D' == 0)
				tempValue[j] = 3;
			else
				tempValue[j] = tempValue[j] * 10 + (OurBuf[0] - '0');
		}
	}
	if(key != tempValue[1])
	{
		PDo5(tempValue, ind, fd, key);
		return;
	}
	else
	{
		sprintf(OurBuf, "> %d\n", tempValue[2]);
		write(fd[ind], OurBuf, strlen(OurBuf));
		return;
	}
}
void PDo7(int tempValue[], int fd[], int tempPrior[], int tempLater[], int key)
{
	char OurBuf[buffSize];
	tempValue[0] = 0;
	tempValue[1] = 0;
	tempValue[2] = 0;
	int j;
	for(j = 0;j<3;j++)
	{
		while(1)
		{
			read(fd[5], OurBuf, 1);
			if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
				break;
			else if(OurBuf[0] - '-' == 0)
			{
				while(1)
				{
					read(fd[5], OurBuf, 1);
					if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
						break;
					else
						tempValue[j] = tempValue[j] * 10 + (OurBuf[0] - '0');
				}
				tempValue[j] = tempValue[j] * (-1);
				break;
			}
			else if(OurBuf[0] - 'A' == 0)
				tempValue[j] = 0;
			else if(OurBuf[0] - 'B' == 0)
				tempValue[j] = 1;
			else if(OurBuf[0] - 'C' == 0)
				tempValue[j] = 2;
			else if(OurBuf[0] - 'D' == 0)
				tempValue[j] = 3;
			else
				tempValue[j] = tempValue[j] * 10 + (OurBuf[0] - '0');
		}
	}
	if(key != tempValue[1])
	{
		PDo7(tempValue, fd, tempPrior, tempLater, key);
		return;
	}
	else
	{
		//updates
		tempLater[1] = tempLater[1] - 1;
		if(tempValue[2] == 1)
			tempPrior[1] = tempPrior[1] - 1;
		else
			tempPrior[1] = tempPrior[1] + 1;
		return;
	}
}
int main(int argc, char *argv[])
{
	int len, i, n, pid, j, ind;
	int key[4], readyToKill[4];
	int j_id = 0;
	char OurBuf[buffSize];
	char judgeid[4];

	//TODO: collect j_id + read wirte pipe
	len = strlen(argv[1]);
	for(i = 0;i<len;i++)
		j_id = j_id * 10 + (argv[1][i] - '0');
	sprintf(judgeid, "%d", j_id);
	//TODO: create names of judgej_id.FIFO get resp from players; 	judgej_id_A.FIFO, ..., judgej_id_A.FIFO write to players
	sprintf(OurBuf, "%s%d%s", judge, j_id, FIFO);
	n = strlen(OurBuf);
	char judgeFIFO[n];
	sprintf(judgeFIFO, "%s", OurBuf);
	
	sprintf(OurBuf, "%s%d%s", judge, j_id, AFIFO);
	n = strlen(OurBuf);
	char judgeAFIFO[n];
	sprintf(judgeAFIFO, "%s", OurBuf);
	
	sprintf(OurBuf, "%s%d%s", judge, j_id, BFIFO);
	n = strlen(OurBuf);
	char judgeBFIFO[n];
	sprintf(judgeBFIFO, "%s", OurBuf);
	
	sprintf(OurBuf, "%s%d%s", judge, j_id, CFIFO);
	n = strlen(OurBuf);
	char judgeCFIFO[n];
	sprintf(judgeCFIFO, "%s", OurBuf);
	
	sprintf(OurBuf, "%s%d%s", judge, j_id, DFIFO);
	n = strlen(OurBuf);
	char judgeDFIFO[n];
	sprintf(judgeDFIFO, "%s", OurBuf);
		
	int loser = 1;
	int fd[6];
	int tempValue[6][3];
	int p[4][14];
	int id, k, m, Nplayer;
	int next[5], exist[5], player[5];

	srand(time(NULL));
	while(1)
	{
		//TODO: read data from pipe
		for(j = 0;j<5;j++)
			player[j] = 0;
		for(j = 0;j<4;j++)
		{
			while(1)
			{
				read(STDIN_FILENO, OurBuf, 1);
				if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
					break;
				else
					player[j] = player[j] * 10 + (OurBuf[0] - '0');
			}
		}
		//TODO: execute + write back
		if(player[0] == player[1] && player[1] == player[2] && player[2] ==  player[3] &&  player[3] == 0)
		{	
			sleep(3);
			break;
		}
		else
		{
			//TODO: create 5 FIFOs
			mkfifo(judgeFIFO, 04755);
			mkfifo(judgeAFIFO, 04755);
			mkfifo(judgeBFIFO, 04755);
			mkfifo(judgeCFIFO, 04755);
			mkfifo(judgeDFIFO, 04755);
			//TODO: producing rand key
			for(i = 0;i<4;i++)
				key[i] = (rand()/j_id) % 65536;
			//TODO: fork 4 players
			for(k = 1; k<5;k++)
				next[k] = k + 1;
			next[4] = 1;
			for(k = 1;k<5;k++)
				exist[k] = 1;
			Nplayer = 4;
			for(id = 0;id<4;id++)
				if((pid = fork()) == 0)
					break;
				else
					readyToKill[id] = pid;
			//TODO: P, set 4 piles of cards
			if(pid > 0)
			{
				rand4Cards(p[0], p[1], p[2], p[3], j_id);
				for(i = 0;i<13;i++)
				{
					p[0][i] = (p[0][i]/4) + 1;
					p[1][i] = (p[1][i]/4) + 1;
					p[2][i] = (p[2][i]/4) + 1;
					p[3][i] = (p[3][i]/4) + 1;
					if(p[0][i] == 14)
						p[0][i] = 0;
					else if(p[1][i] == 14)
						p[1][i] = 0;
					else if(p[2][i] == 14)
						p[2][i] = 0;
					else if(p[3][i] == 14)
						p[3][i] = 0;
				}
					p[0][13] = (p[0][13]/4) + 1;
					if(p[0][13] == 14)
						p[0][13] = 0;
			}
			//TODO: P, send cards; C, get cards + rearrange
			if(pid > 0)
			{
				fd[1] = open(judgeAFIFO, O_RDWR);
				fd[2] = open(judgeBFIFO, O_RDWR);
				fd[3] = open(judgeCFIFO, O_RDWR);
				fd[4] = open(judgeDFIFO, O_RDWR);
				fd[5] = open(judgeFIFO, O_RDWR);
		
				sprintf(OurBuf, "%d %d %d %d %d %d %d %d %d %d %d %d %d %d\n", p[0][0], p[0][1], p[0][2], p[0][3], p[0][4], p[0][5], p[0][6], p[0][7], p[0][8], p[0][9], p[0][10], p[0][11], p[0][12], p[0][13]);
				write(fd[1], OurBuf, strlen(OurBuf));
				sprintf(OurBuf, "%d %d %d %d %d %d %d %d %d %d %d %d %d\n", p[1][0], p[1][1], p[1][2], p[1][3], p[1][4], p[1][5], p[1][6], p[1][7], p[1][8], p[1][9], p[1][10], p[1][11], p[1][12]);
				write(fd[2], OurBuf, strlen(OurBuf));
				sprintf(OurBuf, "%d %d %d %d %d %d %d %d %d %d %d %d %d\n", p[2][0], p[2][1], p[2][2], p[2][3], p[2][4], p[2][5], p[2][6], p[2][7], p[2][8], p[2][9], p[2][10], p[2][11], p[2][12]);
				write(fd[3], OurBuf, strlen(OurBuf));
				sprintf(OurBuf, "%d %d %d %d %d %d %d %d %d %d %d %d %d\n", p[3][0], p[3][1], p[3][2], p[3][3], p[3][4], p[3][5], p[3][6], p[3][7], p[3][8], p[3][9], p[3][10], p[3][11], p[3][12]);
				write(fd[4], OurBuf, strlen(OurBuf));
			}
			else
			{
				if(id == 0)
				{
					fd[1] = open(judgeAFIFO, O_RDWR);
					fd[5] = open(judgeFIFO, O_RDWR);
					sprintf(OurBuf, "%d", key[id]);
					execlp("./player", "./player", judgeid,"A",OurBuf,(char*)0);
				}
				else if(id == 1)
				{
					fd[2] = open(judgeBFIFO, O_RDWR);
					fd[5] = open(judgeFIFO, O_RDWR);
					sprintf(OurBuf, "%d", key[id]);
					execlp("./player", "./player", judgeid,"B",OurBuf,(char*)0);
				}
				else if(id == 2)
				{
					fd[3] = open(judgeCFIFO, O_RDWR);
					fd[5] = open(judgeFIFO, O_RDWR);
					sprintf(OurBuf, "%d", key[id]);
					execlp("./player", "./player", judgeid,"C",OurBuf,(char*)0);
				}
				else if(id == 3)
				{
					fd[4] = open(judgeDFIFO, O_RDWR);
					fd[5] = open(judgeFIFO, O_RDWR);
					sprintf(OurBuf, "%d", key[id]);
					execlp("./player", "./player", judgeid,"D",OurBuf,(char*)0);
				}
			}
			
			if(pid > 0)
			{
				//TODO: P, get # of cards
				for(i = 0;i<4;i++)
				{
					tempValue[5][0] = 0;
					tempValue[5][1] = 0;
					tempValue[5][2] = 0;
					for(j = 0;j<3;j++)
					{
						while(1)
						{
							read(fd[5], OurBuf, 1);
							if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
								break;
							else if(OurBuf[0] - 'A' == 0)
								tempValue[5][j] = 0;
							else if(OurBuf[0] - 'B' == 0)
								tempValue[5][j] = 1;
							else if(OurBuf[0] - 'C' == 0)
								tempValue[5][j] = 2;
							else if(OurBuf[0] - 'D' == 0)
								tempValue[5][j] = 3;
							else
								tempValue[5][j] = tempValue[5][j] * 10 + (OurBuf[0] - '0');
						}
					}
					for(j = 0;j<4;j++)
					{
						if(tempValue[5][0] == j)
						{
							tempValue[j][0] = tempValue[5][0];
							tempValue[j][1] = tempValue[5][2];
							tempValue[j][2] = tempValue[5][1];
							break;
						}
					}
				}
				//TODO: P, in game
				i = 4;
				while(Nplayer > 1)
				{
					i = next[i];
			
					//1
					ind = i;
					PDo1(tempValue[next[i]-1][1], ind, fd);
					//3
					ind = next[i];
					PDo3(tempValue[5], ind, fd, tempValue[i-1][2]);
					//5
					ind = i;
					PDo5(tempValue[5], ind, fd, tempValue[next[i]-1][2]);
					//7
					PDo7(tempValue[5], fd, tempValue[i - 1], tempValue[next[i] - 1], tempValue[i-1][2]);
					if(tempValue[i-1][1] == 0)
					{
						for(m = 1;m<5;m++)
							if(next[m] == i && exist[m]>0)
								break;
						exist[i] = 0;
						Nplayer = Nplayer - 1;
						next[m] = next[i];
						i = m;
					}
					if(tempValue[next[i]-1][1] == 0)
					{
						for(m = 1;m<5;m++)
							if(next[m] == next[i] && exist[m]>0)
								break;
						exist[next[i]] = 0;
						Nplayer = Nplayer - 1;
						next[m] = next[next[i]];
						i = m;
					}
				}
				loser = player[next[i] - 1];
				
				sprintf(OurBuf, "%d\n", loser);
				write(STDOUT_FILENO, OurBuf, strlen(OurBuf));
				//TODO: kill 4 players
				for(i = 0;i<4;i++)
				{
					kill(readyToKill[i], SIGKILL);
					waitpid(readyToKill[i], NULL, 0);
				}
				//TODO: unlink 5 FIFOs
				unlink(judgeFIFO);
				unlink(judgeAFIFO);
				unlink(judgeBFIFO);
				unlink(judgeCFIFO);
				unlink(judgeDFIFO);
				
				//TODO: close fd
				for(i = 1;i<6;i++)
					close(fd[i]);
			}		
		}
	}
	exit(0);
}
