from datetime import datetime, time
from datetime import timedelta

import arrow
import pytz

loc_tz = pytz.timezone('Asia/Shanghai')
utc_tz = pytz.timezone('UTC')


def str2str_by_format(dt_str, dt_format='%Y-%m-%d %H:%M:%S'):
    return arrow.get(dt_str).astimezone(tz=loc_tz).strftime(dt_format)


def str2datetime_by_format(dt_str, dt_format='%Y-%m-%d %H:%M:%S'):
    '''
    时间字符串转datetime
    '''
    return loc_tz.localize(datetime.strptime(dt_str, dt_format))
    # return arrow.get(dt_str).astimezone(tz=loc_tz).strftime(dt_format)


def datetime2str_by_format(dt=None, dt_format='%Y-%m-%d %H:%M:%S'):
    '''
    本地datetime转本地字符串
    '''
    if not dt:
        dt = now()
    return dt.astimezone(loc_tz).strftime(dt_format)


def date2str(dt, dt_format='%Y-%m-%d'):
    '''
    日期转字符串
    '''
    if not dt:
        dt = now()
    return dt.strftime(dt_format)


def str2date(dt_str):
    '''
    字符串转日期
    '''
    dt = str2datetime_by_format(dt_str, '%Y-%m-%d')
    return dt.date()


def date2datetime(dt):
    return today().replace(year=dt.year, month=dt.month, day=dt.day)


def datetime2date_range(dt):
    '''
    datetime转换成一天的开始和结束时间[start, end)
    '''
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def now():
    return datetime.utcnow().replace(tzinfo=utc_tz).astimezone(loc_tz)


def now_str():
    return datetime2str_by_format()


def utc_now():
    return datetime.utcnow()


def today():
    dt = now()
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt


def tomorrow():
    return today() + timedelta(days=1)


def yesterday():
    return today() - timedelta(days=1)


def total_seconds(begin_time, end_time):
    return (arrow.get(end_time).astimezone(tz=loc_tz) - arrow.get(begin_time).astimezone(tz=loc_tz)).total_seconds()


def add_local_tz(time_utc):
    return arrow.get(time_utc, tzinfo=loc_tz)


def last_time(seconds):
    current_time = datetime.now(tz=utc_tz) - timedelta(seconds=seconds)
    return current_time.replace(tzinfo=utc_tz).astimezone(loc_tz)


def next_time(hours):
    current_time = datetime.now(tz=utc_tz) + timedelta(hours=hours)
    return current_time.replace(tzinfo=utc_tz).astimezone(loc_tz)


if __name__ == "__main__":
    print(datetime2str_by_format(dt_format='%Y%m%d%H%M%S'))
