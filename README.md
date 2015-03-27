# daryl
Set of tools and best practices for detecting and getting rid of dead code


## deadgargoyle

Simple Django management command to determine which Gargoyle switches have not been touched for ages and are either completely disabled or globally enabled, thus code can be simplified to get rid of feature flags.


## fopen-shim

Small bit of C code to shim fopen() and open() syscalls on Linux, logging each call to syslog.
Intended to be used with LD_PRELOAD


## deadfunctions

Tools to determine if given function is dead.

