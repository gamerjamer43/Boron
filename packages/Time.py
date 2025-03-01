import time, pytz
from datetime import datetime

def utc() -> int:
    return int(time.time())

def now(tz: str = "UTC") -> str:
    info = pytz.timezone(tz)
    return datetime.now(info).strftime("%Y-%m-%d %H:%M:%S %Z")

def tzToTz(dt: str, fro: str, to: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Converts a datetime string from one timezone to another."""
    fro = pytz.timezone(fro)
    to = pytz.timezone(to)
    
    dt = fro.localize(datetime.strptime(dt, fmt))
    converted = dt.astimezone(to)
    
    return converted.strftime(fmt + " %Z")

def toDatetime(timestamp: int, tz: str = "UTC", fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    info = pytz.timezone(tz)
    dt = datetime.fromtimestamp(timestamp, info)
    return dt.strftime(fmt + " %Z")

def toTimestamp(dt: str, tz: str = "UTC", fmt: str = "%Y-%m-%d %H:%M:%S") -> int:
    info = pytz.timezone(tz)
    dt = info.localize(datetime.strptime(dt, fmt))
    return int(dt.timestamp())

def wait(interval: int) -> None:
    time.sleep(interval)