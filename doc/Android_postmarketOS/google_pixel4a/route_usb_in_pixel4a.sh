# sudo to perform below
# usb connect, NAT to internet
# guide: https://wiki.postmarketos.org/wiki/USB_Internet
# ssh <user>@172.16.42.1
ip route add default via 172.16.42.2 dev usb0
echo nameserver 1.1.1.1 >> /etc/resolv.conf
route add default gw 172.16.42.2
