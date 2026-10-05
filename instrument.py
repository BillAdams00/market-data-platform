import json

class Instrument:
    """Un instrument financier négociable : action, ETF ou obligation."""

    def __init__(self, symbole, nom, secteur, devise: str = "EUR"):
        self.symbole = symbole.upper()
        self.nom = nom
        self.secteur = secteur
        self.devise = devise

    def __repr__(self) -> str:
        return f"Instrument({self.symbole!r}, {self.nom!r}, {self.secteur!r})"

    def etiquette(self) -> str:
        """Libellé lisible destiné à l'affichage."""
        return f"{self.symbole} — {self.nom} ({self.secteur}, {self.devise})"
    
    
    def to_dict(self) -> dict:
        """Représentation sérialisable de cet instrument."""
        return {
            "symbole": self.symbole,
            "nom": self.nom,
            "secteur": self.secteur,
            "devise": self.devise,
        }

    @classmethod
    def from_dict(cls, donnees: dict):
        """Reconstruit un Instrument depuis un dictionnaire."""
        return cls(
            donnees["symbole"],
            donnees["nom"],
            donnees["secteur"],
            donnees["devise"],
        )


class Position():
    def __init__(self,instrument,quantite,prix_revient):
        
        if quantite <= 0 :
            raise ValueError("La valeur de la quantité n'est pas conforme, veuillez la reecrire ")
        if prix_revient <= 0 :
                raise ValueError("La valeur du prix de revient n'est pas conforme, veuillez la reecrire ")
    
        self.instrument = instrument
        self.quantite = quantite
        self.prix_revient = prix_revient
    
    def montant_investi(self):
        return self.quantite * self.prix_revient
    
    def __repr__(self) -> str:
        return f"Position({self.instrument.symbole}, {self.quantite} × {self.prix_revient})"

    def valeur_actuelle(self, prix_marche: float) -> float:
        """Valorisation de la ligne au cours fourni."""
        return self.quantite * prix_marche

    def plus_value(self, prix_marche: float) -> float:
        """Gain ou perte latente sur cette ligne."""
        return self.valeur_actuelle(prix_marche) - self.montant_investi()
    
    def renforcer(self, quantite, prix_revient):
        """Achat complémentaire : recalcule la quantité et le PRU pondéré."""
        if quantite <= 0:
            raise ValueError(f"{self.instrument.symbole} : quantité invalide ({quantite})")
        if prix_revient <= 0:
            raise ValueError(f"{self.instrument.symbole} : prix de revient invalide ({prix_revient})")

        montant_total = self.montant_investi() + quantite * prix_revient
        quantite_totale = self.quantite + quantite

        self.prix_revient = montant_total / quantite_totale
        self.quantite = quantite_totale
        
    def to_dict(self) -> dict:
        """Représentation sérialisable de cette position."""
        return {
            "instrument": self.instrument.to_dict(),
            "quantite": self.quantite,
            "prix_revient": self.prix_revient,
        }

    @classmethod
    def from_dict(cls, donnees: dict):
        """Reconstruit une Position depuis un dictionnaire."""
        instrument = Instrument.from_dict(donnees["instrument"])
        return cls(
            instrument,
            donnees["quantite"],
            donnees["prix_revient"],
        )
    
    
