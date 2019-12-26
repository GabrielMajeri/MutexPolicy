#ifndef MPOLICY_H
#define MPOLICY_H

// To make this header file compatible with C++, all declarations have to be
// wrapped inside an `extern "C" {}` block.
#ifdef __cplusplus
extern "C" {
#endif


/// Opaque handle, uniquely identifies a mutex.
typedef int mutex_t;

/// This is returned when creating a mutex fails,
/// and `errno` is set appropiately.
#define INVALID_MUTEX ((mutex_t)-1)


mutex_t mutex_open(const char* name);

void mutex_close(mutex_t);


#ifdef __cplusplus
}
#endif

#endif
