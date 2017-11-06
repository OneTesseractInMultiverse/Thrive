
class Experiment:

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        for key in self.__dict__.keys():
            print("key: " + key)
        return "alguna vara"

    def get(self):
        for key, value in self.__dict__.items():
            print('key: ' + key + ' value: ' + value)


experimento = Experiment(nombre="Sor", apellido="Raimunda")
print(experimento)
experimento.get()