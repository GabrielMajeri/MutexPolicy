# Mutex Policy

This repository contains the code for our team's project,
as part of the Operating Systems course at FMI UniBuc.

## Running

The project is primarily written in Python. It 

The code relies on the [ZeroMQ](https://zeromq.org/) messaging library
for inter-process communication.

To install the ZeroMQ bindings for Python do:
```sh
pip3 install pyzmq
```

First, start the daemon by running:
```sh
cd daemon && python3 main.py
```

You can then run the included sample applications by doing:
```sh
cd demo && python3 test.py
```

The client library for communicating with the mutex is [included with the apps](demo/mpolicy.py).

## Authors

- [Antonia Biro](https://github.com/ToniBiro)
- [Bogdan Gavril](https://github.com/bogdangvr)
- [Bogdan Nițică](https://github.com/BogdanNitica99)
- [Gabriel Majeri](https://github.com/GabrielMajeri)
