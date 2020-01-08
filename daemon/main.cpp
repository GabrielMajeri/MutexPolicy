#include <assert.h>
#include <stdio.h>

#include "ipc.h"

int main() {
    printf("Hello from daemon!\n");

    ipc_context ctx = ipc_bind();
    assert(ctx);

    printf("Daemon bound to IPC\n");

    ipc_close(ctx);

    return 0;
}
