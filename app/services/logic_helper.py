from datetime import datetime

def format_date_human(date_obj: datetime.date) -> str:
    day = date_obj.day
    suffix = (
        "th" if 11 <= day <= 13 else
        {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    )
    return date_obj.strftime(f"%-d{suffix} of %B %Y")
