from dataclasses import dataclass

@dataclass(frozen=True)
class Atome():
    '''Un atome a un symbole, un nom, un numéro atomque et une masse atomique'''
    symbole:str
    nom:str
    numero_atomique:int
    masse:float

    def obtenir_masse(self):
        '''Trouve la masse atomique'''
        return self.masse

    def representation_parenthesee(self):
        '''Représentation textuelle de l'atome'''
        return repr(self)

    def __repr__(self):
        return self.symbole
    
    def __str__(self):
        return f"#{self.numero_atomique} : {self.nom} ({self.symbole}). {self.masse}u"
    
    def dict(self):
        '''Dictionnaire comportant l'atome et le multiplicateur 1'''
        return {self.symbole:1}