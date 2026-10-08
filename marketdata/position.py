from marketdata.instrument import Instrument

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