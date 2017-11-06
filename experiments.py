
class Experiment:

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        for key in self.__dict__.keys():
            print("key: " + key)
        return "alguna vara"

experimento = Experiment(nombre="Sor", apellido="Raimunda")
print(experimento)