from scapy.all import *
import sys, getopt
import netifaces

def main(argv):
    ifaceList = netifaces.interfaces()
    try:
        opts, args = getopt.getopt(argv,"hi:",["iface="])
    except getopt.GetoptError:
        print "IdentifyingRogueServer.py -i <interface>"
        print "Interfaces availables: " + str(ifaceList)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "  --> IdentifyingRogueServer.py [-i | --iface] <interface> // default 'eth0'"
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

    fam,hw = get_if_raw_hwaddr(conf.iface)
    print "Interface: " + conf.iface
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0",dst="255.255.255.255")
    udp = UDP(sport=68,dport=67)
    bootp = BOOTP(chaddr=hw)
    dhcp = DHCP(options=[("message-type","discover"),"end"])
    dhcp_discover = ether/ip/udp/bootp/dhcp
    print """
    ***                                           ***
    *** Push Ctrl+C to stop after several seconds ***
    ***                                           ***
    """
    ans, unans = srp(dhcp_discover, multi=True) # send and receive packet

    ans.summary()

    for servers in ans: print servers[1][Ether].src, servers[1][IP].src
    print "Servers identified: " + str(len(ans))


if __name__ == "__main__":
    main(sys.argv[1:])