class PorteFeuille():
    def __init__(self,nom):
        self.nom = nom
        self.positions = []
    
    def montant_investi_total(self):
        total = 0
        for i in  self.positions :
            total = i.montant_investi() + total
        
        return total
    def ajouter(self, position):
        """Ajoute une nouvelle ligne, ou renforce celle qui existe déjà."""
        for position_existante in self.positions:
            if position_existante.instrument.symbole == position.instrument.symbole:
                position_existante.renforcer(position.quantite, position.prix_revient)
                return
        self.positions.append(position)
     
    
    def __len__(self) -> int:
        return len(self.positions)

    def __repr__(self) -> str:
        return f"Portefeuille {self.nom} ({len(self)} positions)"

    def supprimer(self, symbole: str) -> None:
        """Retire la ligne portant ce symbole. Erreur si elle n'existe pas."""
        symbole = symbole.upper()
        for position in self.positions:
            if position.instrument.symbole == symbole:
                self.positions.remove(position)
                return
        raise ValueError(f"{symbole} n'est pas détenu dans ce portefeuille")

    def valeur_totale(self, prix: dict) -> float:
        """Valorise le portefeuille avec le dictionnaire de cours fourni."""
        total = 0
        for position in self.positions:
            symbole = position.instrument.symbole
            if symbole not in prix:
                raise ValueError(f"Aucun cours fourni pour {symbole}")
            total = total + position.valeur_actuelle(prix[symbole])
        return total

    def plus_value_totale(self, prix: dict) -> float:
        """Gain ou perte latente sur l'ensemble du portefeuille."""
        return self.valeur_totale(prix) - self.montant_investi_total()# l'ajout — aligné avec le "for"
    
    def to_dict(self) -> dict:
        """Représentation sérialisable du portefeuille."""
        return {
            "nom": self.nom,
            "positions": [position.to_dict() for position in self.positions],
        }

    @classmethod
    def from_dict(cls, donnees: dict):
        """Reconstruit un PorteFeuille depuis un dictionnaire."""
        portefeuille = cls(donnees["nom"])
        for donnees_position in donnees["positions"]:
            portefeuille.positions.append(Position.from_dict(donnees_position))
        return portefeuille
    
    def sauvegarder(self, chemin: str) -> None:
        """Écrit le portefeuille dans un fichier JSON."""
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump(self.to_dict(), fichier, indent=2, ensure_ascii=False)

    @classmethod
    def charger(cls, chemin: str):
        """Reconstruit un portefeuille depuis un fichier JSON."""
        try:
            with open(chemin, "r", encoding="utf-8") as fichier:
                donnees = json.load(fichier)
        except FileNotFoundError:
            raise FileNotFoundError(f"Aucun portefeuille enregistré à l'emplacement {chemin}")
        except json.JSONDecodeError as erreur:
            raise ValueError(f"Le fichier {chemin} n'est pas un JSON valide : {erreur}")

        return cls.from_dict(donnees)
    
if __name__ == "__main__":
    nvidia = Instrument("nvda", "Nvidia", "Technologie")
    microsoft = Instrument("msft", "Microsoft", "Technologie")

    portefeuille = PorteFeuille("PEA Adams")
    portefeuille.ajouter(Position(nvidia, 12, 158.40))
    portefeuille.ajouter(Position(microsoft, 5, 214.75))

    print(portefeuille)
    print("Taille du portefeuille :",len(portefeuille))
    print("Le montant investi toatl est de: ",portefeuille.montant_investi_total())

    # renforcement : 8 Nvidia de plus, a 175,00
    portefeuille.ajouter(Position(nvidia, 8, 175.00))
    print(portefeuille)
    print(portefeuille.positions[0])
    print(portefeuille.montant_investi_total())

    cours = {"NVDA": 171.20, "MSFT": 198.30}
    print(portefeuille.valeur_totale(cours))
    print(portefeuille.plus_value_totale(cours))

    try:
        portefeuille.supprimer("aapl")
    except ValueError as erreur:
        print("Refusé :", erreur)

    try:
        portefeuille.valeur_totale({"NVDA": 171.20})
    except ValueError as erreur:
        print("Refusé :", erreur)
    
    # le JSON produit
    print(json.dumps(portefeuille.to_dict(), indent=2, ensure_ascii=False))

    # aller-retour complet
    copie = PorteFeuille.from_dict(portefeuille.to_dict())
    print(copie)
    print(copie.positions[0])
    print(copie.montant_investi_total())
    
    portefeuille.sauvegarder("portefeuille.json")
    print("Sauvegardé.")

    recharge = PorteFeuille.charger("portefeuille.json")
    print(recharge)
    print(recharge.positions[0])
    print(recharge.montant_investi_total())

    try:
        PorteFeuille.charger("inexistant.json")
    except FileNotFoundError as erreur:
        print("Refusé :", erreur)