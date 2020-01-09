#include <assert.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <syslog.h>
#include <string.h>
#include <map>
#include <vector>

#include <bits/stdc++.h>

#include "ipc.h"

#define NU_MUTEX "nu exista bo$$"

using namespace std;

struct my_mutex{
	string boss = NU_MUTEX;
	set<string> procese;
	queue<string> coada;
};

map<string, my_mutex> mutecsi;

int main() {
    printf("Hello from daemon!\n");

    ipc_context ctx = ipc_bind();
    assert(ctx);

    printf("Daemon bound to IPC\n");
	
	while (1) {
		char * nume_client = ipc_receive(ctx);
		free(ipc_receive(ctx));
		char * msg = ipc_receive(ctx);

		string nume_mutex = msg+1;

		my_mutex &m = mutecsi[nume_mutex];

		if(msg[0] == 'O') {
			//deschid mutex idk
			//sa verific daca nu exista deja in vecotr
			if(m.procese.count(nume_client) > 0){
				//Verifica daca ai fost de 2 ori acolo si nu ai dat close inainte adica acolo in acel proceso
				ipc_reply(ctx, nume_client, "NU E OK");
			}
			else{
				m.procese.insert(nume_client);
				ipc_reply(ctx, nume_client, "OK");
			}
		}
		if(msg[0] == 'C') {
			if(m.procese.count(nume_client) > 0){
				m.procese.erase(nume_client);
				ipc_reply(ctx, nume_client, "S-A STERS");
			}
			else{
				ipc_reply(ctx, nume_client, "UITA-TE LA AL PACINO <3");
			}
		}
		if(msg[0] == 'L') {
			if(m.procese.count(nume_client)) { // >0
				if(m.boss == NU_MUTEX){
					ipc_reply(ctx, nume_client, "E AL TAU BO$$");
				}					
				else{
					m.coada.push(nume_client);
				}
			}
			else{
				ipc_reply(ctx, nume_client, "UITA-TE LA AL PACINO <3");
			}
		}

		if(msg[0] == 'U') {
			if(m.procese.count(nume_client)) { // >0
				if(m.boss == nume_client){
					ipc_reply(ctx, nume_client, "AI DAT UNLOCK BO$$");
					string urmatorul_guy = m.coada.front();
					m.coada.pop();
					m.boss = urmatorul_guy;
					ipc_reply(ctx, urmatorul_guy.c_str(), "E AL TAU BO$$");
				}					
				else{
					ipc_reply(ctx, nume_client, "UITA-TE LA AL PACINO <3");	
				}
			}
			else{
				ipc_reply(ctx, nume_client, "UITA-TE LA AL PACINO <3");
			}
		}

		//daca a fost inchis de atatea ori de cate ori a fost deschis --mai tarziu, intai baza



		free(nume_client);
		free(msg);

		sleep(30); // wait 30 seconds
	}
	exit(EXIT_SUCCESS);

    ipc_close(ctx);

    return 0;
}
