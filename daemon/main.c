#include <stdio.h>
#include "ipc.h"

int main() {
    printf("Hello from daemon!\n");

    ipc_test();

    return 0;
}
