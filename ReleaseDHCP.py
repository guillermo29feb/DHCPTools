from scapy.all import *
import sys, getopt
import netifaces

def main(argv):

    ifaceList = netifaces.interfaces()
    serverIP="255.255.255.255"
    try:
        opts, args = getopt.getopt(argv,"hi:s:",["help","iface=","serverIP="])
    except getopt.GetoptError:
        print "ReleaseDHCP.py -i <interface> -s <serverIP> "
        print "Interfaces availables: " + str(ifaceList)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "  --> ReleaseDHCP.py [-i | --iface] <interface> [-s | --server] <serverIP> // default 'eth0'"
            print "  --> Interfaces availables: " + str(ifaceList)
            sys.exit()
        elif opt in ("-i", "--iface"):

            if str(argv[1]) in ifaceList:
                conf.iface = arg
                print arg
            else:
                print "Invalid interface. Interfaces availables: " + str(ifaceList)
                exit()
        elif opt in ("-s", "--server"):
            serverIP = arg
            print serverIP
        else:
            conf.iface = 'eth0' #Interface default eth0


    for ipaddres in netifaces.ifaddresses(conf.iface)[netifaces.AF_INET]:
        releaseIP = ipaddres['addr'] # get IP address
    for mac in netifaces.ifaddresses(conf.iface)[netifaces.AF_LINK]:
        releaseMAC = mac['addr'] # get MAC address


    releaseMACraw = releaseMAC.replace(':','').decode('hex')
    ip = IP(src="0.0.0.0", dst=serverIP)#(dst=serverIP)
    udp = UDP(sport=68,dport=67)
    bootp = BOOTP(chaddr=releaseMACraw,ciaddr=releaseIP,xid=111) #RandInt())
    dhcp = DHCP(options=[('message-type','release'),'end'])
    dhcp_release = ip/udp/bootp/dhcp
    dhcp_release.show()
    send(dhcp_release)

if __name__ == "__main__":
    main(sys.argv[1:])