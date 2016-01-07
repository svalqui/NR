# NetworkTangents

A set of python libraries, code examples for Network Engineers to interact with Network Devices; CLI style.

exa010shint.py : Example 010, show interfaces on steroids, collects "show interfaces status" and others commands to show an extended version of sh int status.

netdef.py : Class definitions for Network devices

netconfigparser.py : library of text manipulation, to review Network Devices' output, do some processing and return more workable structures

libnetservices.py : A library to connect with Network devices, ssh using Paramiko

test* : test files are concoction pots; will be deleted... eventually.

Requirements:
Python3.3 or above
Paramiko 1.15.2 https://github.com/paramiko/paramiko
Netmiko 0.2.6 https://github.com/ktbyers/netmiko
