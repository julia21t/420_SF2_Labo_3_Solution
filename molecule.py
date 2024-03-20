class Molecule:
    '''
    Une molécule a un multiplicateur et une liste de composants.
    Les composants d'une molécule peuvent être une molécule ou un atome
    '''
    def __init__(self):
        self._multiplicateur = 1
        self._composants = []

    @property
    def multiplicateur(self):
        return self._multiplicateur
    
    @multiplicateur.setter
    def multiplicateur(self, valeur):
        self._multiplicateur = valeur

    def ajouter_composant(self, composant):
        '''Ajoute un composant à la molécule'''
        self._composants.append(composant)

    def obtenir_masse(self):
        '''Trouve la masse de la molécule'''
        return self.multiplicateur * sum(c.obtenir_masse() for c in self._composants)

    def representation_parenthesee(self):
        '''Représentation textuelle d'une molécule'''
        composants = ""
        if len(self._composants) > 1:
            composants = "("
        composants += f"{''.join(c.representation_parenthesee() for c in self._composants)}"
        if len(self._composants) > 1:
            composants += ")"
        if self.multiplicateur > 1:
            composants += str(self.multiplicateur)
        return composants

    def __repr__(self):
        composants = ""
        composants += f"{''.join(c.representation_parenthesee() for c in self._composants)}"
        return composants

    def dict(self):
        '''bâtit le dictionnaire des occurences des atomes dans la molécule'''
        dict = {}
        for c in self._composants:
            d = c.dict()
            dict = {x: dict.get(x, 0) + self.multiplicateur * d.get(x, 0) for x in dict | d}
        return dict