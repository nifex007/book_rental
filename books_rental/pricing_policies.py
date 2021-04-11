def compute_charge(book_type, days):
    charges_per_day = {
        'F' : 3.0,
        'R' : 1.5,
        'N' : 1.5
    }

    return float(charges_per_day[book_type] * days)