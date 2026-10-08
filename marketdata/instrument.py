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
