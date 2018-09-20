# ipfs-demo
A offline, mesh-networking demo of IPFS, originally for use by tomesh.net

**WIP**

## Notes

* Add nginx script so that it reverse proxies the flask server over IPv6 to port 80
* It will be on /demo - an index file or something will redirect there from /
* Install script involves importing demo key file
* It's assumed that nodes 1 and 2 are peered over IPFS, and have the daemon started already
* make /tmp/ipfs-demo folder as part of install
* install flask and flask-socketio, eventlet too - with sudo -H I guess
* Make it so the server doesn't have to respond to all the client requests at the same time

## Instead
* Look at https://cryptpad.fr/code/#/2/code/view/cNX1Y33NqcL2yuWWeaqfJ5H5UgGWQvmt-z+xwqXeYvs/
for instructions
* Also look through code for XXX, ie things to change
