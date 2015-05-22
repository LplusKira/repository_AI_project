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
#include <vector>
const char judge[] = "judge";
const char FIFO[] = ".FIFO";
const char AFIFO[] = "_A.FIFO";
const char BFIFO[] = "_B.FIFO";
const char CFIFO[] = "_C.FIFO";
const char DFIFO[] = "_D.FIFO";
const int buffSize = 1000;

void fifo_test(std::vector<int> a){
    printf("hello world!\n");
    char judgeFIFO[] = "FIFO.fifo";
    mkfifo(judgeFIFO, 04755);
    int fd = open(judgeFIFO, O_RDWR);
    write(fd, "FIFO_TEST_DATA", sizeof("FIFO_TEST_DATA"));
    char rdata[15];
    read(fd, rdata, 9);
    printf("read %s\n", rdata);

    //std::vector<int> a;
    a.push_back(111);
    printf("vector: %d\n", a[0]);
}

int Do6(int tempValue, int id, int fdR, int fdW, int p[], int count, int key, char index)
{
	char OurBuf[buffSize];
	tempValue = 0;
	while(1)
	{
		read(fdR, OurBuf, 1);
		if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
			break;
		else
			tempValue = tempValue * 10 + (OurBuf[0] - '0');
	}
	//printf("in game, C: id = %d, in6 = %d\n",id , tempValue);
			
	int ind = 0;
	int i, j;
	for(i = 0;i<count;i++)
	{
		if(p[i] == tempValue)
		{
			for(j = i;j<count-1;j++)
				p[j] = p[j+1];
			count = count - 1;
			ind = 1;
			break;
		}
	}
	if(ind == 0)
	{
		p[count] = tempValue;
		count = count + 1;
	}
	sprintf(OurBuf, "%c %d %d\n",index, key, ind);
	write(fdW, OurBuf, strlen(OurBuf));
	
	return count;
}
int main(int argc, char *argv[])
{

	char OurBuf[buffSize];
	int	temp[14];
	//TODO: collect j_id + player index + rand key
	int j_id = 0;
	int key = 0;
	int id, i, count, j, pick, ind, n;
	int len = strlen(argv[1]);
	for(i = 0;i<len;i++)
		j_id = j_id * 10 + (argv[1][i] - '0');
	if(argv[2][0] - 'A' == 0)
		id = 0;
	else if(argv[2][0] - 'B' == 0)
		id = 1;
	else if(argv[2][0] - 'C' == 0)
		id = 2;
	else 
		id = 3;
	len = strlen(argv[3]);
	for(i = 0;i<len;i++)
		key = key * 10 + (argv[3][i] - '0');
	
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
	
	int fdW = open(judgeFIFO, O_RDWR);
	int fdR;
	if(id == 0)
		fdR = open(judgeAFIFO, O_RDWR);
	else if(id == 1)
		fdR = open(judgeBFIFO, O_RDWR);
	else if(id == 2)
		fdR = open(judgeCFIFO, O_RDWR);
	else if(id == 3)
		fdR = open(judgeDFIFO, O_RDWR);
	
	int p[4][14];
	int tempValue[6][3];
	char index[4];
	index[0] = 'A'; index[1] = 'B';index[2] = 'C';index[3] = 'D';
	if(id == 0)
	{
		//TODO: C, eat initial cards
		for(i = 0;i<14;i++)
			p[0][i] = 0;
		for(i = 0;i<14;i++)
		{
			while(1)
			{
				read(fdR, OurBuf, 1);
				if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
					break;
				else
					p[0][i] = p[0][i] * 10 + (OurBuf[0] - '0');
			}
		}
		//TODO: C, organize cards
		for(i = 0;i<14;i++)
			temp[i] = p[0][i];
		for(i = 0;i<14;i++)
		{
			if(temp[i] != -1)
			{
				count = 0;
				for(j = i+1; j<14;j++)
				{
					if(temp[i] == temp[j])
					{
						temp[i] = -1;
						temp[j] = -1;
					}
				}
			}
		}
			
		count = 0;
		for(i = 0;i<14;i++)
			if(temp[i] != -1)
			{
				p[0][count] = temp[i];
				count = count + 1;
			}

		//TODO: return card num on hands
		sprintf(OurBuf, "%c %d %d\n",index[id] ,key, count);
		write(fdW, OurBuf, strlen(OurBuf));
	}
	else
	{
		//TODO: C, eat initial cards
		for(i = 0;i<13;i++)
			p[0][i] = 0;
		for(i = 0;i<13;i++)
		{
			while(1)
			{
				read(fdR, OurBuf, 1);
				if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
					break;
				else
					p[0][i] = p[0][i] * 10 + (OurBuf[0] - '0');
			}
		}
		//TODO: C, organize cards
		for(i = 0;i<13;i++)
			temp[i] = p[0][i];
		for(i = 0;i<13;i++)
		{
			if(temp[i] != -1)
			{
				count = 0;
				for(j = i+1; j<13;j++)
				{
					if(temp[i] == temp[j])
					{
						temp[i] = -1;
						temp[j] = -1;
					}
				}
			}
		}
			
		count = 0;
		for(i = 0;i<13;i++)
			if(temp[i] != -1)
			{
				p[0][count] = temp[i];
				count = count + 1;
			}

		//TODO: return card num on hands
		sprintf(OurBuf, "%c %d %d\n",index[id] ,key, count);
		write(fdW, OurBuf, strlen(OurBuf));
		//printf("j_id = %d, id = %d, key = %d, count = %d\n", j_id, id, key, count);
	}
	
	//TODO: C, in game
	while(1)
	{
		tempValue[0][0] = 0;				
		while(1)
		{
			read(fdR, OurBuf, 1);
			if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
				break;
			else if(OurBuf[0] - '<' == 0)//i.e. then Do2 and Do6
				ind = 2;
			else if(OurBuf[0] - '>' == 0)//i.e. then Do4
				ind = 4;
		}

		if(ind == 2)
		{
			//2
			tempValue[0][0] = 0;
			while(1)
			{
				read(fdR, OurBuf, 1);
				if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
					break;
				else
					tempValue[0][0] = tempValue[0][0] * 10 + (OurBuf[0] - '0');
			}
			pick = ((rand()/(id+1)) % tempValue[0][0]) + 1;	
			sprintf(OurBuf, "%c %d %d\n",index[id] ,key ,pick);
			write(fdW, OurBuf, strlen(OurBuf));
					
			//6
			count = Do6(tempValue[0][0], id, fdR, fdW, p[0], count, key, index[id]);
		}
		else if(ind == 4)
		{
			//4
			tempValue[0][0] = 0;
			while(1)
			{
				read(fdR, OurBuf, 1);
				if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
					break;
				else
					tempValue[0][0] = tempValue[0][0] * 10 + (OurBuf[0] - '0');
			}
			sprintf(OurBuf, "%c %d %d\n",index[id] ,key, p[0][tempValue[0][0] - 1]);
			write(fdW, OurBuf, strlen(OurBuf));
	
			for(j = tempValue[0][0] - 1;j<count-1;j++)
				p[id][j] = p[id][j+1];
			count = count - 1;
		}
	}
	exit(0);
}
