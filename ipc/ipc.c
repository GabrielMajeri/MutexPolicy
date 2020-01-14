#include "ipc.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <zmq.h>


#define MAX_MSG_LEN 256


struct ipc_context_t {
    void* context;
    void* socket;
};


static ipc_context init_context(int socket_type) {
    // Initialize the ZeroMQ context structure
    void* context = zmq_ctx_new();
    if (!context) {
        return NULL;
    }

    // Create a new ZMQ socket of the requested type
    void* socket = zmq_socket(context, socket_type);
    if (!socket) {
        zmq_ctx_destroy(context);
        return NULL;
    }

    // Allocate memory for the context structure and fill in its fields
    ipc_context ctx = (ipc_context)malloc(sizeof(struct ipc_context_t));

    ctx->context = context;
    ctx->socket = socket;

    return ctx;
}

static const char IPC_ADDRESS[] = "tcp://*:5555";

ipc_context ipc_bind(void) {
    // Router socket attaches an envelope which identifies the sender
    // of each message. This way it's able to reply back to each client
    // individually.
    //
    // See the documentation for an extended explanation on how it works:
    // http://zguide.zeromq.org/page:chapter3#The-Extended-Reply-Envelope
    ipc_context ctx = init_context(ZMQ_ROUTER);
    if (!ctx) {
        return NULL;
    }

    // Bind the socket to the common address,
    // waiting for connections from clients
    if (zmq_bind(ctx->socket, IPC_ADDRESS) != 0) {
        ipc_close(ctx);
        return NULL;
    }


    return ctx;
}

ipc_context ipc_connect(void) {
    ipc_context ctx = init_context(ZMQ_REQ);
    if (!ctx) {
        return NULL;
    }

    // Try to connect to the already-bound common address
    if (zmq_connect(ctx->socket, IPC_ADDRESS) != 0) {
        ipc_close(ctx);
        return NULL;
    }

    return ctx;
}

void ipc_close(ipc_context ctx) {
    int result;

    // First close the ZMQ socket
    result = zmq_close(ctx->socket);

    assert(result == 0);
    ctx->socket = NULL;

    // Now try cleaning up the ZMQ context
    result = 0;
    do {
        // While destroying the context, the app could be interrupted by a signal.
        // In that case we must call `zmq_ctx_destroy` again.
        result = zmq_ctx_destroy(ctx->context);
    } while (result == EINTR);

    assert(result == 0);
    ctx->context = NULL;

    // Finally, release the memory
    free(ctx);
}

int ipc_send(ipc_context ctx, const char* message, int flags) {

    return zmq_send_const(ctx->socket, message, strlen(message), flags?ZMQ_SNDMORE:ZMQ_NOBLOCK);
}



char* ipc_receive(ipc_context ctx) {
    char buf[MAX_MSG_LEN];
    int rc = zmq_recv(ctx->socket, buf, MAX_MSG_LEN, 0);
    if (rc == -1) {
        return NULL;
    } else {
        buf[rc] = 0;
        return strdup(buf);
    }
}
