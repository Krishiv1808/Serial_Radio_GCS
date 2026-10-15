import serial
import threading
import sys

# Change this to the ground radio's serial port.
PORT = "/dev/ttyUSB0"

# Must match the radio's configured serial baud rate.
BAUD = 57600

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



print("Laptop bridge ready.")
print("Type 'exit' to quit.")

def send_messages():
    try:
        while True:
            command = input("> ").strip()

            if command.lower() == "exit":
                break

            if command:
                radio.write((command + "\n").encode())
                radio.flush()
                print(f"Sent: {command}")

    except KeyboardInterrupt:
        sys.exit()
        
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
