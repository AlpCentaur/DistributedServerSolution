# saved as greeting-client.py
import Pyro4
import serpent
import subprocess

arr = []

GameShop = Pyro4.Proxy("PYRONAME:example.greeting") # use name server object lookup uri shortcut


print 'This are the items you can order in our Gameshop'
print
print GameShop.ListProducts()

done = False

while done == False:
    ordarr = []
    ID = int(raw_input('Please Type in your Costumer ID NR:'))
    
    for i in xrange(3):
        ordarr.append(raw_input('Please type in the {0} item you want to place in your order:'.format(i+1)))
    
    
    IDbin = serpent.dumps(ID)                            
    ordarraybin = serpent.dumps(ordarr)                        #use serpent instead of pickle, because its safer
        
    print'You placed an order!! Your Order History is now:'
    GameShop.PlacingOrder(IDbin,ordarraybin)
    #print GameShop.ListOrders(ID)
    print GameShop.AllOrderPrint()
    
    Cancelarr = []
    
    
    Cancelarr.append(raw_input('If you want to cancel an item in your order history, type it in, otherwise just push enter:'))

    Cancelitembin = serpent.dumps(Cancelarr)
    
    
    
    GameShop.CancellingOrder(IDbin, Cancelitembin)
    
    print'Your Order History is now:'
    print GameShop.AllOrderPrint()
    
    Quit = int(raw_input('Please Type in 1 to place next order or 0 to quit:'))
    if Quit == 0:
        done = True
        