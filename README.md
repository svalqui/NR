# NetworkTangents

A set of python libraries, code examples for Network Engineers to interact with Network Devices; CLI style.

**exa010shint.py** : Example 010, show interfaces on steroids, collects "show interfaces status" and others related commands to show an extended version of "show interfaces status".more can be found here http://littletechnicalities.weebly.com/show-interfaces-status-on-steroids.html

**exa020ios-rev** : Example 020, ios revision, checks that a list of devices (ideally same model), have a given ios installed, and/or have spare space to store it.

**netdef.py** : Class definitions for Network devices.

**libnetconparser.py** : Library of text manipulation, to review Network Devices' output, do some processing and return more workable structures.

**libfilesio.py** : Library to manage text files, to read/write them

libnetservices.py : A library to connect with Network devices, ssh using Paramiko.

test* : test files are concoction pots; will be deleted... eventually.

####Requirements:
Python3.5 or above
Netmiko 0.4.3
