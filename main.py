import psutil
from datetime import datetime
import time
import json
import os

current_date = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = f"logs/{current_date}.json"

def list_processes():
    current_processes = {}
    loaded_processes = {}
    new_processes = {}

    # load log file
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            if os.stat(LOG_FILE).st_size != 0:
                loaded_processes = json.load(f)

    # current processes, this gets the highest uptime of multiple same processes (e.g. multiple notepad.exe)
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            info = proc.info

            # skip if username is None
            # if info['username'] is None:
            #     continue

            # skip if not "Notepad.exe"
            # if info['name'] != "Notepad.exe":
            #     continue

            pid = info['pid']
            name = info['name']

            start_time = datetime.fromtimestamp(info['create_time'])
            uptime = datetime.now() - start_time
            total_seconds = uptime.total_seconds()

            if name not in current_processes or total_seconds > float(current_processes[name]['uptime_seconds']):
                current_processes[name] = {
                    'pid': pid,
                    'uptime_seconds': total_seconds,
                    'uptime_seconds_old': total_seconds
                }

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # add current processes that are not in the loaded_processes to new_processes
    loaded_processes_set = set(loaded_processes)
    new_processes = {name: process for name, process in current_processes.items() if name not in loaded_processes_set}
    current_pids = {process['pid'] for process in current_processes.values()}

    # process calculation
    # same process: (current - loaded_current_old) + loaded
    # different process: current + loaded

    for name, process in loaded_processes.items():
        loaded_pid = process['pid']
        loaded_uptime_seconds = process['uptime_seconds']
        loaded_uptime_seconds_old = process['uptime_seconds_old']

        # same process
        if name in current_processes and loaded_pid in current_pids:
            current_uptime_seconds = current_processes[name]['uptime_seconds']
            offset_uptime_seconds = current_uptime_seconds - loaded_uptime_seconds_old
            new_processes[name] = {
                'pid': loaded_pid,
                'uptime_seconds': offset_uptime_seconds + loaded_uptime_seconds,
                'uptime_seconds_old': current_uptime_seconds
            }

        # different process
        elif name in current_processes and loaded_pid not in current_pids:
            current_uptime_seconds = current_processes[name]['uptime_seconds']
            new_processes[name] = {
                'pid': current_processes[name]['pid'],
                'uptime_seconds': current_uptime_seconds + loaded_uptime_seconds,
                'uptime_seconds_old': current_uptime_seconds
            }

        # not in current processes (might be closed)
        else:
            new_processes[name] = {
                'pid': loaded_pid,
                'uptime_seconds': loaded_uptime_seconds,
                'uptime_seconds_old': loaded_uptime_seconds_old
            }

    with open(LOG_FILE, "w") as f:
        json.dump(new_processes, f, indent=4)

if __name__ == "__main__":
    while True:
        list_processes()
        time.sleep(30)