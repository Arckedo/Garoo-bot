from discord import Client, Embed, TextChannel


class GarooClient:
    """Used by the game to communicate with the discord bot."""

    def __init__(self, client: Client, channel: TextChannel) -> None:
        self.client = client
        self.channel = channel

    async def __send(self, content: str, embed: Embed = None) -> None:
        await self.channel.send(content, embed=embed)

    def send(self, content: str, embed: Embed = None) -> None:
        """Send a message to a specific channel."""
        self.client.loop.run_until_complete(self.__send(content, embed))