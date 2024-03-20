from atome import Atome
from molecule import Molecule
import csv, re

def chager_tableau_periodique(nom_fichier):
    '''Charge le fichier contenant le tableau périodique'''
    with open(nom_fichier, newline='') as csvfile:
        lecteur = csv.reader(csvfile)
        next(lecteur)  # Sauter la ligne d'en-tête
        atomes = {r[0] : Atome(r[0], r[1], int(r[2]), float(r[3])) for r in lecteur}
    return atomes

def charger_molecules(tableau_periodique, nom_fichier):
    '''Charge le fichier contenant les formules chimiques des molécules'''
    with open(nom_fichier, newline='') as csvfile:
        lecteur = csv.reader(csvfile)
        next(lecteur)  # Sauter la ligne d'en-tête
        molecules = [m for m in 
                     (batir_molecule(tableau_periodique, r[0]) for r in lecteur) 
                     if m is not None]
    return molecules

def string_to_molecule(tableau_periodique, formule):
    '''
    Transforme une string en molécule
    Lance une exception si la formule ne représente pas une molécule
    '''
    pile = []
    pile.append(Molecule())

    regex_jetons = r"([A-Z][a-z]?\d*|\(|\{|\[|[\)\}\]]\d*)"
    jetons = re.split(regex_jetons, formule)
    for jeton in jetons:
        if re.match(r'(\(|\[|\{)', jeton) :
            pile.append(Molecule())
        elif re.match(r'(\)|\]|\})\d*', jeton) :
            particule = pile.pop()
            multiplicateur = re.search(r'\d+', jeton)
            particule.multiplicateur = int(multiplicateur.group()) if multiplicateur else 1
            pile[-1].ajouter_composant(particule)
        elif re.match(r'[A-Z][a-z]?\d*', jeton):
            atome = re.search(r'[A-Z][a-z]?', jeton).group()
            multiplicateur = re.search(r'\d+', jeton)
            particule = Molecule()
            particule.ajouter_composant(tableau_periodique[atome])
            particule.multiplicateur = int(multiplicateur.group()) if multiplicateur else 1
            pile[-1].ajouter_composant(particule)
    if len(pile) > 1:
        raise Exception(f"La chaîne {formule} ne représente pas une molécule valide")
    return pile.pop()
    
def batir_molecule(tableau_periodique, entree):
    '''
    Bâtit une molécule représentée par le texte entree. 
    Si l'entrée ne représente pas une molécule, la fonction retourne None.
    '''
    try:
        return string_to_molecule(tableau_periodique, entree)
    except Exception as e:
        print(f"La molécule {entree} est ignorée. {e}")
        return None
        
def menu():
    '''Affiche le menu et lit le choix de l'utilisateur'''
    debut = 1
    fin = 6
    choix = 6
    print("1 - Voir la liste des atomes")
    print("2 - Voir la liste des molécules")
    print("3 - Voir la masse d'une molécule")
    print("4 - Ajouter une molécule")
    print("5 - Voir la description d'une molécule")
    print("6 - Quitter")
    valide = False
    while not valide:
        entree = input(f"Entrez un choix entre {debut} et {fin}")
        choix = re.search(r'\d+', entree)
        valide = choix
        if valide:
            choix = int(choix.group())
            valide = debut <= choix <= fin
    return choix

def choix_liste_avec_nom(collection, description = ''):
    '''
    Demande à l'utilisateur de choisir une option parmi une liste. La liste doit être 
    itérable.  La description, optionnelle, est le texte à afficher.
    '''
    choix_valide = False
    pattern = r'^\d+$'
    
    while not choix_valide:
        print("Choisissez un option parmi les suivantes:")
        i = 0
        for m in collection:
            print(f"{i}: {m}")
            i += 1
        print(f"Entrez le numéro {description}")
        choix = input()
        choix_valide = re.match(pattern, choix)
        if (choix_valide):
            choix = int(choix)
            choix_valide = choix >= 0 and choix < len(collection)
    return collection[choix]
    
def imprimer_masse_molecule(molecules):
    '''Imprime la masse d'une molécule choisie par l'utilisateur'''
    print(str(choix_liste_avec_nom(molecules, 'de la molécule').obtenir_masse()) + 'u')

def imprimer_molecule(molecules):
    '''Imprime la description d'une molécule choisie par l'utilisateur'''
    m = choix_liste_avec_nom(molecules, 'de la molécule')
    print(m.dict())

def imprimer_atomes(tableau_periodique):
    '''Imprime la liste des atomes'''
    print('\n'.join([str(a) for a in tableau_periodique.values()]))

def ajouter_molecule(molecules, tableau_periodique, nom_fichier):
    '''Ajoute une molécule choisie par l'utilisateur à la liste de molécule et au fichier'''
    print("Entrez la formule d'une molécule")
    molecule = batir_molecule(tableau_periodique, input())
    if molecule is not None:
        molecules.append(molecule)
        with open(nom_fichier, 'a') as f:
            f.write(str(molecule))
    return molecules

def labo3():
    '''Point d'entrée du laboratoire 3'''
    fichier_atomes ='particules/tableau_periodique.csv'
    fichier_molecules = 'particules/molecules.csv'
    tableau_periodique = chager_tableau_periodique(fichier_atomes)
    for atome in tableau_periodique:
        print(atome)
    
    molecules = charger_molecules(tableau_periodique, fichier_molecules)

    choix = 1
    while choix != 6:
        choix = menu()
        match choix:
            case 1:
                imprimer_atomes(tableau_periodique)
            case 2:
                print(molecules)
            case 3 : 
                imprimer_masse_molecule(molecules)
            case 4 : 
                ajouter_molecule(molecules, tableau_periodique, fichier_molecules)
            case 5 : 
                imprimer_molecule(molecules)

if __name__ == "__main__":
    labo3()