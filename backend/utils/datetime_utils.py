from datetime import timezone, timedelta

def converter_horario(data):
    return data.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-3)))
