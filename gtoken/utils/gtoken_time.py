import pytz
from datetime import datetime

def _utcnow():
    return datetime.utcnow().replace(tzinfo=pytz.UTC)
