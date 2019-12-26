#include "ipc.h"
#include <stdio.h>
#include <unistd.h>

void ipc_test() {
    printf("IPC library called from process %d\n", getpid());
}
