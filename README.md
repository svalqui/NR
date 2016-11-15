# NetworkTangents

A set of python libraries, code examples for Network Engineers to interact with Network Devices; CLI style.

**exa010shint.py** : Example 010, show interfaces on steroids, collects "show interfaces status" and others related commands to show an extended version of "show interfaces status".more can be found here http://littletechnicalities.weebly.com/show-interfaces-status-on-steroids.html

**exa020ios-rev** : Example 020, ios revision, checks that a list of devices (ideally same model), have a given ios installed, and/or have spare space to store it.

**exa030shut-int.py** : Example 030, shutdown interfaces, it would shutdown interfaces that haven't been use in the last 3 Months.

**exa101wrebunreac.py** : Example 101, wireless reboot unreachable; it would connect to "Prime" using its API to find out which wireless access points are on an unreachable state, it would take the details of the switch connected to, name and interface; then it would connect to each switch and reset the specific interface.

**libnetconparser.py** : Library of text manipulation, to review Network Devices' output, do some processing and return more workable structures.

**libfilesio.py** : Library to manage text files, to read/write them




####Requirements:
Python3.5 or above
Netmiko 0.4.3
