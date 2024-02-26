from discord import Client, User, SelectOption, TextChannel, Thread, Embed
from discord.interactions import Interaction
from discord.ui import Button, Select, View
from typing import Any, Optional, Union
import asyncio


"""
### Envoyer des interaction ###

# Envoyer un message simple
self.client.send("Message envoyé à tous")

# Envoyer et recevoir les résultats d'un vote
# Sous la forme d'un dico {entry: vote_count}
my_vote = GarooVote(...)
results = self.client.send_interface("Message", my_vote)

# Même chose pour un choix simple
my_choose = GarooChoose(...)
result = self.client.send_interface("Message", my_choose)

# Envoyer un message dans le salon des loup-garoux
self.client.send("Message", dest=self.client.werewolf_channel)

# Envoyer un message à un membre (en messages privés)
member = self.client.get_member(...)
self.client.send("Message", dest=member)
"""


class GarooEmbed(Embed):
    """Représente un embed pour interagir avec les joueurs."""

    def __init__(self, **kwargs) -> None:
        if "author" in kwargs:
            super().set_author(**kwargs.pop("author"))
        if "footer" in kwargs:
            super().set_footer(**kwargs.pop("footer"))
        if "thumbnail" in kwargs:
            super().set_thumbnail(**kwargs.pop("thumbnail"))
        if "image" in kwargs:
            super().set_image(**kwargs.pop("image"))
        super().__init__(**kwargs)


class GarooButton(Button):
    """Représente un bouton pour interagir avec les joueurs."""

    def __init__(self, *, label: str = None, **kwargs) -> None:
        super().__init__(label=label, **kwargs)
        self.event: asyncio.Event = None

    async def callback(self, interaction: Interaction) -> None:
        """COROUTINE - La fonction appelée lorsque le bouton est cliqué.
        Cette fonction peut être écrasée par des sous-classes."""
        self.event.set()

    def get_value(self) -> Any:
        """Renvoie la valeur associée au bouton.
        Cette fonction peut être écrasée par des sous-classes."""
        return None


