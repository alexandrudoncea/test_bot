import datetime

def parse_iso_date(date_string):
    """Parse an ISO 8601 date string to a datetime object."""
    try:
        return datetime.datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None

def calculate_pr_age(created_at):
    """Calculate the age of a pull request in days."""
    parsed_date = parse_iso_date(created_at)
    if parsed_date:
        return (datetime.datetime.now(datetime.timezone.utc) - parsed_date).days
    return None
