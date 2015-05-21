//$./organizer j_num p_num
//Q: 怎樣可以複寫pipe ans: 無法, 要read掉
//Q: 為什麼原本的程式 run 下續就會block住? b.c. read 不到東西(which results from 對方沒把東西寫入)

//Rmk) 如果pipe的某一端被關掉, 但仍要做寫入, 會顯示broken pipe
//Rmk) 不要用: while((n = read[...]) != 0), 在pipe會出錯!!!
//如果有用STDlib, by fflush 把write的東西丟出去!!(b.c. fully buffered for standardio in pipe)
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <fcntl.h>
#include <sys/select.h>
//supp we have at most 1000 players
const int Maxsize = 1000000;
const int buffSize = 1000;
const char initOread[] = "1 1 1 1 1";
const char initOwrite[] = "1 1 1 1";
const char theEnd[] = "0 0 0 0";
struct joblist
{
	int value;
	int first, second, third, fourth;
};
typedef struct joblist Joblist;
int power(int base, int exp)
{
    int i;
    int ans = 1;
    for(i = 0;i<exp;i++)
          ans = ans * base;
    return ans;
}
Joblist NextJob(int n, int value, int min)
{
    int i, j;
    int ind[n];
    for(i = 0;i<n;i++)
		ind[i] = 0;
    for(i = 0;i<4;i++)
        ind[i] = 1;
	int temp, NumOfOne, count;
    value = value + power(2, min);
	
    //TODO: translate to count in 2
    for(i = 0;i<n;i++)
		ind[i] = 0;
    i = 0;
    NumOfOne = 0;
    temp = value;
    while(1)
    {
        if(temp == 1)
        {
            ind[i] = 1;
            NumOfOne = NumOfOne + 1; 
            break;  
        }
        if(temp % 2 == 1)
        {
            ind[i] = 1;
            NumOfOne = NumOfOne + 1; 
        }
        temp = temp / 2;
        i = i + 1;
    }
    //TODO: add more 1 if the ones in the representation are less than 4 ones
    Joblist job;
	
	if(ind[n-1] == ind[n-2] && ind[n-2] == ind[n-3] && ind[n-3] == ind[n-4] && ind[n-4] == 1)
	{
		job.first = n-4; 
		job.second = n-3; job.third = n-2; job.fourth = n-1;
	}
    else
    {
        for(i = 0;i < 4 - NumOfOne ;i++)
            ind[i] = 1;
        i = 0;
		count = 0;
		for(j = 0;j<4;j++)
		{
			count = count + 1;
			while(ind[i] != 1)
				i = i + 1;
			if(count == 1)
				job.first = i;
			else if(count == 2)
				job.second = i;
			else if(count == 3)
				job.third = i;
			else
				job.fourth = i;
			i = i + 1;
		}
    }
    //TODO: renew value
    value = 0;
    for(i = 0;i<n;i++)
		if(ind[i] == 1)
            value = value + power(2, i);
	job.value = value;
	return job;
}
int main(int argc, char *argv[])
{
	//TODO: collect j_num & p_num; i.e. judgenum and playernum
	int len, i, j, n;
	int j_num = 0;
	int p_num = 0;
	len = strlen(argv[1]);
	for(i = 0;i<len;i++)
		j_num = j_num * 10 + (argv[1][i] - '0');
	len = strlen(argv[2]);
	for(i = 0;i<len;i++)
		p_num = p_num * 10 + (argv[2][i] - '0');	
	
	int fd_Owrite[j_num][2];
	int fd_Oread[j_num][2];
	int pid[j_num];
	for(i = 0; i<j_num;i++)
		pid[i] = 0;
	char OurBuf[buffSize];
	int looserTable[p_num + 1], IhaveAjob[j_num];
	for(i = 0; i<p_num+1;i++)
		looserTable[i] = 0;
	for(i = 0;i<j_num;i++)
		IhaveAjob[i] = 0;
	int id = 0;
	//TODO: build pipe & fork, can use fd[i] to each connection btw parent and child i
	while(id<j_num)
	{
		pipe(fd_Oread[id]);
		pipe(fd_Owrite[id]);
		pid[id] = fork();

		if(pid[id]>0)
		{
			close(fd_Oread[id][1]);
			close(fd_Owrite[id][0]);
			id = id + 1;
		}
		else
		{
			close(fd_Oread[id][0]);
			close(fd_Owrite[id][1]);
			id = id + 1;
			break;
		}
	}
	id = id - 1;
	sleep(1);
	Joblist job;	job.value = 15;	job.first = 0;	job.second = 1;	job.third = 2;	job.fourth = 3;
	int rettemp[5];
	int current_job = 0;
	int final_job = p_num - 4;//by the use of job.first
	int getout = 0;
	fd_set readset;
	if(pid[id]>0)
	{
		write(fd_Owrite[0][1], "1 2 3 4\n", 8);
		IhaveAjob[0] = 1;
		
		while(getout != 1)
		{
			if(current_job == final_job)
			{
				for(i = 0;i < j_num;i++)
				{
					//TODO: write the end
					sprintf(OurBuf, "%s\n", theEnd);
					write(fd_Owrite[i][1], OurBuf, strlen(OurBuf));
				}
				//TODO: read unread
				n = 0;
				for(i = 0;i<j_num;i++)
					if(IhaveAjob[i] == 1)
						n = n + 1;
				for(i= 0;i<n;i++)
				{
					FD_ZERO(&readset);
					for(i = 0;i<j_num;i++)
						FD_SET(fd_Oread[i][0], &readset);
					select(fd_Oread[j_num - 1][0] + 1, &readset, NULL, NULL, NULL);
					for(i = 0;i<j_num;i++)
						if(FD_ISSET(fd_Oread[i][0], &readset))//some data write in from judge i
							break;
					rettemp[0] = 0;
					for(j = 0;j<1;j++)
					{
						while(1)
						{
							read(fd_Oread[i][0], OurBuf, 1);
							if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
								break;
							else
								rettemp[j] = rettemp[j] * 10 + (OurBuf[0] - '0');
						}
					}
					looserTable[rettemp[0]] = looserTable[rettemp[0]] - 1;
				}
				getout = 1;
					//break;
			}
			else
			{
				//TODO: select fd(i.e. fd with read data available) to write new job
				FD_ZERO(&readset);
				for(i = 0;i<j_num;i++)
					FD_SET(fd_Oread[i][0], &readset);
					
				select(fd_Oread[j_num - 1][0] + 1, &readset, NULL, NULL, NULL);
				for(i = 0;i<j_num;i++)
					if(FD_ISSET(fd_Oread[i][0], &readset))//some data write in from judge i
						break;
					
				//TODO: write new job
				job = NextJob(p_num, job.value, job.first);
				sprintf(OurBuf, "%d %d %d %d\n", job.first+1, job.second+1, job.third+1, job.fourth+1);
				write(fd_Owrite[i][1], OurBuf, strlen(OurBuf));
				IhaveAjob[i] = 1;
					
				current_job = job.first;
				//TODO: read return data
				rettemp[0] = 0;
				for(j = 0;j<1;j++)
				{
					while(1)
					{
						read(fd_Oread[i][0], OurBuf, 1);
						if(OurBuf[0] - '\n' == 0 || OurBuf[0] - ' ' == 0)
							break;
						else
							rettemp[j] = rettemp[j] * 10 + (OurBuf[0] - '0');
					}
				}
				looserTable[rettemp[0]] = looserTable[rettemp[0]] - 1;
			}
		}
		for(i = 0;i<p_num;i++)
			looserTable[i] = looserTable[i+1];
		n = p_num;
		int c, d, swap;
		int winnerOrder[p_num];
		for(i = 0;i<p_num;i++)
			winnerOrder[i] = i+1;
		for (c = 0 ; c < ( n - 1 ); c++)
		{
			for (d = 0 ; d < n - c - 1; d++)
			{
				if (looserTable[d] > looserTable[d+1]) /* For decreasing order use < */
				{
					swap       = looserTable[d];
					looserTable[d]   = looserTable[d+1];
					looserTable[d+1] = swap;
					swap       = winnerOrder[d];
					winnerOrder[d]   = winnerOrder[d+1];
					winnerOrder[d+1] = swap;
					
				}
			}
		}
		for ( c = 0 ; c < n ; c++ )
			printf("%d ", winnerOrder[c]);
		printf("\n");
	}
	else
	{
		dup2(fd_Owrite[id][0],STDIN_FILENO);
		dup2(fd_Oread[id][1],STDOUT_FILENO);
		sprintf(OurBuf, "%d", id+1);
		execlp("./judge", "./judge", OurBuf, (char*)0);
	}
	exit(0);
}