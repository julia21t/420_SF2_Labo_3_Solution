from dataclasses import dataclass

@dataclass(frozen=True)
class Atome():
    symbole:str
    nom:str
    numero_atomique:int
    masse:float

    def obtenir_masse(self):
        return self.masse

    def representation(self):
        return repr(self)

    def __repr__(self):
        return self.symbole
    
    def __str__(self):
        return f"#{self.numero_atomique} : {self.nom} ({self.symbole}). {self.masse}u"
    
    def dict(self):
        return {self.symbole:1}