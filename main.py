import discord
import asyncio
from aiohttp import web


class MyClient(discord.Client):
    async def setup_hook(self) -> None:
        self.loop.create_task(self.my_background_task())
        self.loop.create_task(self.start_web_server())

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        print(f'{message.author} in {message.channel}: {message.content}')

    async def my_background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            print("Background task is running")
            await asyncio.sleep(10)

    async def start_web_server(self):
        app = web.Application()
        app.add_routes([web.get('/ws', self.websocket_handler)])

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()

        print("WebSocket server running on ws://localhost:8080/ws")

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                print("Received message via WebSocket:", msg.data)
                await ws.send_str("Message received: " + msg.data)
            elif msg.type == web.WSMsgType.ERROR:
                print('WebSocket connection closed with exception', ws.exception())

        print("WebSocket connection closed")
        return ws


if __name__ == '__main__':
    client = MyClient()
    client.run('YOUR_TOKEN')
