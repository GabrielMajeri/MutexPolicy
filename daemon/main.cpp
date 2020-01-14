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
#include <zmq.hpp>

#define NU_MUTEX "nu exista bo$$"

using namespace std;

struct my_mutex{
	string boss = NU_MUTEX;
	set<string> procese;
	queue<string> coada;
};

map<string, my_mutex> mutecsi;

int main() {
	/*
	zmq::context_t context(1);
	zmq::socket_t broker(context, ZMQ_ROUTER);

	broker.bind("tcp://*:5555");

	std::string identity = broker.;
	s_recv(broker);
	s_recv(broker);

	s_sendmore(broker, identity);
	s_sendmore(broker, "");
	s_send(broker, "OK nu stiu");
	*/

    printf("Hello from daemon!\n");

    ipc_context ctx = ipc_bind();
    assert(ctx);

    printf("Daemon bound to IPC\n");
	
	while (1) {
		char * nume_client = ipc_receive(ctx);
		free(ipc_receive(ctx));
		char * msg = ipc_receive(ctx);

		string nume_mutex = msg+1;

		cout << "Toni e in pc meu " << nume_client << endl;

		my_mutex &m = mutecsi[nume_mutex];

		if(msg[0] == 'O') {
			//deschid mutex idk
			//sa verific daca nu exista deja in vecotr
			cout << "Toni incearca sa faca Open" << endl;
			if(m.procese.count(nume_client) > 0){
				//Verifica daca ai fost de 2 ori acolo si nu ai dat close inainte adica acolo in acel proceso
				cout << "A intrat acolo 74"<< endl;
				while(ipc_send(ctx, "NU E OK", 0) == 0){
					perror("N-am putut trimite");
				}
			}
			else{	
				m.procese.insert(nume_client);
				ipc_send(ctx, nume_client, 1);
				ipc_send(ctx, "", 1);
				while(ipc_send(ctx, "OK", 0) == 0){
					perror("Tot nu am putut trimite");
				}
			}
		}
		if(msg[0] == 'C') {
			if(m.procese.count(nume_client) > 0){
				m.procese.erase(nume_client);
				ipc_send(ctx, "S-A STERS", 0);
			}
			else{
				ipc_send(ctx, "UITA-TE LA AL PACINO <3", 0);
			}
		}
		if(msg[0] == 'L') {
			if(m.procese.count(nume_client)) { // >0
				if(m.boss == NU_MUTEX){
					ipc_send(ctx, "E AL TAU BO$$", 0);
				}					
				else{
					m.coada.push(nume_client);
				}
			}
			else{
				ipc_send(ctx, "UITA-TE LA AL PACINO <3", 0);
			}
		}

		if(msg[0] == 'U') {
			if(m.procese.count(nume_client)) { // >0
				if(m.boss == nume_client){
					ipc_send(ctx, "AI DAT UNLOCK BO$$", 0);
					string urmatorul_guy = m.coada.front();
					m.coada.pop();
					m.boss = urmatorul_guy;
					ipc_send(ctx, "E AL TAU BO$$", 0);
				}					
				else{
					ipc_send(ctx, "UITA-TE LA AL PACINO <3", 0);	
				}
			}
			else{
				ipc_send(ctx, "UITA-TE LA AL PACINO <3", 0);
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
