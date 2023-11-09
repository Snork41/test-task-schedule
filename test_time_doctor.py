# Тестовое задание.

# Код формирует список свободных окон в расписании рабочего дня доктора.
# Адаптивен под изменения времени начала и конца рабочего дня,
# длину свободного окна и списка busy.
# Интервалы короче длины свободного окна и не входящие в перерывы (busy)
# не регистрируются, но учитываются.


from datetime import time, timedelta
from pprint import pprint


def check_list(busy):
    """Отбрасывает перерывы вне рабочего дня."""
    checked_list = busy.copy()
    for timestamp in checked_list :
        if str(end_work)[:-3] < timestamp['start'] or str(start_work)[:-3] > timestamp['start']:
            busy.remove(timestamp)
    return busy


def interval_splitting(interval, windows_list, start_work):
    """Нарезка свободных окон."""
    if interval.seconds > free_window.second:
        amount_windows_in_interval = int(interval.seconds / 60 // free_window.minute)
        start_time_window = timedelta(hours=start_work.hour, minutes=start_work.minute)
        for window in range(amount_windows_in_interval):
            windows_list.append(
                f'Свободное окно: c {str(start_time_window)[:-3]} до {str(start_time_window + timedelta(minutes=free_window.minute))[:-3]}'
            )
            start_time_window += timedelta(minutes=free_window.minute)
    return windows_list


def first_interval(start_work, end_work):
    """Проходит по интервалу от начала рабочего дня до последнего перерыва включительно."""
    windows_list = []
    if start_work < end_work:
        for timestamp in sorted(busy, key=lambda x: x['start']):
            hour_start, minute_start = [int(x) for x in timestamp['start'].split(':')]
            hour_end, minute_end = [int(x) for x in timestamp['stop'].split(':')]
            interval = timedelta(hours=hour_start, minutes=minute_start) - timedelta(
                hours=start_work.hour, minutes=start_work.minute
            )
            windows_list = interval_splitting(interval, windows_list, start_work)
            windows_list.append(
                f'Перерыв: с {hour_start}:{minute_start} до {hour_end}:{minute_end}'
            )
            start_work = time(hour=hour_end, minute=minute_end)
    return windows_list, start_work


def last_interval(start_work, end_work):
    """Проходит по интервалу от последнего перерыва до конца рабочего дня."""
    windows_list = []
    if start_work < end_work:
        interval = timedelta(hours=end_work.hour, minutes=end_work.minute) - timedelta(
            hours=start_work.hour, minutes=start_work.minute
        )
        windows_list = interval_splitting(interval, windows_list, start_work)
    return windows_list


def main(busy, start_work, end_work):
    """Основная функция."""
    busy = check_list(busy)
    windows_list, start_work = first_interval(start_work, end_work)
    windows_list_last_interval = last_interval(start_work, end_work)
    windows_list.extend(windows_list_last_interval)
    return windows_list


if __name__ == '__main__':
    busy = [
        {'start': '10:30', 'stop': '10:50'},
        {'start': '18:40', 'stop': '18:50'},
        {'start': '14:40', 'stop': '15:50'},
        {'start': '16:40', 'stop': '17:20'},
        {'start': '20:05', 'stop': '20:20'},
    ]
    # Длинна свободных окон:
    free_window = time(minute=30)
    # Начала рабочего дня:
    start_work = time(hour=9)
    # Конец рабочего дня:
    end_work = time(hour=21)
    pprint(main(busy, start_work, end_work))
