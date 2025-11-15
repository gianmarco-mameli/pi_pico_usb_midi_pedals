'''Send Sustain Pedal (CC64) messages over USB MIDI when a button is pressed.'''

import board
import busio
import digitalio
import usb_midi
import adafruit_midi

from adafruit_midi.control_change import ControlChange

MIDI_CHANNEL = 1
CC = 64
CC_MIN = 0
CC_MAX = 127

board_led = digitalio.DigitalInOut(board.LED)
board_led.direction = digitalio.Direction.OUTPUT
BOARD_LED_ENABLED = True

led = digitalio.DigitalInOut(board.GP9)
led.direction = digitalio.Direction.OUTPUT

sus = digitalio.DigitalInOut(board.GP27)
sus.pull = digitalio.Pull.UP
uart = busio.UART(
    tx=board.GP4, rx=board.GP5, baudrate=31250, timeout=0.001)  # UART Midi device on pin 6
uart_midi = adafruit_midi.MIDI(midi_out=uart, out_channel=MIDI_CHANNEL - 1)
usb_midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=MIDI_CHANNEL - 1)

print("Code start")
print(f"MIDI Channel: {MIDI_CHANNEL}")
print(f"CC: {CC} (Sustain Pedal)")
print(f"Initial Sus Status: {'OPEN' if sus.value else 'CLOSED'}")

SUS_PRESSED = False

# Main loop
while True:
    if not sus.value and not SUS_PRESSED:
        SUS_PRESSED = True
        led.value = True
        if BOARD_LED_ENABLED:
            board_led.value = True
        usb_midi.send(ControlChange(CC, CC_MAX))
        print(f"Sus Status: CLOSED - CC {CC} sent with value {CC_MAX}")

    elif sus.value and SUS_PRESSED:
        SUS_PRESSED = False
        led.value = False
        if BOARD_LED_ENABLED:
            board_led.value = False
        usb_midi.send(ControlChange(CC, CC_MIN))
        print(f"Sus Status: OPEN - CC {CC} sent with value {CC_MIN}")
