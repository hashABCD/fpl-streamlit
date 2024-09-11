from datetime import datetime

def date_parser(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime('%d %B, %Y  %H:%M %p')

def num_processor(num):
    THOUSAND = 1000
    MILLION = 1000000
    NOT_AVAILABLE = "N.A."
    
    if(num == NOT_AVAILABLE):
        return NOT_AVAILABLE
    
    if(type(num)==str):
        return "ILLEGAL ARGUMENT"

    if num>MILLION:
        return f"{round(num/MILLION,2)} M"
    elif num>THOUSAND:
        return f"{round(num/THOUSAND,2)} K"
    else:
        return f"{num}"
    