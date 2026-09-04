import tkinter as tk
import math


# ==========================================
# CONFIGURATION
# ==========================================

LOW_THRESHOLD = 60
HIGH_THRESHOLD = 100


# ==========================================
# HEARTBEAT MONITOR
# ==========================================

class HeartbeatMonitor:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Heartbeat Monitor & Alert System"
        )

        self.root.geometry("1000x750")

        self.root.configure(
            bg="#101114"
        )

        self.bpm = 80
        self.running = False
        self.phase = 0

        self.create_interface()

        self.animate_waveform()

    # ======================================
    # INTERFACE
    # ======================================

    def create_interface(self):

        # ---------- Header ----------

        header = tk.Frame(
            self.root,
            bg="#101114"
        )

        header.pack(
            pady=(20, 5)
        )

        tk.Label(
            header,
            text="HEARTBEAT MONITOR",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#101114"
        ).pack()

        tk.Label(
            header,
            text="Embedded Health Monitoring Prototype",
            font=("Arial", 11),
            fg="#aaaaaa",
            bg="#101114"
        ).pack(
            pady=3
        )

        # ---------- BPM Card ----------

        bpm_card = tk.Frame(
            self.root,
            bg="#181a1f",
            highlightthickness=1,
            highlightbackground="#30343b"
        )

        bpm_card.pack(
            padx=60,
            pady=15,
            fill="x"
        )

        tk.Label(
            bpm_card,
            text="CURRENT HEART RATE",
            font=("Arial", 11, "bold"),
            fg="#aaaaaa",
            bg="#181a1f"
        ).pack(
            pady=(15, 0)
        )

        self.bpm_label = tk.Label(
            bpm_card,
            text="80 BPM",
            font=("Arial", 40, "bold"),
            fg="#00e676",
            bg="#181a1f"
        )

        self.bpm_label.pack()

        self.status_label = tk.Label(
            bpm_card,
            text="NORMAL",
            font=("Arial", 17, "bold"),
            fg="#00e676",
            bg="#181a1f"
        )

        self.status_label.pack(
            pady=(0, 15)
        )

        # ---------- Indicators ----------

        indicator_frame = tk.Frame(
            self.root,
            bg="#101114"
        )

        indicator_frame.pack(
            pady=5
        )

        self.green_indicator = tk.Label(
            indicator_frame,
            text="●  NORMAL LED",
            font=("Arial", 11, "bold"),
            fg="#00e676",
            bg="#101114"
        )

        self.green_indicator.grid(
            row=0,
            column=0,
            padx=50
        )

        self.red_indicator = tk.Label(
            indicator_frame,
            text="●  ALERT LED",
            font=("Arial", 11, "bold"),
            fg="#555555",
            bg="#101114"
        )

        self.red_indicator.grid(
            row=0,
            column=1,
            padx=50
        )

        self.buzzer_indicator = tk.Label(
            indicator_frame,
            text="●  BUZZER",
            font=("Arial", 11, "bold"),
            fg="#555555",
            bg="#101114"
        )

        self.buzzer_indicator.grid(
            row=0,
            column=2,
            padx=50
        )

        # ---------- Waveform ----------

        tk.Label(
            self.root,
            text="LIVE HEARTBEAT WAVEFORM",
            font=("Arial", 11, "bold"),
            fg="#aaaaaa",
            bg="#101114"
        ).pack(
            pady=(15, 5)
        )

        self.waveform = tk.Canvas(
            self.root,
            width=850,
            height=180,
            bg="#08090b",
            highlightthickness=1,
            highlightbackground="#30343b"
        )

        self.waveform.pack(
            padx=60
        )

        # ---------- BPM Control ----------

        control_frame = tk.Frame(
            self.root,
            bg="#101114"
        )

        control_frame.pack(
            pady=15
        )

        tk.Label(
            control_frame,
            text="SIMULATED HEART RATE",
            font=("Arial", 10, "bold"),
            fg="#aaaaaa",
            bg="#101114"
        ).pack()

        self.bpm_scale = tk.Scale(
            control_frame,
            from_=40,
            to=140,
            orient="horizontal",
            length=600,
            command=self.change_bpm,
            bg="#101114",
            fg="white",
            troughcolor="#30343b",
            highlightthickness=0,
            showvalue=True
        )

        self.bpm_scale.set(80)

        self.bpm_scale.pack()

        # ---------- Buttons ----------

        button_frame = tk.Frame(
            self.root,
            bg="#101114"
        )

        button_frame.pack(
            pady=5
        )

        tk.Button(
            button_frame,
            text="START MONITORING",
            command=self.start_monitoring,
            font=("Arial", 11, "bold"),
            bg="#00a86b",
            fg="white",
            padx=25,
            pady=10,
            relief="flat"
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        tk.Button(
            button_frame,
            text="STOP",
            command=self.stop_monitoring,
            font=("Arial", 11, "bold"),
            bg="#444444",
            fg="white",
            padx=35,
            pady=10,
            relief="flat"
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        # ---------- Disclaimer ----------

        tk.Label(
            self.root,
            text=(
                "Educational prototype only — "
                "not a medical diagnostic device."
            ),
            font=("Arial", 9),
            fg="#777777",
            bg="#101114"
        ).pack(
            side="bottom",
            pady=10
        )

    # ======================================
    # BPM CONTROL
    # ======================================

    def change_bpm(self, value):

        self.bpm = int(float(value))

        if self.running:
            self.update_monitor()

    # ======================================
    # START
    # ======================================

    def start_monitoring(self):

        self.running = True

        self.update_monitor()

    # ======================================
    # STOP
    # ======================================

    def stop_monitoring(self):

        self.running = False

        self.bpm_label.config(
            text="-- BPM",
            fg="#aaaaaa"
        )

        self.status_label.config(
            text="STOPPED",
            fg="#aaaaaa"
        )

        self.green_indicator.config(
            fg="#555555"
        )

        self.red_indicator.config(
            fg="#555555"
        )

        self.buzzer_indicator.config(
            fg="#555555"
        )

    # ======================================
    # ALERT LOGIC
    # ======================================

    def update_monitor(self):

        if not self.running:
            return

        bpm = self.bpm

        # ---------- LOW ----------

        if bpm < LOW_THRESHOLD:

            self.status_label.config(
                text="LOW ALERT",
                fg="#ff3b30"
            )

            self.bpm_label.config(
                text=f"{bpm} BPM",
                fg="#ff3b30"
            )

            self.green_indicator.config(
                fg="#555555"
            )

            self.red_indicator.config(
                fg="#ff3b30"
            )

            self.buzzer_indicator.config(
                fg="#ff3b30"
            )

        # ---------- HIGH ----------

        elif bpm > HIGH_THRESHOLD:

            self.status_label.config(
                text="HIGH ALERT",
                fg="#ff3b30"
            )

            self.bpm_label.config(
                text=f"{bpm} BPM",
                fg="#ff3b30"
            )

            self.green_indicator.config(
                fg="#555555"
            )

            self.red_indicator.config(
                fg="#ff3b30"
            )

            self.buzzer_indicator.config(
                fg="#ff3b30"
            )

        # ---------- NORMAL ----------

        else:

            self.status_label.config(
                text="NORMAL",
                fg="#00e676"
            )

            self.bpm_label.config(
                text=f"{bpm} BPM",
                fg="#00e676"
            )

            self.green_indicator.config(
                fg="#00e676"
            )

            self.red_indicator.config(
                fg="#555555"
            )

            self.buzzer_indicator.config(
                fg="#555555"
            )

    # ======================================
    # HEARTBEAT WAVEFORM
    # ======================================

    def heartbeat_signal(self, x):

        # Repeating heartbeat pattern

        position = x % 100

        if position < 10:

            return 0

        elif position < 20:

            return -20 * math.exp(
                -((position - 15) ** 2) / 8
            )

        elif position < 30:

            return 55 * math.exp(
                -((position - 25) ** 2) / 3
            )

        elif position < 40:

            return -35 * math.exp(
                -((position - 35) ** 2) / 4
            )

        elif position < 55:

            return 15 * math.exp(
                -((position - 47) ** 2) / 25
            )

        else:

            return 0

    # ======================================
    # ANIMATE WAVEFORM
    # ======================================

    def animate_waveform(self):

        self.waveform.delete("all")

        width = 850
        height = 180

        center = height // 2

        points = []

        for x in range(width):

            signal_x = (
                x + self.phase
            ) * (
                self.bpm / 80
            )

            y = center + self.heartbeat_signal(
                signal_x
            )

            points.extend(
                [x, y]
            )

        if self.running:

            self.waveform.create_line(
                *points,
                fill="#00e676",
                width=2,
                smooth=True
            )

        else:

            self.waveform.create_line(
                0,
                center,
                width,
                center,
                fill="#444444",
                width=1
            )

        self.phase += 3

        self.root.after(
            40,
            self.animate_waveform
        )


# ==========================================
# APPLICATION
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = HeartbeatMonitor(root)

    root.mainloop()