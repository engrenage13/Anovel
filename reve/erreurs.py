from systeme.FondMarin import draw_texture, file_exists, get_file_extension, WHITE
from systeme.erreurs import *
from reve.OZ import TAILLEPOLICE, P1, P2
from ui.blocTexte import BlocTexte
from museeNoyee import cadreCodeErreur, cauchemar

def affichErreur(erreur: tuple, dims: list, y: int, espace: int) -> None:
        """Définit ce qui s'affiche dans la fenêtre quand le fichier ne peut pas être lu.

        Args:
            mode (int): Définit le type d'erreur rencontrée.
        """
        codeErreur = erreur[0]
        texteErreur = erreur[1]
        ebis = [codeErreur.texte, texteErreur.texte]
        draw_texture(cauchemar, int(dims[0]+dims[1]/2-cauchemar.width/2), 
                     int(y+cadreCodeErreur.height/2-cauchemar.height/2), checkCouleurErreur(ebis))
        draw_texture(cadreCodeErreur, int(dims[0]+dims[1]/2-cadreCodeErreur.width/2), y, WHITE)
        codeErreur.dessine([[int(dims[0]+dims[1]/2), int(y+cadreCodeErreur.height/2)], 'c'])
        y += cadreCodeErreur.height + espace
        texteErreur.dessine([[int(dims[0]+dims[1]/2), y], 'c'], checkCouleurErreur(ebis))

def erreursFichier(fichier: str, limites: list) -> bool:
    rep = []
    if not file_exists(fichier):
        texte = f"Le fichier \"{fichier}\" n'existe pas, ou n'est pas au bon endroit."
        rep.append((BlocTexte(e000[0], P1, int(TAILLEPOLICE*1.2)), 
                    BlocTexte(texte, P2, TAILLEPOLICE, limites)))
    if get_file_extension(fichier) != ".md":
        texte = f"L'extension du fichier \"{fichier}\", n'est pas prise en charge."
        rep.append((BlocTexte(e001[0], P1, int(TAILLEPOLICE*1.2)), 
                    BlocTexte(texte, P2, TAILLEPOLICE, limites)))
    if len(rep) == 0:
        rep = False
    return rep