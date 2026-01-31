class Utils:
    @staticmethod
    def uptime(core):
        return int(time.time() - core.start_time)
    
    @staticmethod
    def ping():
        return "⚡ 50ms"
