from PIL import Image, ImageDraw, ImageEnhance, ImageTk

class Ima:
    def __init__(self, adresse: str):
        self.original = Image.open(adresse)
        self.liCopie = []

    def reDim(self, largeur:int=0, hauteur:int=0, prop:float=0.0, source: int=None) -> int:
        """Permet de créer une copie redimensionnée d'une image Ima.

        Args:
            largeur (int, optional): largeur voulue pour l'image. Defaults to 0.
            hauteur (int, optional): hauteur voulue pour l'image. Defaults to 0.
            prop (float, optional): pourcentage de taille de l'image par rapport à ces dimensions originnelles. Defaults to 0.0.
            source (int, optional): indice de l'image à modifier. Si non précisé, modifie l'original.

        Returns:
            int: Numéro de la copie.
        """
        image = self.original
        if source != None and type(source) == int and source >= 0 and source < len(self.liCopie):
            image = self.liCopie[source]
        largeur = int(largeur)
        hauteur = int(hauteur)
        if prop == 0.0:
            d = (largeur, hauteur)
        else:
            w = int(image.width)
            h = int(image.height)
            d = (int(w*prop), int(h*prop))
        b = image.copy()
        b = b.resize(d)
        self.liCopie.append(b)
        return len(self.liCopie)-1

    def rogne(self, coo: tuple, source: int=None) -> int:
        """Permet de créer une copie rognée d'une image Ima.

        Args:
            coo (tuple): Partie de l'image à gardée, sous forme d'un rectangle.
            source (int, optional): indice de l'image à modifier. Si non précisé, modifie l'original.

        Returns:
            int: Numéro de la copie.
        """
        image = self.original
        if source != None and type(source) == int and source >= 0 and source < len(self.liCopie):
            image = self.liCopie[source]
        n = image.copy()
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
            tuple: Longueur x hauteur de l'image.
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

    def tourne(self, angle: float, source: int=None) -> int:
        """Crée une copie tournée de l'image source avec le degré voulu.

        Args:
            angle (float): Degré pour la rotation de l'image. (sens inverse des aiguilles d'une montre.)
            source (int, optional): Si non précisé, copie de l'original ; sinon, copie de la copie voulue. Defaults to None.

        Returns:
            int: L'indice de la copie créée.
        """
        image = self.original
        if source != None and type(source) == int and source >= 0 and source < len(self.liCopie):
            image = self.liCopie[source]
        mod = image.copy()
        nouv = mod.rotate(angle, expand=True)
        self.liCopie.append(nouv)
        return len(self.liCopie)-1