import socket
import struct
import sys
import serpent
import numpy as np
import Pyro4


multicast_group = '224.3.29.71'
server_address = ('', 12009)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)


# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

GameShop = Pyro4.Proxy("PYRONAME:server.prime") # use name server object lookup uri shortcut
GameShopBackup1 = Pyro4.Proxy("PYRONAME:backupserver.one") # use name server object lookup uri
GameShopBackup2 = Pyro4.Proxy("PYRONAME:backupserver.two")
# Receive/respond loop
while True:
    print >>sys.stderr, '\nwaiting to receive message'
    rawsentence, address = sock.recvfrom(1024)
    arr = serpent.loads(rawsentence)
    
    
    print >>sys.stderr, 'received %s bytes from %s' % (len(arr), address)
    print >>sys.stderr, arr
    
    if arr[0] == 1:
        
        try:
            
            
            GameShop.PlacingOrder(serpent.dumps(arr[1]),serpent.dumps(arr[2]))
            newarr = GameShop.AllOrderPrint()
            
        except:
            
            try:
                GameShopBackup1.PlacingOrder(serpent.dumps(arr[1]),serpent.dumps(arr[2]))
                newarr = GameShopBackup1.AllOrderPrint()
                
            except:
                
                try:
                    GameShopBackup2.PlacingOrder(serpent.dumps(arr[1]),serpent.dumps(arr[2]))
                    newarr = GameShopBackup2.AllOrderPrint()
                    
                except:
                    pass
       
        
    if arr[0] == 2:
        
        try:
            GameShop.CancellingOrder(serpent.dumps(arr[1]),serpent.dumps(arr[2]))
            newarr = GameShop.AllOrderPrint()
           
        except:
            
            try:
                GameShopBackup1.CancellingOrder(serpent.dumps(arr[1]),serpent.dumps(arr[2]))
                newarr = GameShopBackup1.AllOrderPrint()
                
            except:
                
                try:
                    GameShopBackup2.CancellingOrder(serpent.dumps(arr[1]),serpent.dumps(arr[2]))
                    newarr = GameShopBackup2.AllOrderPrint()
                    
                except:
                    pass
                    
        
        
        
    #capitalizedSentence = sentence.upper()
    newarrsend = serpent.dumps(newarr)
    
    print >>sys.stderr, 'sending updated History to', address
    sock.sendto(newarrsend, address)
