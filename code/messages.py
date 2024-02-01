class GarooMessages:
    """Messages par défaut pour les évènements durant une partie."""

    @classmethod
    def nightfall(cls):
        """Annonce le début de la nuit."""
        return "La nuit tombe sur Thiercelieux..."

    @classmethod
    def sunrise(cls):
        """Annonce le début du jour."""
        return "Le jour se lève sur Thiercelieux..."

    @classmethod
    def deaths_tonight(cls, count: int) -> str:
        """Annonce les joueurs tués pendant la nuit:

        Cette nuit il y a eu X morts.
        - <Joueur A> (à formatter)
        - <Joueur B> (à formatter)
        - etc...
        """
        return f"Cette nuit il y a eu {count} morts." + count * ("\n- {}")