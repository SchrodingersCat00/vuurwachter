from utils import get_datafilestring

class FileLogger:
    def __init__(self):
        self.filename = get_datafilestring()
        self.temp_values = []

    async def on_notify(self, new_temp):
        self.temp_values.append(new_temp)
        if len(self.temp_values) >= 300:
            date_time = get_datafilestring()
            with open(f'{date_time}.csv', 'a+') as f:
                f.write('\n'.join(map(str, self.temp_values)) + '\n')
            self.temp_values = []

