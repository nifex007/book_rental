def regular(days):
    if days<2:
        return 2.0
    else:
        return float(2 + (days - 2) * 1.5)


def novels(days):
    if days<2:
        return 2.0
    elif days<3:
        return 4.5
    elif days>=3:
        return float(1.5 * days)
    

def compute_charge(book_type, days):
    
    charges = {
        'F' : float(3.0 * days),
        'R' : regular(days),
        'N' : novels(days)
    }

    return charges[book_type]

 