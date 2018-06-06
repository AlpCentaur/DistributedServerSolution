# saved as greeting-server.py
import Pyro4
import serpent

GameShopB1 = Pyro4.Proxy("PYRONAME:backupserver.one")
GameShopB2 = Pyro4.Proxy("PYRONAME:backupserver.two")


#
# Here the update is made, if the server fails and gets into work directly


try:
    All = GameShopB2.AllOrderPrint() 
except:
    print 'Failed: PgetB2'
try:
    All = GameShopB1.AllOrderPrint()
except:
    print 'Failed: PgetB1'




@Pyro4.behavior(instance_mode="single")
@Pyro4.expose
class GameShop(object):
    def __init__(self):
        self.products = ['AgeOfEmpires', 'Tron', 'SuperMarioKart', 'ZombieApokalypse']
        self.AllOrders = All
        
        
        
    def ListProducts(self):
        return self.products
    
    def UpdateB1(self):
        
        self.AllOrders = GameShopB1.AllOrderPrint()
        
    
    def UpdateB2(self):
        
        self.AllOrders = GameShopB2.AllOrderPrint()
        
    
    def AllOrderPrint(self):
        return self.AllOrders
    
    def ListOrders(self,ID):
        for vektor in self.AllOrders:
            if vektor[0] == ID:
                List = vektor
        return List        
    
    def PlacingOrder(self, IDbin, OrdersBin):
        
        #
        # Here the update is made
        
        try:
            self.UpdateB2()
        except:
            print 'Failed: PgetB2'
        try:
            self.UpdateB1()
        except:
            print 'Failed: PgetB1'
        
        Orders = serpent.loads(OrdersBin)
        ID = serpent.loads(IDbin)
        
        count = 0
        for vektor in self.AllOrders:
            print vektor
            if vektor[0] == ID:
                for Order in Orders:
                    if Order in self.products:
                        vektor.append(Order)
                count =+ 1
        
        
        if count == 0:    
            NewCustom = []
            NewCustom.append(ID)
            for Order in Orders:
                if Order in self.products:
                    NewCustom.append(Order)
                
            self.AllOrders.append(NewCustom)
        
        #
        # Here the updated server is        
        try:
            GameShopB1.UpdateP() 
        except:
            print 'Failed: B1getP'
        try:
            GameShopB2.UpdateP()
        except:
            print 'Failed: B2getP'
        return serpent.dumps(self.AllOrders)
    
    def CancellingOrder(self, IDbin, OrdersBin):
        
        #
        # Here the update is made
        
        try:
            self.UpdateB1()
        except:
            print 'Failed: PBget1'
        try:
            self.UpdateB2()
        except:
            print 'Failed: PBget2'
        Orders = serpent.loads(OrdersBin)
        ID = serpent.loads(IDbin)
        
        
        count = 0
        for vektor in self.AllOrders:
            if vektor[0] == ID:
                
                for Order in Orders:
                    if Order in vektor:
                        
                        vektor.remove(Order)
                count =+ 1
        if count == 0:    
            return 'Sorry, you havent placed an order yet'
        try:
            GameShopB1.UpdateP()
        except:
            print 'Failed: B1P'
        try:
            GameShopB2.UpdateP()
        except:
            print 'Failed: B2P'
        return serpent.dumps(self.AllOrders)



daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GameShop)   # register the greeting maker as a Pyro object
ns.register("server.prime", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls

#if __name__ == '__main__':
    #GameShop = Pyro4.Proxy("PYRONAME:server.prime")
    #try:
        #Gameshop.UpdateB2()
    #except:
        #print 'Failed: PgetB2'
    #try:
        #Gameshop.UpdateB1()
    #except:
        #print 'Failed: PgetB1'
