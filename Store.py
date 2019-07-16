import Enc
import json
class Store:
    def __init__(self):
        self.enc = Enc.Enc()
        self.data = json.loads('{"A":10,"B":20, "C": 5}')
        try:
            print(self.data['C'])
        except:
            self.data['C'] = 10
            print(self.data['C'])
        
        
Store()

