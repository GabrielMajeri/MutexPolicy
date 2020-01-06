#include "mpolicy.h"
#include <ipc.h>

#include <errno.h>
#include <stdio.h>

mutex_t mutex_open(const char* name) {
    printf("Mutex open %s\n", name);

    // ENOSYS = Function not implemented
    errno = ENOSYS;

    return INVALID_MUTEX;
}

void mutex_close(mutex_t mutex) {
    printf("Mutex close %d\n", mutex);

    errno = ENOSYS;
}
