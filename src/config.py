
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRIGGER_EMOJI = os.getenv("TRIGGER_EMOJI", "🔊")
MESSAGE_LIMIT = int(os.getenv("MESSAGE_LIMIT", 100))
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8765))
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST", "localhost")
