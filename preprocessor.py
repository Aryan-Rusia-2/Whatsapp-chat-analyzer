import re
import pandas as pd

import re


def find_matching_pattern(s):

    date_patterns = [
        r'\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\s-\s',  # Pattern for "yyyy-mm-dd, HH:MM - "
        r'\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}:\d{2}\s-\s',  # Pattern for "yyyy-mm-dd, HH:MM:SS - "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\]\s-\s',  # Pattern for "[yyyy-mm-dd, HH:MM] - "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\]\s',  # Pattern for "[yyyy-mm-dd, HH:MM] "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}:\d{2}]\s-\s',  # Pattern for "[yyyy-mm-dd, HH:MM:SS] - "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}:\d{2}\]\s',  # Pattern for "[yyyy-mm-dd, HH:MM:SS] "
        r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s-\s'  # Pattern for "mm/dd/yy, HH:MM"
        # Add more patterns as needed
    ]

    for pattern in date_patterns:
        if re.search(pattern, s):
            return pattern
    return None
def preprocess(data, pattern):

    my_dict = {
        r'\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\s-\s' : '%Y-%m-%d, %H:%M - ',  # Pattern for "yyyy-mm-dd, HH:MM - "
        r'\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}:\d{2}\s-\s' : '%Y-%m-%d, %H:%M:%S - ',  # Pattern for "yyyy-mm-dd, HH:MM:SS - "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\]\s-\s' : '[%Y-%m-%d, %H:%M] - ',  # Pattern for "[yyyy-mm-dd, HH:MM] - "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\]\s' : '[%Y-%m-%d, %H:%M] ',  # Pattern for "[yyyy-mm-dd, HH:MM] "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}:\d{2}]\s-\s': '[%Y-%m-%d, %H:%M:%S] - ',  # Pattern for "[yyyy-mm-dd, HH:MM:SS] - "
        r'\[\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}:\d{2}\]\s' : '[%Y-%m-%d, %H:%M:%S] ',  # Pattern for "[yyyy-mm-dd, HH:MM:SS] "
        r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s-\s' : '%d/%m/%y, %H:%M - '# Pattern for "mm/dd/yy, HH:MM"
    }

    # pattern = '\d{2,4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    print(my_dict[pattern])
    print("Hello this is new line!")
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format=my_dict[pattern])

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df



