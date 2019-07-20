import Cliente as cliente

class Lock:
    def __init__(self):
        self.c = cliente.Cliente()

    def run(self):
        if self.c.connect():
            while 1:
                building = input("Selecione o prédio (A, B ou C): ")

                while(building != 'A' and building != 'B' and building != 'C'):
                    building = input("Prédio inválido, prédios disponiveis: A, B, C\nSelecione o prédio: ")

                layer = input("Selecione o andar (1, 2 ou 3): ")

                while(int(layer) < 1 or int(layer) > 3):
                    layer = input("Andar inválido, andares disponiveis: 1, 2, 3\nSelecione o andar: ")

                passwdCode = input("Código de entrada (0 para visitante ou 1 para Funcionario)\nSelecione o código: ")

                while(int(passwdCode) != 0 and int(passwdCode) != 1):
                    passwdCode = input("Codigo invalido, codigos disponiveis\n0- Visitante\n1- Funcionário\nSelecione o código: ")

                
                msg = [building, layer]

                if (self.c.validate(msg,  passwdCode)): 
                    print("\nAutorizado\n")
                else:
                    print("\nNão autorizado\n")


Lock().run()
