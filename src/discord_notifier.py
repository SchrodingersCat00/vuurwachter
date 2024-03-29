import logging

class DiscordNotifier:
    def __init__(self, alertfunc):
        self.alertfunc = alertfunc
        self.state = Starting()

    async def on_notify(self, new_temp):
        last_state = self.state
        self.state = await self.state.handle(new_temp, self.alertfunc)
        if self.state.name != last_state.name:
            logging.info(f'State changed to {self.state.name}')

class State:
    pass

class Starting(State):
    def __init__(self):
        self.name = 'Starting'

    async def handle(self, temp, alertfunc) -> State:
        if temp > 50:
            return Burning()
        else:
            return Starting()

class Burning(State):
    def __init__(self):
        self.name = 'Burning'
    
    async def handle(self, temp, alertfunc) -> State:
        if temp >= 75:
            try:
                await alertfunc(f'Temperatuur is te hoog!\nDe temperatuur is: {temp}°C.', 'warning')
            except ValueError:
                logging.warning(f'Temperature is too high but Discord is not initialized yet!')
        
            return Danger()

        elif temp < 50:
            try:
                await alertfunc(f'Temperatuur is te laag!\nDe temperatuur is: {temp}°C.', 'info')
            except ValueError:
                logging.warning(f'Temperature is too low but Discord is not initialized yet!')

            return Dying()

        else:
            return Burning()

class Dying(State):
    def __init__(self):
        self.name = 'Dying'
    
    async def handle(self, temp, alertfunc) -> State:
        if temp > 50:
            return Burning()

        if temp < 30:
            try:
                await alertfunc(f'Het vuur is uit.', 'info')
            except ValueError:
                logging.warning(f'Fire has died but Discord is not initialized yet!')

            return Starting()

        else:
            return Dying()

class Danger(State):
    def __init__(self):
        self.name = 'Danger'
    
    async def handle(self, temp, alertfunc) -> State:
        if temp < 70:
            try:
                await alertfunc(f'De temperatuur is terug onder 70°C gedaald.\nDe temperatuur is: {temp}°C.', 'info')
            except ValueError:
                logging.warning(f'Fire has gone below 70 but Discord is not initialized yet!')

            return Burning()
        
        if temp > 80:
            try:
                await alertfunc(f'Gevaar: Het vuur is warmer dan 80°C!\nDe temperatuur is: {temp}°C.', 'danger')
            except ValueError:
                logging.warning(f'Fire is higher than 80 degrees but Discord is not initialized yet!')

        return Danger()
