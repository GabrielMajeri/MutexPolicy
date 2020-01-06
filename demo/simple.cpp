#include <iostream>
#include <mpolicy.h>


int main() {
    std::cout << "Hello from example app!\n";

    mutex_t my_mutex = mutex_open("some_mutex_name");
    if (my_mutex == INVALID_MUTEX) {
        perror("Failed to create mutex");
        return 1;
    }

    // TODO: do something with the mutex

    mutex_close(my_mutex);

    return 0;
}
