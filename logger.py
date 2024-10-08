import datetime

logs = []
can_log = True

class BaseLogTypes:
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'

    BASHCOLORS = {INFO:'\033[92m',
                  WARN:'\033[93m',
                  ERROR:'\033[91m'}
    
    WHITE = '\033[97m'

def disablelog():
    global can_log
    can_log = False

def enablelog():
    global can_log
    can_log = True  

def log(logtype: str, message: str) -> None:
    log = f'[{logtype}]: {message} - {str(datetime.datetime.now())}'
    colored_log = BaseLogTypes.BASHCOLORS[logtype] + log + BaseLogTypes.WHITE
        
    logs.append(log)
    if can_log:
        print(colored_log)
    else:
        return

def dumplogs(filepath: str) -> None:
    with open(filepath, 'a') as file:
        for log in logs:
            file.write(f'{log}\n')