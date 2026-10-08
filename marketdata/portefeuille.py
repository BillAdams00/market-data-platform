import json 
from marketdata.position import Position 
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