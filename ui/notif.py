from FondMarin import Lili2, fond, gris, blanc, bleu1, Lili3, xf, yf

class Notification:
    def __init__(self, titre: str, identifiant: str) -> None:
        self.__titre = titre[:]
        self.__id = identifiant[:]
        self.__idMessage = 'message'+identifiant[:]
        self.__maxh = int(yf*0.73)
        self.__minh = int(yf*1.03)
        self.__etat = False
        x = int(xf*0.3)
        y = int(yf*0.11)
        fond.create_rectangle(xf/2-x/2, self.__minh, xf/2+x/2, self.__minh+y, fill=gris, tags=(self.__id))
        fond.create_text(xf/2, self.__minh+y*0.35, text=self.__titre, font=Lili3, fill=blanc, tags=(self.__id))
        fond.create_text(xf/2, self.__minh+y*0.77, text="", font=Lili2, fill=bleu1, 
                         tags=(self.__id, self.__idMessage))

    def montre(self) -> None:
        """Lance l'ascension de la notif.
        """
        self.__etat = True
        fond.tag_raise(self.__id, 'plateau')
        self.monte()
    
    def monte(self) -> None:
        """Fait monter la notif jusqu'à la limite puis attend et appel la méthode de descente.
        """
        pas = int(yf*0.02)
        fond.move(self.__id, 0, -pas)
        coord = fond.coords(self.__id)
        if coord[1] > self.__maxh:
            fond.after(30, self.monte)
        else:
            fond.after(1200, self.cache)

    def cache(self) -> None:
        """Fait descendre la notif jusqu'à la limite.
        """
        pas = int(yf*0.02)
        fond.move(self.__id, 0, pas)
        coord = fond.coords(self.__id)
        if coord[1] < self.__minh:
            fond.after(30, self.cache)
        else:
            self.__etat = False

    def getEtat(self) -> bool:
        """Retourne l'etat de la notif.

        Returns:
            bool: True si la notif est visible à l'écran, et False sinon.
        """
        return self.__etat

    def modifMessage(self, case: str=None) -> None:
        """Permet de modifier le message transmis par la notification.

        Args:
            case (str, optional): Nom de case. Defaults to None.
        """
        message = ""
        if case != None:
            message += f"en {case}"
        fond.itemconfigure(self.__idMessage, text=message)