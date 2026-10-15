import serial
import threading
import sys
# Change this to your radio's serial port.
# USB radio: /dev/ttyUSB0
# GPIO UART: /dev/serial0
PORT = "/dev/ttyUSB0"

# Must match the radio's configured serial baud rate.
BAUD = 57600

print(f"Opening radio on {PORT} at {BAUD} baud...")

radio = serial.Serial(
    PORT,
    BAUD,
    timeout=1
)

def receive_messages():
    while True:
        try:
            message = radio.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            if message:
                print(f"\nReceived from RPi: {message}")

        except serial.SerialException:
            break



print("drone bridge ready.")
print("Type 'exit' to quit.")

def send_messages():
    while True:
        command = input("> ").strip()
        
        if command.lower() == "exit":
            break
        if command:
            radio.write((command + "\n").encode())
            radio.flush()
            print(f"Sent: {command}")
        
recv = threading.Thread(
    target=receive_messages,
    daemon=True
)
send = threading.Thread(
    target=send_messages,
    daemon=True
)
recv.start()
send.start()

radio.close()
