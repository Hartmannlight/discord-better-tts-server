
from aiohttp import web
import config


class WebSocketServer:
    def __init__(self):
        self.active_websockets = {}

    async def start_server(self):
        app = web.Application()
        app.add_routes([web.get('/ws', self.websocket_handler)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, config.WEBSOCKET_HOST, config.WEBSOCKET_PORT)
        await site.start()
        print(f"WebSocket server running on ws://{config.WEBSOCKET_HOST}:{config.WEBSOCKET_PORT}/ws")

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        name = None
        print("New connection")

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    if name is None:
                        name = msg.data
                        print(f"{name} noted")
                        self.active_websockets[name] = ws
                    else:
                        print(f"Message from {name}: {msg.data}")
                elif msg.type == web.WSMsgType.ERROR:
                    print(f'WebSocket connection for {name} closed with exception', ws.exception())
        finally:
            if name:
                del self.active_websockets[name]

    async def send_message(self, name, message):
        if name in self.active_websockets:
            await self.active_websockets[name].send_str(message)

    def member_is_connected(self, name):
        return name in self.active_websockets
