from roles.role import Role


class Villager(Role):
    def __init__(self, lst_player):
        super().__init__(
            lst_player,
            image_link="https://th.bing.com/th/id/OIG4.iSx9lSZEfEWqvQCnPEnb?w=1024&h=1024&rs=1&pid=ImgDetMain",
            description="Les villageois sont des habitants ordinaires de Thiercelieux qui doivent identifier et éliminer les loups-garous pour sauver leur village.",
        )

    def __str__(self) -> str:
        return "Villageois"
