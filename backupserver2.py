# saved as greeting-server.py
import Pyro4
import serpent


GameShopPrime = Pyro4.Proxy("PYRONAME:server.prime") # use name server object lookup uri shortcut
GameShopB1 = Pyro4.Proxy("PYRONAME:backupserver.one")

@Pyro4.behavior(instance_mode="single")
@Pyro4.expose
class GameShop(object):
    def __init__(self):
        self.products = ['AgeOfEmpires2', 'Tron', 'SuperMarioKart', 'ZombieApokalypse']
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
        
    def UpdateB1(self):
        try:
            self.AllOrders = GameShopB1.AllOrderPrint()
        except:
            state = 0
        return state
    
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
            self.UpdateB1()
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
            GameShopPrime.UpdateB2()
            GameShopB1.UpdateB2()
        except:
            pass
        return serpent.dumps(self.AllOrders)
    
    def CancellingOrder(self, IDbin, OrdersBin):
        try:
            self.UpdateP()
            self.UpdateB1()
        except:
            pass
        
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
            GameShopPrime.UpdateB2()
            GameShopB1.UpdateB2()
        except:
            pass
        return serpent.dumps(self.AllOrders)


        


daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GameShop)   # register the greeting maker as a Pyro object
ns.register("backupserver.two", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls



if __name__ == '__main__':
    GameShop = Pyro4.Proxy("PYRONAME:backupserver.two")
    try:
        Gameshop.UpdateP()
    except:
        print 'Failed: B2getP'
    try:
        Gameshop.UpdateB1()
    except:
        print 'Failed: B2getB1'