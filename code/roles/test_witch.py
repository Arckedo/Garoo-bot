from discord.interactions import Interaction
from roles.preset_template import RolePreset
from role import _Player as Player
from bot.interactions import GarooButton, GarooClient, GarooUI
from typing import Optional


CHOICE_NOTHING = "nothing"
CHOICE_LIFE = "life"
CHOICE_DEATH = "death"


class LifePotionButton(GarooButton):
    def __init__(self, disabled: bool) -> None:
        super().__init__(
            label="Potion de Vie",
            custom_id=CHOICE_LIFE,
            disabled=disabled
        )

class DeathPotionButton(GarooButton):
    def __init__(self, disabled: bool) -> None:
        super().__init__(
            label="Potion de Mort",
            custom_id=CHOICE_DEATH,
            disabled=disabled
        )

class NothingButton(GarooButton):
    def __init__(self) -> None:
        super().__init__(
            label="Ne rien faire",
            custom_id=CHOICE_NOTHING
        )

class WitchUI(GarooUI):
    def __init__(self, no_life_potion: bool, no_death_potion: bool) -> None:
        super().__init__(
            LifePotionButton(no_life_potion),
            DeathPotionButton(no_death_potion),
            NothingButton()
        )

    async def interaction_check(self, interaction: Interaction) -> bool:
        self.value = interaction.custom_id
        self.disable_all_items()
        await interaction.message.edit(view=self)
        await interaction.response.send_message(f"Vous avez choisi : `{self.value}`", ephemeral=True)
        self.event.set()
        return False

    def get_value(self) -> Optional[str]:
        return self.value


class Witch(RolePreset):
    def __init__(self) -> None:
        self.name = "witch"
        self.team = "villagers"
        self.max_players = 1
        self.min_players = 0

        self.life_potions = 1
        self.death_potions = 1

    def nighttime_behavior(self, client: GarooClient, player_list: list[Player], last_killed: Optional[Player]):
        """La nuit, la sorcière peut soit ressusciter le joueur venant d'être tué
        par les loup-garous, soit tuer un autre joueur, soit ne rien faire."""

        if self.life_potions == self.death_potions == 0:
            client.send("La sorcière n'a plus de potions...")
            return

        no_life_potion = (self.life_potions <= 0) or not last_killed
        no_death_potion = (self.death_potions <= 0)
        interface = WitchUI(no_life_potion, no_death_potion)
        result = client.send_interface("Que voulez-vous faire ?", interface)

        if result == CHOICE_LIFE:
            # last_killed.is_alive = True
            print("a choisi de ressusciter")
            self.life_potions -= 1

        elif result == CHOICE_DEATH:
            # Tuer un autre joueur
            print("a choisi de tuer")
            self.death_potions -= 1


def setup():
    return Witch