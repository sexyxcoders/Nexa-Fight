class RaidEngine:
    def __init__(self, vc):
        self.vc = vc
    
    async def single_raid(self, chat_id):
        return await self.vc.multi_join(chat_id)
    
    async def mass_raid(self, chat_id):
        return await self.vc.multi_join(chat_id)
