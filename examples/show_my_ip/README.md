# Show My Ip 

This is a useful service that will display your current IP address (either from your Wifi connection, or your Ethernet port) every 10 seconds. 

To install it run:

`sh ip_at_boot.sh`

This will install the appropriate service for you.

Caveat:
this is a simple implementation that requires an internet connection to figure out the IP address. If you are connecting to a router that does not provide an internet connection, it will not work.
