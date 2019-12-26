#include "mpolicy.h"
#include <ipc.h>

#include <errno.h>

mutex_t mutex_open(const char* name) {
    ipc_test();

    // ENOSYS = Function not implemented
    errno = ENOSYS;

    return INVALID_MUTEX;
}

void mutex_close(mutex_t mutex) {
    errno = ENOSYS;
}
