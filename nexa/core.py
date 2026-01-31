from pyrogram import Client
from config import *
import asyncio
import time

class NexaCore:
    def __init__(self):
        self.clients = {}
        self.vc_status = {}
        self.sudo_list = SUDO_USERS.copy()
        self.start_time = time.time()
    
    async def start_clients(self):
        for i, session in enumerate(SESSIONS):
            if session:
                name = f"nexa{i+1}"
                client = Client(name, API_ID, API_HASH, session_string=session)
                await client.start()
                self.clients[name] = client
                self.vc_status[name] = {"active": False, "chat_id": None}
        print(f"✅ {len(self.clients)} Sessions Active!")
