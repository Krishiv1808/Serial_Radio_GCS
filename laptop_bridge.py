import serial
import threading

# Ground radio's serial port
PORT = "/dev/ttyUSB0"

# Radio baud rate
BAUD = 57600

radio = serial.Serial(
    PORT,
    BAUD,
    timeout=1
)

# Shared signal to stop both threads
stop_event = threading.Event()


def receive_messages():
    while not stop_event.is_set():
        try:
            message = radio.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            if message:
                print(f"\nReceived from RPi: {message}")

        except serial.SerialException:
            stop_event.set()
            break


def send_messages():
    while not stop_event.is_set():
        try:
            command = input("> ").strip()

            if command.lower() == "exit":
                stop_event.set()
                break

            if command and not stop_event.is_set():
                radio.write((command + "\n").encode())
                radio.flush()
                print(f"Sent: {command}")

        except (EOFError, KeyboardInterrupt):
            stop_event.set()
            break


print("Laptop bridge ready.")
print("Type 'exit' to quit.")

recv = threading.Thread(
    target=receive_messages
)

send = threading.Thread(
    target=send_messages
)

recv.start()
send.start()

try:
    send.join()
finally:
    stop_event.set()
    recv.join()
    radio.close()
    print("Laptop bridge stopped.")