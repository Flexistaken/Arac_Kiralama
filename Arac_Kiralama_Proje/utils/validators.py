from datetime import datetime

def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_date_order_valid(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    return end_date >= start_date

def is_empty(*args):
    return any(a.strip() == "" for a in args)

def is_number(value):
    return value.isdigit()
