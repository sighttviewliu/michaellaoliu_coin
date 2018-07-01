Michaellaoliu Core
=============

Setup
---------------------
Michaellaoliu Core is the original Michaellaoliu client and it builds the backbone of the network. It downloads and, by default, stores the entire history of Michaellaoliu transactions (which is currently more than 100 GBs); depending on the speed of your computer and network connection, the synchronization process can take anywhere from a few hours to a day or more.

To download Michaellaoliu Core, visit [michaellaoliucore.org](https://michaellaoliucore.org/en/releases/).

Running
---------------------
The following are some helpful notes on how to run Michaellaoliu on your native platform.

### Unix

Unpack the files into a directory and run:

- `bin/michaellaoliu-qt` (GUI) or
- `bin/michaellaoliud` (headless)

### Windows

Unpack the files into a directory, and then run michaellaoliu-qt.exe.

### OS X

Drag Michaellaoliu-Core to your applications folder, and then run Michaellaoliu-Core.

### Need Help?

* See the documentation at the [Michaellaoliu Wiki](https://en.michaellaoliu.it/wiki/Main_Page)
for help and more information.
* Ask for help on [#michaellaoliu](http://webchat.freenode.net?channels=michaellaoliu) on Freenode. If you don't have an IRC client use [webchat here](http://webchat.freenode.net?channels=michaellaoliu).
* Ask for help on the [MichaellaoliuTalk](https://michaellaoliutalk.org/) forums, in the [Technical Support board](https://michaellaoliutalk.org/index.php?board=4.0).

Building
---------------------
The following are developer notes on how to build Michaellaoliu on your native platform. They are not complete guides, but include notes on the necessary libraries, compile flags, etc.

- [Dependencies](dependencies.md)
- [OS X Build Notes](build-osx.md)
- [Unix Build Notes](build-unix.md)
- [Windows Build Notes](build-windows.md)
- [OpenBSD Build Notes](build-openbsd.md)
- [Gitian Building Guide](gitian-building.md)

Development
---------------------
The Michaellaoliu repo's [root README](/README.md) contains relevant information on the development process and automated testing.

- [Developer Notes](developer-notes.md)
- [Release Notes](release-notes.md)
- [Release Process](release-process.md)
- [Source Code Documentation (External Link)](https://dev.visucore.com/michaellaoliu/doxygen/)
- [Translation Process](translation_process.md)
- [Translation Strings Policy](translation_strings_policy.md)
- [Travis CI](travis-ci.md)
- [Unauthenticated REST Interface](REST-interface.md)
- [Shared Libraries](shared-libraries.md)
- [BIPS](bips.md)
- [Dnsseed Policy](dnsseed-policy.md)
- [Benchmarking](benchmarking.md)

### Resources
* Discuss on the [MichaellaoliuTalk](https://michaellaoliutalk.org/) forums, in the [Development & Technical Discussion board](https://michaellaoliutalk.org/index.php?board=6.0).
* Discuss project-specific development on #michaellaoliu-core-dev on Freenode. If you don't have an IRC client use [webchat here](http://webchat.freenode.net/?channels=michaellaoliu-core-dev).
* Discuss general Michaellaoliu development on #michaellaoliu-dev on Freenode. If you don't have an IRC client use [webchat here](http://webchat.freenode.net/?channels=michaellaoliu-dev).

### Miscellaneous
- [Assets Attribution](assets-attribution.md)
- [Files](files.md)
- [Fuzz-testing](fuzzing.md)
- [Reduce Traffic](reduce-traffic.md)
- [Tor Support](tor.md)
- [Init Scripts (systemd/upstart/openrc)](init.md)
- [ZMQ](zmq.md)

License
---------------------
Distributed under the [MIT software license](/COPYING).
This product includes software developed by the OpenSSL Project for use in the [OpenSSL Toolkit](https://www.openssl.org/). This product includes
cryptographic software written by Eric Young ([eay@cryptsoft.com](mailto:eay@cryptsoft.com)), and UPnP software written by Thomas Bernard.
