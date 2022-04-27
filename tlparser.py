import time
import os

YEAR = 2022
STRIP_TIME_1 = '%I %M %p %Y %d'
STRIP_TIME_2 = '%I %M %p %Y'
TIME = 60


def parse_line(line, separator):
    logs = list()
    log = line.find(separator)
    while log != -1:
        logs.append(line[:log])
        line = line[log + len(separator):]
        log = line.find(separator)
    logs.append(line)
    return logs

def separate_log(line, get, update):
    i = line.find(get)
    while i != -1:
        line = line[:i] + \
            update + line[i + len(get):]
        i = line.find(get)
    return line

def GetTimeValue(type, hr, min, mode):
    return time.mktime(time.strptime(
        str(hr) + " " + str(min) + " " + mode + " " + str(YEAR) + " 2", STRIP_TIME_1)) if type else time.mktime(time.strptime(
            str(hr) + " " + str(min) + " " + mode + " " + str(YEAR), STRIP_TIME_2))


def GetTimePeriod(line):
    difference_time = 0
    time_list = list()
    i = line.find(":")
    while i != -1:
        time_list.append(line[:i])
        line = line[i + len(":"):]
        i = line.find(":")
    time_list.append(line)
    temp_list = time_list
    if len(temp_list) > 1 and len(temp_list[0]) <= 2:
        hour_A = int(temp_list[0])
        minute_A = int(temp_list[1][:2])
        mode_A = temp_list[1][2:4]
        hour_B = int(temp_list[1].split("-")[1])
        minute_B = int(temp_list[2][:2])
        mode_B = temp_list[2][2:4]
    elif len(temp_list) >= 3 and len(temp_list[0]) > 2:
        hour_A = int(temp_list[1])
        minute_A = int(temp_list[2][:2])
        mode_A = temp_list[2][2:4]
        hour_B = int(temp_list[2].split("-")[1])
        minute_B = int(temp_list[3][:2])
        mode_B = temp_list[3][2:4]
    list_length = len(temp_list)
    if list_length >= 3:
        t1 = GetTimeValue(False, hour_A, minute_A, mode_A)
        t2 = GetTimeValue(True, hour_B, minute_B, mode_B) if mode_A == "pm" and mode_B == "am" else GetTimeValue(
            False, hour_B, minute_B, mode_B)
        difference_time = abs(t2 - t1) / TIME
    return difference_time


def calculate_total_log(source):
    final_hours = 0
    final_minutes = 0

    source_in_read = open(os.path.join(
        os.path.dirname(__file__), "upload/"+source), "r")
    log_A = source_in_read.read().lower()
    opens = log_A.find("time log:")
    source_in_read.close()

    try:
        if opens != -1:
            log_data = log_A[opens + 10:]
            log_data = separate_log(log_data, " ", "")
            parsed_line = parse_line(log_data, "\n")
            final_time = 0
            log_line = 1
            for i in parsed_line:
                final_time += GetTimePeriod(i)
                log_line += 1

            # finding the final hours and minutes
            final_hours = int(final_time // TIME)
            final_minutes = int(final_time % TIME)
    except Exception as e:
        return ("ERROR OCCURRED - Please check the line at "+
              str(log_line) + ": "+ str(e))

    # displaying the total time logged
    return (source[:-4] + " - " + str(final_hours) +
          " hour(s) " + str(final_minutes) + " and minute(s)")
