#ifndef IPC_H
#define IPC_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct ipc_context_t* ipc_context;

/**
 * Creates a new IPC context bound to the given address and starts listening
 * for connections from clients.
 *
 * Returns NULL if there is an error.
 */
ipc_context ipc_bind(void);

/**
 * Creates a new IPC context connected to a given address, ready to send
 * requests to the server.
 *
 * Returns NULL if there is an error connecting.
 */
ipc_context ipc_connect(void);

/**
 * Closes all communications through a given IPC context.
 */
void ipc_close(ipc_context context);

/**
 * Sends a message from a client process to the daemon.
 */
int ipc_send(ipc_context ctx, const char* message);

/**
 * Sends a message from the daemon to a specific client.
 */
int ipc_reply(ipc_context ctx, const char* identity, const char* message);

/**
 * Receives a message from the socket.
 *
 * It is the caller's responsibility to `free` the returned string.
 */
char* ipc_receive(ipc_context ctx);

#ifdef __cplusplus
}
#endif

#endif
