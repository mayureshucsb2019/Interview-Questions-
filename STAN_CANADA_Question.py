"""
Question

Stan is looking to provide access to creators' calendars and enable fans to book meetings with them.
Your assignment is to create an algorithm that will assess the creator's calendar and return available slots
for fans to book.
"""
import datetime

# Takes string YYYY-MM-DD hh:mmAM as string
def getEpochTime(date):
    a_year = int(date[:4])
    a_month = int(date[5:7])
    a_day = int(date[8:10])
    a_hr = int(date[11:13])
    a_min = int(date[14:16])
    if date[-2] == "P" and a_hr < 12:
        a_hr += 12
    return datetime.datetime(a_year, a_month, a_day, a_hr, a_min, 0)

# Takes datetime object
def getStringTime(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    hour = date.hour
    hour = str(hour - 12) if hour > 12 else str(hour)
    minute = str(date.minute)
    am_pm = "AM" if date.hour < 12 else "PM"
    year = "0"*(4-len(year))+year
    month = "0"+month if len(month) == 1 else month
    day = "0"+day if len(day) == 1 else day
    hour = "0"+hour if len(hour) == 1 else hour
    minute = "0"+minute if len(minute) == 1 else minute
    return f"{year}-{month}-{day} {hour}:{minute}{am_pm}"

# Takes datetime objects as input
def get_duration_in_minutes(date_1, date_2):
    if date_1 > date_2:
        date_1, date_2 = date_2, date_1
    c = date_2-date_1
    return c.total_seconds()/60

# Interval is in string, and duration in minutes
def get_chunks_of_interval(interval, duration):
    if get_duration_in_minutes(getEpochTime(interval[0]), getEpochTime(interval[1])) < duration:
        return []
    chunks = []
    start = getEpochTime(interval[0])
    end = getEpochTime(interval[1])
    while start <= end:
        if start + datetime.timedelta(minutes=duration) <= end:
            chunks.append(
                [getStringTime(start), getStringTime(start + datetime.timedelta(minutes=duration))])
        start += datetime.timedelta(minutes=duration)
    return chunks


def fetch_available_slots(duration, events):
    """
    :param duration <int>: duration of the slot we're trying to book in minutes

    :param events <list<list<datetime>>>: list of start and end dates of time slots that are alrady taken
        i.e. [["2021-06-20 00:00AM", "2021-06-20 00:30AM"],["2021-06-20 11:00AM", "2021-06-20 11:30AM"], ["2021-06-20 03:00PM", "2021-06-20 04:00PM"] ]
        24 * 60 = 1440
        events: [[0,30],[660,690],[900,960]]
    :return <list<list<datetime>>>: list of slots a fan may book
    """
    # Sort the array buy the start time
    available_slots = []
    events = sorted(events, key=lambda y: getEpochTime(y[0]), reverse=False)
    print("All events: ", events)
    l = len(events)
    temp_event = events[0]
    for i in range(0, l):
        # Add the slots from start of day if not starting from 00:00AM
        if i == 0:
            if events[i][0][-7:] != "00:00AM":
                temp_available_slot = [events[0][0]
                                       [:-7]+"00:00AM", events[0][0]]
                if (get_duration_in_minutes(getEpochTime(temp_available_slot[0]), getEpochTime(temp_available_slot[1])) >= duration):
                    available_slots.extend(get_chunks_of_interval(temp_available_slot, duration))
                temp_event = events[0]
            continue
        # check if the next entry has overlap
        # Complete overlap end_1 > end_2
        if getEpochTime(temp_event[1]) >= getEpochTime(events[i][1]):
            continue
        # partial overlap end_1>start_1 and end_1<end_2
        elif getEpochTime(temp_event[1]) >= getEpochTime(events[i][0]) and getEpochTime(temp_event[1]) <= getEpochTime(events[i][0]):
            temp_event = [temp_event[0], events[i][1]]
        # if not overlapping then get the interval end_1-start_1
        else:
            temp_available_slot = [temp_event[1], events[i][0]]
            if (get_duration_in_minutes(getEpochTime(temp_available_slot[0]), getEpochTime(temp_available_slot[1])) >= duration):
                available_slots.extend(get_chunks_of_interval(temp_available_slot,duration))
            temp_event = events[i]
    
    if temp_event[1][-7:] != "00:00AM":
        # get next date format
        next_date = f"{temp_event[1][:-7]}00:00AM"
        next_date = getEpochTime(next_date) + datetime.timedelta(minutes=24*60)
        temp_available_slot = [temp_event[1], getStringTime(next_date)]        
        if (get_duration_in_minutes(getEpochTime(temp_available_slot[0]), getEpochTime(temp_available_slot[1])) >= duration):
            available_slots.extend(get_chunks_of_interval(temp_available_slot,duration))

    print("FINAL: ", available_slots)
    return available_slots


fetch_available_slots(60, [["2021-06-20 00:00AM", "2021-06-20 00:30AM"], [
                      "2021-06-20 11:00AM", "2021-06-20 11:30AM"], ["2021-06-20 03:00PM", "2021-06-20 04:00PM"]])