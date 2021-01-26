import time
from datetime import date
import os                           # This is needed to have the command line
os.system("")                       # render ANSI escape codes


# For ANSI escape sequences
# Refer to https://en.wikipedia.org/wiki/ANSI_escape_code
def esc(code):
    return f'\033[{code}m'


def feb_days(year):
    if year % 4 == 0:
        return list(range(1, 30))
    else:
        return list(range(1, 29))


current_year = time.strftime("%Y")

calendar_year_struct = {
        "January": (list(range(1, 32)), 1),
        "February": (feb_days(int(current_year)), 2),
        "March": (list(range(1, 32)), 3),
        "April": (list(range(1, 31)), 4),
        "May": (list(range(1, 32)), 5),
        "June": (list(range(1, 31)), 6),
        "July": (list(range(1, 32)), 7),
        "August": (list(range(1, 32)), 8),
        "September": (list(range(1, 31)), 9),
        "October": (list(range(1, 32)), 10),
        "November": (list(range(1, 31)), 11),
        "December": (list(range(1, 32)), 12)
}

weekdays = "Su\tM\tT\tW\tTh\tF\tS"


# Prints calendar of requested month
# Month input must be consistent with dict keys
def print_month_calendar(month):
    i = date(int(current_year), calendar_year_struct[month][1], 1).isoweekday()     # Aligns month to center
    if i == 7:                                                                      # Handles months whose first day
        i = 0                                                                       # is on a Monday
    spaces = int(len(weekdays) - len(month))
    print(" " * spaces, esc(1), month, esc(0), sep="")
    print(esc(94), weekdays, esc(0), sep="")
    for day in calendar_year_struct[month][0]:
        if day == calendar_year_struct[month][0][0]:                                # Aligns first week to the right
            print("\t" * i, end="")                                                 # of the calendar
        i += 1
        if i < 7:
            print(day, end="\t")
        else:
            i = 0
            print(day)
