def get_secret(secret):
    from secrets import secrets
    return secrets[secret]

def trim_datetime(datetime):
    to_return = [datetime.year,
                 datetime.month - 1,
                 datetime.day,
                 datetime.hour,
                 datetime.minute]
    return to_return