
import discord
from websocket import WebSocketServer
import config


class MyClient(discord.Client):
    async def setup_hook(self) -> None:
        self.websocket_server = WebSocketServer()
        self.loop.create_task(self.websocket_server.start_server())

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_raw_reaction_add(self, payload):
        user = payload.member.name
        emoji = payload.emoji.name
        if emoji == config.TRIGGER_EMOJI and self.websocket_server.member_is_connected(user):
            channel = client.get_channel(payload.channel_id)
            snowflake = discord.Object(id=payload.message_id)
            async for message in channel.history(limit=config.MESSAGE_LIMIT, after=snowflake):
                await self.websocket_server.send_message(user, f"{message.author.display_name}: {message.content}")


if __name__ == '__main__':
    client = MyClient()
    client.run(config.BOT_TOKEN)
