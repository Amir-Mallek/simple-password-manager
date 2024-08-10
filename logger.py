import datetime


def log(text):
    open('logs.txt', 'a').write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [info]: {text}\n")
