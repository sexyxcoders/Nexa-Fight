class VCManager:
    def __init__(self, core):
        self.core = core
        self.playing = {}
        self.volume = 100
        self.loop = False
    
    async def multi_join(self, chat_id):
        count = 0
        for name, client in self.core.clients.items():
            try:
                await client.join_group_call(chat_id)
                self.core.vc_status[name]["active"] = True
                self.core.vc_status[name]["chat_id"] = chat_id
                count += 1
            except:
                pass
        return count
    
    async def multi_leave(self):
        count = 0
        for name, client in self.core.clients.items():
            if self.core.vc_status[name]["active"]:
                try:
                    await client.leave_group_call(self.core.vc_status[name]["chat_id"])
                    self.core.vc_status[name]["active"] = False
                    count += 1
                except:
                    pass
        return count
    
    async def multi_play(self, chat_id, audio_id):
        count = 0
        for name, client in self.core.clients.items():
            if self.core.vc_status[name]["chat_id"] == chat_id:
                try:
                    await client.start_audio_file(audio_id)
                    self.playing[name] = True
                    count += 1
                except:
                    pass
        return count
