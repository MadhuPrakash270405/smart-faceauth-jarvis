from datetime import time
from screen_brightness_control import set_brightness
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess
import psutil


def brightness_control():
    # Set brightness to 100% (100)
    set_brightness(display=0, value=100)


def audio_control():
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume
    currentVolumeDb = volume.GetMasterVolumeLevel()

    # volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
    volume.SetMasterVolumeLevelScalar(0.0, None)  # mute
    # volume.SetMasterVolumeLevelScalar(1.0, None)
    # NOTE: -6.0 dB = half volume !


def wifi_control():
    result = subprocess.run(
        ["netsh", "interface", "show", "interface", "Wi-Fi"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    # wifi turn off
    # subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "admin=disable"])
    # wifi turn on
    # subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "admin=enable"])


def toggle_audio(enable):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if enable:
        volume.SetMute(0, None)
        print("Audio turned on.")
    else:
        volume.SetMute(1, None)
        print("Audio turned off.")


def get_battery_status():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    if plugged:
        status = "Plugged in"
    else:
        status = "Not Plugged in"
    print(f"Charge: {percent}% | Status: {status}")


if __name__ == "__main__":
    # Test the function
    # toggle_audio(enable=False)  # To turn off
    toggle_audio(enable=True)  # To turn on
    get_battery_status()
