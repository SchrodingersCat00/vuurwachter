from datetime import datetime

def get_datafilestring() -> str:
    now = datetime.now()
    return now.strftime("%m%d%Y")
