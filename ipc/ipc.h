#ifndef IPC_H
#define IPC_H

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

#endif
