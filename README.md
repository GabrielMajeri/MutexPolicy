# Mutex Policy

This repository contains the code for our team's project,
as part of the Operating Systems course at FMI UniBuc.

## Building

The project is primarily written in C/C++, and built using a Makefile.


To compile the project:

```sh
make build
```

To start the mutex policy daemon:

```sh
make run-daemon
```

To run a demo application which uses the library:

```sh
make run-demo
```

## Installing ZeroMQ

The code relies on the [ZeroMQ](https://zeromq.org/) messaging library
for inter-process communication. In order to get the project to build,
you will have to install the ZMQ development headers.

This can be done in a painless way on Linux:

### ArchLinux

```sh
sudo pacman -S zeromq
```

### Ubuntu/Debian

```sh
sudo apt install libzmq3-dev
```
