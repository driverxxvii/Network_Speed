import PySimpleGUI as sg
import psutil
import time
import pathlib
import os
from configparser import ConfigParser


def total_bandwidth_used(dl_start, ul_start):
    dl_now = psutil.net_io_counters().bytes_recv
    ul_now = psutil.net_io_counters().bytes_sent
    total_dl = dl_now - dl_start
    total_ul = ul_now - ul_start

    if (total_dl > 1024 ** 3) or (total_ul > 1024 ** 3):
        total_dl = round(total_dl/(1024**3), 2)
        total_ul = round(total_ul / (1024 ** 3), 2)
        suffix = "GB"
    elif (total_dl > 1024 ** 2) or (total_ul > 1024 ** 2):
        total_dl = round(total_dl / (1024 ** 2), 2)
        total_ul = round(total_ul / (1024 ** 2), 2)
        suffix = "MB"
    else:
        total_dl = round(total_dl / 1024, 2)
        total_ul = round(total_ul / 1024, 2)
        suffix = "KB"

    data_used = f"Total DL: {total_dl:05.2f} {suffix}\n" \
                f"Total UL: {total_ul:05.2f} {suffix}"

    return data_used


def get_current_bandwidth():
    dl_value = psutil.net_io_counters().bytes_recv
    ul_value = psutil.net_io_counters().bytes_sent
    time_stamp = time.time()
    return dl_value, ul_value, time_stamp


def get_bandwidth_speed(dl_delta, ul_delta, time_delta):
    dl_speed = dl_delta/time_delta
    ul_speed = ul_delta/time_delta

    if (dl_speed > 1024**2) or (ul_speed > 1024**2):
        dl_speed = round(dl_speed / (1024**2), 2)
        ul_speed = round(ul_speed / (1024 ** 2), 2)
        suffix = "MB/s"
    elif (dl_speed > 1024) or (ul_speed > 1024):
        dl_speed = round(dl_speed / 1024, 2)
        ul_speed = round(ul_speed / 1024, 2)
        suffix = "KB/s"
    else:
        dl_speed = round(dl_speed, 0)
        ul_speed = round(ul_speed, 0)
        suffix = "Bytes/s"

    bandwidth = f"Current DL/UL Speed\n" \
                f"DL Speed: {dl_speed:06.2f} {suffix}\n" \
                f"UL Speed: {ul_speed:06.2f} {suffix}"
    return bandwidth


def read_config_info(section, option):
    config = ConfigParser()
    config_file = pathlib.Path(os.getcwd()).joinpath("bandwidth_monitor.ini")
    if not config_file.exists():
        config.add_section("settings")
        config.set("settings", "window_location_x", "50")
        config.set("settings", "window_location_y", "50")
        config.set("settings", "keep_on_top", "0")

        with open(config_file, "w") as f:
            config.write(f)

    config.read(config_file)
    return config.get(section, option)


def write_config_info(section, option, value):
    config = ConfigParser()
    config_file = pathlib.Path(os.getcwd()).joinpath("bandwidth_monitor.ini")
    config.read(config_file)
    config.set(section, option, value)

    with open(config_file, "w") as f:
        config.write(f)


def gui_layout():
    x_loc = int(read_config_info("settings", "window_location_x"))
    y_loc = int(read_config_info("settings", "window_location_y"))
    on_top = bool(int(read_config_info("settings", "keep_on_top")))
    # img_data = b'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'
    # img_data = b'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'
    # img_data = b'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'
    width = 19
    layout = [
        [sg.Text("Current DL/UL Speed", key="data_speed", size=(width, 3))],
        [sg.Text("", key="total_data", size=(width, 2)),
         sg.VerticalSeparator(),
         sg.Button("Reset", key="reset")
         ],
        [sg.Text("", key="cpu", size=(width, 1)),
         sg.VerticalSeparator(),
         sg.Button("Exit", key="Exit")
         ],
        [sg.Checkbox("Keep On Top", key="on_top", enable_events=True, default=on_top)],
        # [sg.Button("Test", key="test")]
    ]

    return sg.Window("Bandwidth Monitor", layout=layout, grab_anywhere=True,
                     no_titlebar=True, alpha_channel=0.9, keep_on_top=on_top,
                     use_default_focus=False, location=(x_loc, y_loc))


def event_loop():
    sg.theme("Topanga")
    window = gui_layout()
    dl_start = psutil.net_io_counters().bytes_recv
    ul_start = psutil.net_io_counters().bytes_sent

    while True:
        old_dl, old_ul, start_time = get_current_bandwidth()

        event, values = window.read(1000)

        new_dl, new_ul, end_time = get_current_bandwidth()

        dl_delta = new_dl-old_dl
        ul_delta = new_ul-old_ul
        time_delta = end_time-start_time

        data_speed = get_bandwidth_speed(dl_delta, ul_delta, time_delta)
        window["data_speed"].update(data_speed)

        total_data = total_bandwidth_used(dl_start, ul_start)
        window["total_data"].update(total_data)

        cpu = psutil.cpu_percent()
        cpu = f"CPU Usage: {cpu}%"
        window["cpu"].update(cpu)

        if event in (None, "Exit"):
            (x, y) = window.current_location()
            write_config_info("settings", "window_location_x", str(x))
            write_config_info("settings", "window_location_y", str(y))
            break

        if event == "reset":
            dl_start = psutil.net_io_counters().bytes_recv
            ul_start = psutil.net_io_counters().bytes_sent

        if event == "on_top":
            if values["on_top"]:
                window.TKroot.wm_attributes("-topmost", 1)
                write_config_info("settings", "keep_on_top", "1")
            else:
                window.TKroot.wm_attributes("-topmost", 0)
                write_config_info("settings", "keep_on_top", "0")

        # print(time.time()-end_time)

    window.close()


event_loop()
