# NetworkTangents

A set of python libraries, code examples for Network Engineers to interact with Network Devices; CLI style.

**exa001connect.py** : Example 001, connect, shows how to connect to a Network Device using telnet and ssh. More details here: http://littletechnicalities.com/networktangents-exa001connect/

**exa010shint.py** : Example 010, show interfaces on steroids, collects "show interfaces status" and others related commands to show an extended version of "show interfaces status".more can be found here http://littletechnicalities.com/networktangents-exa010shint/

**exa020ios-rev** : Example 020, ios revision, checks that a list of devices (ideally same model), have a given ios installed, and/or have spare space to store it. It connects to all the devices on the list to check the IOS version of it or of the stack members if the switch the made of a stack.
This script needs 2 files in the parent directory as follow:
"exa020ios-rev-devices.txt" ; text file containing the devices names, one per line.
"exa020ios-rev-model-to-ios.tx"; text file containing:switch model, ios name, ios size(in bytes); separate by comma,
which ios you wish to review on each model as below
WS-C3750X-24P, c3750e-ipbasek9-mz.150-2.SE9.bin, 20430848

**exa030shut-int.py** : Example 030, shutdown interfaces, it would shutdown interfaces that haven't been use in the last 3 Months.

**exa101wrebunreac.py** : Example 101, wireless reboot unreachable; it would connect to "Prime" using its API to find out which wireless access points are on an unreachable state, it would take the details of the switch connected to, name and interface; then it would connect to each switch and reset the specific interface.


This project was created to easy the learning curve of Network Engineers to Devops, as the examples give the general idea that it was intend to, progress on this project would concluded at the end of 2017.

All the best,

Sergio. 
