class SudoManager:
    def __init__(self, core):
        self.core = core
    
    def add(self, user_id):
        if user_id not in self.core.sudo_list:
            self.core.sudo_list.append(user_id)
            return True
        return False
    
    def remove(self, user_id):
        if user_id in self.core.sudo_list and user_id != OWNER_ID:
            self.core.sudo_list.remove(user_id)
            return True
        return False
    
    def list(self):
        return self.core.sudo_list.copy()
