# ==========================================
# HEARTBEAT MONITOR - SOFTWARE SIMULATOR
# Educational Embedded Systems Demonstration
# ==========================================

LOW_THRESHOLD = 60
HIGH_THRESHOLD = 100


def check_heartbeat(bpm):
    print("\n" + "=" * 45)
    print("       HEARTBEAT MONITOR SYSTEM")
    print("=" * 45)

    print(f"Heart Rate : {bpm} BPM")

    if bpm < LOW_THRESHOLD:
        status = "LOW"
        led = "RED"
        buzzer = "ON"

    elif bpm > HIGH_THRESHOLD:
        status = "HIGH"
        led = "RED"
        buzzer = "ON"

    else:
        status = "NORMAL"
        led = "GREEN"
        buzzer = "OFF"

    print(f"Status     : {status}")
    print(f"LED        : {led}")
    print(f"Buzzer     : {buzzer}")

    print("=" * 45)


print("==========================================")
print("   HEARTBEAT MONITOR SOFTWARE SIMULATOR")
print("==========================================")
print()
print("Educational simulation only.")
print("Thresholds:")
print(f"LOW    : < {LOW_THRESHOLD} BPM")
print(f"NORMAL : {LOW_THRESHOLD}-{HIGH_THRESHOLD} BPM")
print(f"HIGH   : > {HIGH_THRESHOLD} BPM")
print()

while True:

    user_input = input(
        "Enter BPM (or type 'exit' to stop): "
    )

    if user_input.lower() == "exit":
        print("\nSimulator stopped.")
        break

    try:
        bpm = int(user_input)

        if bpm <= 0:
            print("Please enter a BPM greater than 0.")
            continue

        check_heartbeat(bpm)

    except ValueError:
        print("Invalid input. Please enter a number.")