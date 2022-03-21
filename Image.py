from PIL import Image, ImageDraw, ImageEnhance, ImageTk

class Ima: # Classe permettant de créer des images utilisables et modifiables par Horlengre.
    def __init__(self, adresse: str):
        self.original = Image.open(adresse)
        self.liCopie = []

    def reDim(self, largeur:int=0, hauteur:int=0, prop:float=0.0) -> int:
        """Permet de créer une copie redimensionnée d'une image Ima.

        Args:
            largeur (int, optional): largeur voulue pour l'image. Defaults to 0.
            hauteur (int, optional): hauteur voulue pour l'image. Defaults to 0.
            prop (float, optional): pourcentage de taille de l'image par rapport à ces dimensions originnelles. Defaults to 0.0.

        Returns:
            int: Numéro de la copie.
        """
        largeur = int(largeur)
        hauteur = int(hauteur)
        if prop == 0.0:
            d = (largeur, hauteur)
        else:
            w = int(self.original.width)
            h = int(self.original.height)
            d = (int(w*prop), int(h*prop))
        b = self.original.copy()
        b = b.resize(d)
        self.liCopie.append(b)
        return len(self.liCopie)-1

    def rogne(self, coo: tuple) -> int:
        """Permet de créer une copie rognée d'une image Ima.

        Args:
            coo (tuple): Partie de l'image à gardée, sous forme d'un rectangle.

        Returns:
            int: Numéro de la copie.
        """
        n = self.original.copy()
        n = n.crop(coo)
        self.liCopie.append(n)
        return len(self.liCopie)-1

    def createPhotoImage(self, numero: int) -> object:
        """Permet de créer des images photoImage à partir d'une image Ima.

        Args:
            numero (int): Numéro de la copie.

        Returns:
            object: Image PhotoImage
        """
        return ImageTk.PhotoImage(self.liCopie[numero])

    def getDimensions(self, numero: int = 'original') -> tuple:
        """Renvoie un tuple avec la taille de l'image.

        Args:
            numero (int, optional): Numéro de la copie. Defaults to 'original'.

        Returns:
            tuple: Dimensions de l'image.
        """
        res = None
        if numero == 'original':
            res = self.original
        elif type(numero) == int:
            if numero < len(self.liCopie):
                res = self.liCopie[numero]
        t = ()
        if res != None:
            t = (int(res.width), int(res.height))
        return t