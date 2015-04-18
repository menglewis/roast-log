from datetime import datetime


def convert_times_to_second_diff(time1, time2):
    """
    Takes 2 time strings in the format "hh:mm:ss P" and calculates the difference in seconds
    :param time1:
    :param time2:
    :return int: seconds
    """
    start = datetime.strptime(time1, "%I:%M:%S %p")
    end = datetime.strptime(time2, "%I:%M:%S %p")
    return (end - start).seconds
