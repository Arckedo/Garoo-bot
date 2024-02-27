# Définie le fichier comme un package
from roles.role import *
from roles.hunter import *
from roles.seer import *
from roles.thief import *
from roles.villager import *
from roles.werewolf import *
from roles.witch import *
from roles.roles_combination import *

night_action_list = [Thief, Seer, Werewolf, Witch]
day_action_list = [Hunter]
