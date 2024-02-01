from discord import Client, SelectOption, TextChannel
from discord.interactions import Interaction
from discord.ui import Button, Select, View
from typing import Any, Union
import asyncio


class GarooButton(Button):
    """Représente un bouton pour interagir avec les joueurs."""

    def __init__(self, *, label: str = None, **kwargs) -> None:
        super().__init__(label=label, **kwargs)
        self.event: asyncio.Event = None

    async def callback(self, interaction: Interaction) -> None:
        """COROUTINE - La fonction appelée lorsque le bouton est cliqué.
        Cette fonction peut être écrasée par des sous-classes."""
        self.event.set()

    def get_value(self) -> None:
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

    def __init__(self, *items: Union[GarooButton, GarooSelect], **kwargs) -> None:
        super().__init__(**kwargs)
        self.event: asyncio.Event = None
        self.children: list[Union[GarooButton, GarooSelect]] = list(*items)

    async def interaction_check(self, interaction: Interaction) -> bool:
        """COROUTINE - Une fonction appelée lorsque une interaction se produit dans l'interface.
        Retourne si la fonction `callback` associée à l'interaction devrait être appelée ou pas.
        Cette fonction peut être écrasée par des sous-classes."""
        return True

    def get_value(self) -> Any:
        """Renvoie la valeur associée à l'interface.
        Cette fonction peut être écrasée par des sous-classes."""
        return [child.get_value() for child in self.children]

    def set_event(self, event: asyncio.Event) -> None:
        """Change l'évènement de cette interface et de tous ses éléments."""
        self.event = event
        for child in self.children:
            child.event = event


class GarooVote(GarooUI):
    """Une sous-classe de GarooUI, configurée pour organiser un vote."""

    def __init__(self, entries: list[int], filter: list[int], weight: dict[int, int] = {}, **kwargs) -> None:
        # Liste des noms des joueurs à partir de la liste des id
        names = entries.copy() # [self.message.guild.get_member(id).nick for id in entries]
        options = [SelectOption(label=str(name), value=str(id)) for name, id in zip(names, entries)]

        super().__init__([Select(options=options)], **kwargs)
        self.filter = filter
        self.weight = weight
        self.voted_list: list[int] = []
        self.votes = {k: 0 for k in names}

    async def interaction_check(self, interaction: Interaction) -> bool:
        user_id = interaction.user.id

        # Si l'utilisateur n'est pas dans la liste des autorisés
        if user_id not in self.filter:
            await interaction.response.send_message("❌ Vous n'avez pas le droit de voter.", ephemeral=True)

        # Si l'utilisateur n'a pas encore voté
        elif user_id not in self.voted_list:
            entry = int(self.children[0].values[0])
            self.voted_list.append(user_id)
            self.votes[entry] += self.weight.get(user_id, 1)
            await interaction.response.send_message("✅ Vous avez voté.", ephemeral=True)
        
        else:
            await interaction.response.send_message("❌ Vous avez déjà voté.", ephemeral=True)
        
        # Si tous les utilisateurs de la liste ont voté
        if len(self.voted_list) >= len(self.filter):
            self.event.set()
        
        # Ne pas appeller le callback des boutons
        return False
    
    def get_value(self):
        return self.votes


class GarooClient:
    """Représente un client Discord utilisable par le jeu."""

    def __init__(self, client: Client, channel: TextChannel) -> None:
        self.client = client
        """Un client Discord."""
        self.channel = channel
        """Un salon Discord lié à la partie."""

    async def __send_interface(self, content: str, view: GarooUI) -> None:
        """Envoie un message contenant une interface."""
        event = asyncio.Event()
        view.set_event(event)
        asyncio.create_task(self.channel.send(content, view=view))
        await event.wait()

    def send(self, content: str) -> None:
        """Envoie un message au salon lié à la partie actuelle."""
        self.client.loop.run_until_complete(self.channel.send(content))

    def send_interface(self, content: str, interface: GarooUI) -> None:
        """Envoie un message contenant une interface.
        Renvoie la valeur associée à l'interface une fois l'interaction achevée."""
        task = self.__send_interface(content, view=interface)
        self.client.loop.run_until_complete(task)
        return interface.get_value()