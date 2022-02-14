from datetime import timezone, datetime

def datetime_to_unix(year, month, day):
    # datetime_to_unix(2021, 6, 1) => 1622505600.0
    current_datetime = datetime(year, month, day)
    # Minus current datetime from the time that the unix time has been counted from
    return (current_datetime - datetime(1970, 1, 1)).total_seconds()


def unix_to_datetime(unix_time):
    # unix_to_datetime(1622505700)=> ''2021-06-01 12:01am
    ts = int(unix_time/1000 if len(str(unix_time)) > 10 else unix_time) # /1000 handles milliseconds
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %l:%M%p').lower()

# Found at https://medium.datadriveninvestor.com/plot-cryptocurrency-prices-and-volumes-with-python-d466dcc2661
# Added minor changes

# No. of seconds in a day
#print(datetime_to_unix(2022, 2, 13) - datetime_to_unix(2022, 2, 12))