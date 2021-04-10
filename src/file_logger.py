from utils import get_datafilestring

class FileLogger:
    def __init__(self):
        self.filename = get_datafilestring()
    
    async def on_notify(self, new_temp):
        date_time = get_datafilestring()
        with open(f'{date_time}.csv', 'a+') as f:
            f.write(f'{new_temp}\n')
