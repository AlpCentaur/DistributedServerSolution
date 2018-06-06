# saved as greeting-server.py
import Pyro4
import serpent


GameShopPrime = Pyro4.Proxy("PYRONAME:server.prime") # use name server object lookup uri shortcut
GameShopB2 = Pyro4.Proxy("PYRONAME:backupserver.two")



@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class GameShop(object):
    def __init__(self):
        self.products = ['AgeOfEmpires', 'Tron', 'SuperMarioKart', 'ZombieApokalypse']
        self.AllOrders = []
        
    def ListProducts(self):
        return self.products
    
    def UpdateP(self):
        state = 1
        try:
            self.AllOrders = GameShopPrime.AllOrderPrint()
        except:
            state = 0
        return state
        
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
        try:
            self.UpdateP()
        except:
            pass
        try:
            self.UpdateB2()
        except:
            pass
        
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
        try:
            GameShopPrime.UpdateB1()
        except:
            print 'Failed: PgetB1'
        try:
            GameShopB2.UpdateB1()
        except:
            print 'Failed: B2getB1'
        return serpent.dumps(self.AllOrders)
    
    def CancellingOrder(self, IDbin, OrdersBin):
        try:
            self.UpdateP()
        except:
            print 'Failed: B1getP'
        try:
            self.UpdateB2()
        except:
            print 'Failed: B1getB2'
        
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
            GameShopPrime.UpdateB1()
        except:
            print 'Failed: PgetB1'
        try:
            GameShopB2.UpdateB1()
        except:
            print 'Failed: B2getB1'
        
        return serpent.dumps(self.AllOrders)




daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GameShop)   # register the greeting maker as a Pyro object
ns.register("backupserver.one", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls


#if __name__ == '__main__':
    #GameShop = Pyro4.Proxy("PYRONAME:backupserver.one")
    #try:
        #Gameshop.UpdateP()
    #except:
        #print 'Failed: B1getP'
    #try:
        #Gameshop.UpdateB2()
    #except:
        #print 'Failed: B1getB2'