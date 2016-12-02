#!/usr/bin/python
from unifi.controller import Controller
import subprocess

###############################
#Change me here for where to send email and what controller to connect to

recipient = 'XXXXX@XXXXX.com'
subject = 'Address blocked on Unifi Controller'

c = Controller('127.0.0.1', '<username>', '<password>', '<port>', '<version>')

###############################
################################
#Define the empty variable
body="The following addresses were blocked because they were not on the allowed list:"

def send_message(recipient, subject, body):
    try:
      process = subprocess.Popen(['mail', '-s', subject, recipient],
                               stdin=subprocess.PIPE)
    except Exception, error:
      print error
    process.communicate(body)


#Create the empty list that will be used for our connected clients
connectedlist = list()
allowed = list()

#Create a list of the current mac addresses.
for mac in c.get_clients():
    connectedlist.append(mac['mac'])

#Read in the mac list and remove the # characters so you can comment the mac addresses
with open('/usr/local/src/maclist.txt') as f:
        for line in f:
                line = line.partition('#')[0]
                line = line.rstrip()
                allowed += line.splitlines()

#Print a list of the known mac addresses.
print "The connected addresses to the AP are the following:"
for conn in connectedlist: print conn

print "The allowed mac addresses are as follows:"
for a in allowed: print a

#Compare the list of addresses from what is connected vs what is allowed.
s = set(allowed)
blockme = [x for x in connectedlist if x not in s]

if not blockme:
    print "All addresses matched the allowed list.  There are no addresses to block."
    print "Goodbye."
else:
    print "I am going to block the following addresses."
    for b in blockme: print b
    #Run through the list and block all the addresses that didn't match the allowed mac addresses.
    for mac in blockme:
        #Command to block an address.
        #DEBUG BLOCK HERE
    c.block_client(mac)
        #
    print "Block complete for the following address:"
        print mac
    body += "\n"
    body += mac
    send_message(recipient, subject, body)
    print("Email sent of blocked addresses")

