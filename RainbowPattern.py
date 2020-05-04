from cuesdk import CueSdk
import threading
import queue
import time
from subprocess import check_output
import operator


def get_available_leds():
    leds = list()
    device_count = sdk.get_device_count()
    for device_index in range(device_count):
        led_positions = sdk.get_led_positions_by_device_index(device_index)
        leds.append(led_positions)
    return leds

def set_color(all_leds, color):
    check_output(f".\RGBFusion.exe.lnk --setarea:-1:0:{color[0]}:{color[1]}:{color[2]}", shell=True)
    device_leds = all_leds[0]
    for led in device_leds:
        device_leds[led] = color
    sdk.set_led_colors_buffer_by_device_index(0, device_leds)
    sdk.set_led_colors_flush_buffer()


def get_difference(start, end, step):
    if start == end:
        return 0
    print(f'Start: {start}, end: {end}')
    if start > end:
        if start - end > step:
            return -step
        else:
            return end - start

    if start < end:
        if end - start > step:
            return step
        else:
            return end - start


def transition(leds, start, end, step):
    pic = start
    while end != pic:
        print(pic)
        r = get_difference(pic[0], end[0], step)
        g = get_difference(pic[1], end[1], step)
        b = get_difference(pic[2], end[2], step)

        pic = (tuple(map(operator.add, pic, (r,g,b))))
        set_color(leds, pic)


def main():
    global sdk
    sdk = CueSdk()
    connected = sdk.connect()
    if not connected:
        err = sdk.get_last_error()
        print("Handshake failed: %s" % err)
        return

    wave_duration = 500
    colors = get_available_leds()
    if not colors:
        return

    step = 20
    while(True):
        transition(colors, (255,0,0), (255,255,0), step)
        transition(colors, (255,255,0), (0,255,0), step)
        transition(colors, (0,255,0), (0,255,255), step)
        transition(colors, (0,255,255), (0,0,255), step)
        transition(colors, (0,0,255), (255,0,255), step)
        transition(colors, (255,0,255), (255,0,0), step)

if __name__ == "__main__":
    main()