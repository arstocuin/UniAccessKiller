import psutil
import os
import time
import sys

def get_all_process():
    proc_map = {}
    for proc in psutil.process_iter(['pid', 'name']):
        proc_map[proc.info['name']] = proc.info['pid']
    return proc_map

def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

def main():
    proc_list = [
        "UniAccessAgentDaemon.exe",
        "HutiehuaApp.exe",
        "Tinaiat.exe",
        "LvaNac.exe",
        "UniSensitive.exe",
        "UniAccessAgent.exe",
        "UniAccessAgentTray.exe",
    ]

    in_sub = len(sys.argv) > 1

    times = 0
    while True:
        proc_map = get_all_process()
        pid_count = sum(proc_map.get(proc_name, 0) for proc_name in proc_list)

        if in_sub:
            for proc_name in proc_list:
                pid = proc_map.get(proc_name, 0)
                terminate_process(pid)

            for proc_name in proc_list:
                pid = proc_map.get(proc_name, 0)
                print(f"Kill process: {proc_name}[{pid}]")
                kill_process(pid)
        else:
            if pid_count == 0:
                print("UniAccess is killed.")
                break

        if not in_sub:
            times += 1
            print(f"Try kill {times}...")
            time.sleep(1)
            os.system(f'python "{sys.argv[0]}" sub')
        else:
            print("Kill done...")
            sys.exit(0)

    print("Press Enter to Exit...")
    input()

if __name__ == "__main__":
    main()
