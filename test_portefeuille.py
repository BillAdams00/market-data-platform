import pytest

from marketdata import Instrument, Position, PorteFeuille


def test_montant_investi_total():
    nvidia = Instrument("nvda", "Nvidia", "Technologie")
    microsoft = Instrument("msft", "Microsoft", "Technologie")

    portefeuille = PorteFeuille("PEA test")
    portefeuille.ajouter(Position(nvidia, 12, 158.40))
    portefeuille.ajouter(Position(microsoft, 5, 214.75))

    assert len(portefeuille) == 2
    assert portefeuille.montant_investi_total() == pytest.approx(2974.55)


def test_renforcement_recalcule_le_pru():
    nvidia = Instrument("nvda", "Nvidia", "Technologie")

    portefeuille = PorteFeuille("PEA test")
    portefeuille.ajouter(Position(nvidia, 12, 158.40))
    portefeuille.ajouter(Position(nvidia, 8, 175.00))

    assert len(portefeuille) == 1
    assert portefeuille.positions[0].quantite == 20
    assert portefeuille.positions[0].prix_revient == pytest.approx(165.04)
    
    
def test_quelque_chose_est_refuse():
    nvidia = Instrument("nvda", "Nvidia", "Technologie")
    with pytest.raises(ValueError):
        Position(nvidia,-3,128)

def test_supprimer_symbole_absent():
    nvidia = Instrument("nvda", "Nvidia", "Technologie")
    portefeuille = PorteFeuille("Pea_test")
    portefeuille.ajouter(Position(nvidia,3,128))
    with pytest.raises(ValueError,match="AAPL"):
        portefeuille.supprimer("AAPL")

def test_valeur_totale_sans_cours():
    nvidia = Instrument("nvda", "Nvidia", "Technologie")
    microsoft = Instrument("msft", "Microsoft", "Technologie")
    dic_cours = {"NVDA":120}
    portefeuille = PorteFeuille("PEA test")
    portefeuille.ajouter(Position(nvidia, 12, 158.40))
    portefeuille.ajouter(Position(microsoft, 5, 214.75))
    with pytest.raises(ValueError, match="MSFT"):
        portefeuille.valeur_totale(dic_cours)
    