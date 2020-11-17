class Fract:
    def __init__(self, nom, denom):
        self.nom = nom
        self.denom = denom

    def __add__(self, other):
        new_denom = self.denom * other.denom
        first_nom = self.nom * other.denom
        second_nom = other.nom * self.denom
        new_nom = first_nom + second_nom
        return Fract(new_nom, new_denom)

    def __str__(self):
        return "nom :" + str(self.nom) + "denom :" + str(self.denom)



a = Fract(1, 5)
b = Fract(1, 3)
c = a + b
print(c)