class GarooSelect(Select):
    """Représente une barre de sélection pour interagir avec les joueurs."""

    def __init__(self, entries: list[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.event: asyncio.Event = None
        self.options = [SelectOption(label=entry) for entry in entries]

    async def callback(self, interaction: Interaction) -> None:
        """COROUTINE - La fonction appelée lorsqu'un élément est sélectionné.
        Cette fonction peut être écrasée par des sous-classes."""
        self.event.set()

    def get_value(self) -> str:
        """Renvoie la valeur associée au bouton.
        Cette fonction peut être écrasée par des sous-classes."""
        return self.values[0]


class GarooUI(View):
    """Représente une interface contenant un ou plusieurs boutons."""

    def __init__(
        self, *items: Union[GarooButton, GarooSelect], filter: list[int], **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.filter = filter
        self.event: asyncio.Event = None
        self.children: list[Union[GarooButton, GarooSelect]] = list(items)

    async def interaction_check(self, interaction: Interaction) -> bool:
        """COROUTINE - Une fonction appelée lorsque une interaction se produit dans l'interface.
        Retourne si la fonction `callback` associée à l'interaction devrait être appelée ou pas.
        Cette fonction peut être écrasée par des sous-classes."""
        if not interaction.user.id in self.filter:
            await interaction.response.send_message(
                "❌ Vous n'avez pas le droit d'interagir.", ephemeral=True
            )
        return False

    def get_value(self) -> Any:
        """Renvoie la valeur associée à l'interface.
        Cette fonction peut être écrasée par des sous-classes."""
        return [child.get_value() for child in self.children]

    def setup_event(self, event: asyncio.Event) -> None:
        """Change l'objet évènement associé à cette interface et à ses éléments."""
        self.event = event
        for child in self.children:
            child.event = event


class GarooVote(GarooUI):
    """Une sous-classe de GarooUI, configurée pour organiser un vote."""

    def __init__(
        self,
        entries: list[tuple[str, int]],
        filter: list[int],
        weight: dict[int, int] = {},
        **kwargs
    ) -> None:
        """
        Paramètres
        ----------
        entries : `list`
            Liste des choix pour le vote.
        filter : `list[int]`
            Liste des ID des joueurs autorisés à voter.
        weight : `dict[int, int]`
            Dictionnaire sous la forme `{id_joueur: poids}` où `poids` est le poids du vote du joueur.
        """
        # Liste des noms des joueurs à partir de la liste des id
        # [self.message.guild.get_member(id).nick for id in entries]
        options = [SelectOption(label=str(name), value=str(id)) for name, id in entries]
        entries_names = [name for name, id in entries]
        entries_id = [id for name, id in entries]
        super().__init__(Select(options=options), filter=filter, **kwargs)
        self.weight = weight
        self.voted_list: list[int] = []
        self.votes = {k: 0 for k in entries_id}

    async def interaction_check(self, interaction: Interaction) -> bool:
        user_id = interaction.user.id

        # Si l'utilisateur n'est pas dans la liste des autorisés
        if user_id not in self.filter:
            await interaction.response.send_message(
                "❌ Vous n'avez pas le droit de voter.", ephemeral=True
            )

        # Si l'utilisateur n'a pas encore voté
        elif user_id not in self.voted_list:
            entry = int(self.children[0].values[0])
            self.voted_list.append(user_id)
            self.votes[entry] += self.weight.get(user_id, 1)
            await interaction.response.send_message(
                "✅ Vous avez voté.", ephemeral=True
            )

        else:
            await interaction.response.send_message(
                "❌ Vous avez déjà voté.", ephemeral=True
            )

        # Si tous les utilisateurs de la liste ont voté
        if len(self.voted_list) >= len(self.filter):
            # Termine l'intraction
            self.event.set()

        # Ne pas appeller le callback des boutons
        return False

    def get_value(self) -> dict:
        return self.votes


class GarooChoose(GarooUI):
    """Une sous-classe de GarooUI, configurée pour permettre
    au joueurs de choisir une action."""

    def __init__(self, entries: list, filter: list[int], **kwargs):
        """
        Paramètres
        ----------
        entries : `list`
            Liste des choix à sélectionner.
        filter : `list[int]`
            Liste des ID des joueurs autorisés à interagir.
        """
        options = [SelectOption(label=str(e)) for e in entries]
        super().__init__(Select(options=options), filter=filter, **kwargs)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id in self.filter:
            # Si l'utilisateur est dans la liste des autoriés
            await interaction.response.send_message(
                "✅ Vous avez choisi.", ephemeral=True
            )
            # Termine l'intraction
            self.event.set()
        else:
            # Si l'utilisateur n'est pas dans la liste des autaurisés
            await interaction.response.send_message(
                "❌ Vous n'avez pas le droit d'interagir.", ephemeral=True
            )
        return False

    def get_value(self) -> str:
        return self.children[0].values[0]


class GarooClient:
    """Représente un client Discord utilisable par le jeu."""

    def __init__(
        self,
        client: Client,
        channel: TextChannel,
        werewolf_channel: Optional[TextChannel] = None,
    ) -> None:
        """
        Paramètres
        ----------
        client : `Client`
            Un client Discord.
        channel : `TextChannel`
            Un salon Discord lié à la partie.
        werewolf_channel : `TextChannel`
            Un salon Discord pour les loup-garoux.
        """
        self.client = client
        self.channel = channel
        self.werewolf_channel = werewolf_channel

    async def setup_werewolf_channel(self, werewolf_ids: list[int]) -> Thread:
        """Crée et configure un salon pour le rôle loup-garou.

        Paramètres
        ----------
        player_list : `list[int]`
            La liste des identifiants des utilisateurs à ajouter au salon.

        Retourne
        --------
        `Thread`
            Le salon créé.
        """
        channel = await self.channel.create_thread(name="loups-garous")
        self.werewolf_channel = channel
        for player in werewolf_ids:
            await channel.add_user(self.get_user(player))

    def get_user(self, user_id: int) -> Optional[User]:
        """Récupère un membre à partir d'un identifiant Discord.

        Paramètres
        ----------
        user_id : `int`
            L'identifiant Discord de l'utilisateur.

        Retourne
        --------
        `Optional[User]`
            L'utilisateur associé à l'identifiant.
            Renvoie `None` si l'identifiant est invalide.
        """
        return self.client.loop.run_until_complete(
            self.client.get_or_fetch_user(user_id)
        )

    def send(
        self,
        content: str = None,
        embed: GarooEmbed = None,
        dest: Union[TextChannel, User] = None,
    ) -> None:
        """Envoie un message.

        Paramètres
        ----------
        content : `str`
            Le texte du message.
        dest: `Union[TextChannel, User]`
            Le salon (ou l'utilisateur) à destination du message, par défaut le message sera
            envoyé dans le salon `channel` lié à l'objet.
        """
        dest = dest or self.channel
        self.client.loop.run_until_complete(dest.send(content=content, embed=embed))

    async def __send_interface(
        self,
        content: str = None,
        *,
        embed: GarooEmbed = None,
        view: GarooUI,
        dest: Union[TextChannel, User]
    ) -> None:
        event = asyncio.Event()
        view.setup_event(event)
        asyncio.create_task(dest.send(content, embed=embed, view=view))
        await event.wait()

    def send_interface(
        self,
        content: str = None,
        embed: GarooEmbed = None,
        *,
        interface: GarooUI,
        dest: Union[TextChannel, User] = None
    ) -> None:
        """Envoie un message contenant une interface
        et attend que l'interaction soit achevée.

        Paramètres
        ----------
        content : `str`
            Le texte du message.
        interface: `GarooUI`
            L'interface à envoyer.
        dest: `Union[TextChannel, User]`
            Le salon (ou utilisateur) à destination du message. Par défaut
            le message sera envoyé dans le salon `channel` lié à l'objet.

        Retourne
        --------
        `Any`
            La valeur associée à l'interface une fois l'interaction achevée.
        """
        dest = dest or self.channel
        task = self.__send_interface(
            content=content, embed=embed, view=interface, dest=dest
        )
        self.client.loop.run_until_complete(task)
        return interface.get_value()
