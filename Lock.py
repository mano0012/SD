import Cliente as cliente

class Lock:
    def __init__(self):
        self.building = "A"
        self.layer = "2"
        self.c = cliente.Cliente()

    def run(self):
        if self.c.connect():
            while 1:
                msg = [self.building, self.layer]

                passwdCode = input("Code: ")

                while(int(passwdCode) < 0 or int(passwdCode) > 2):
                    passwdCode = input("Codigo invalido, codigos disponiveis\n0- Visitante\n1- Funcionário\n2- Administrador\nSelecione o código: ")

                if (self.c.validate(msg,  passwdCode)):
                    print("Authorized")
                else:
                    print("Unauthorized")


Lock().run()
