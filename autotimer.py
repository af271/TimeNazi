import time
import subprocess
import re

from datetime import datetime
from activity import *


form = '%Y-%m-%d'
path = 'log/'


def get_active_window():
    """Return the details about the window not just the title."""
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m is not None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match is not None:
        return match.group("name").strip(b'"').decode('UTF-8')
    return None


if __name__ == "__main__":
    active_window = get_active_window()
    start_time = datetime.now()

    today = datetime.today().strftime(form)
    filename = path + 'log_' + today + '.json'
    al = ActivityList(filename=filename)

    try:
        while True:
            time.sleep(1)

            new_window = get_active_window()
            if active_window == new_window:
                continue
            print(active_window)
            active_window = new_window

            end_time = datetime.now()
            time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0, specific=True)

            al.acts[active_window].append(time_entry)
            al.write(filename)
            start_time = datetime.now()

    except KeyboardInterrupt:
        al.write(filename)
