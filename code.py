import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import serial
import threading
from PIL import Image, ImageTk


def update_radar():
    try:
        azimuth = float(azimuth_entry.get())
        inclination = float(inclination_entry.get())

        if not (0 <= azimuth <= 360 and 0 <= inclination <= 90):
            raise ValueError("Angles out of range")

        
        azimuth_rad = math.radians(azimuth)
        inclination_rad = math.radians(inclination)

        
        length = 90  # Length of the radar hand
        x_end = 100 + length * math.cos(azimuth_rad) * math.sin(inclination_rad)
        y_end = 100 - length * math.sin(azimuth_rad) * math.sin(inclination_rad)

        
        radar_clock_canvas.delete("hand")

        
        radar_clock_canvas.create_line(100, 100, x_end, y_end, fill="blue", width=2, tags="hand")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

class SerialConfigApp:
    def __init__(self, root):
        self.root = root
        self.serial_connection = None
        self.create_tabs()

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        self.home_frame = tk.Frame(self.notebook, bg="white")
        self.config_frame = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.home_frame, text='Home')
        self.notebook.add(self.config_frame, text='Configure')

        self.create_home_layout()
        self.create_config_layout()

    def create_home_layout(self):
        global azimuth_entry, inclination_entry, radar_clock_canvas

        logo_image = Image.open("C:\\Users\\aryak\\Downloads\\DRDO.jpeg")  # Update the path to your DRDO logo image
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(self.home_frame, image=logo_photo)
        logo_label.image = logo_photo 
        logo_label.grid(row=0, column=0, padx=20, pady=20, rowspan=2)


        title_frame = tk.Frame(self.home_frame, bg="white")
        title_frame.grid(row=0, column=1, padx=60, pady=20, columnspan=2, sticky="w")
        title_label = tk.Label(title_frame, text="Impulsive Sound Detection System", font=("Helvetica", 14), justify="center")
        title_label.pack()

        
        gray_bar = tk.Frame(self.home_frame, bg="gray", height=20)
        gray_bar.grid(row=1, column=1, padx=20, pady=20, columnspan=2, sticky="we")

        
        azimuth_label = tk.Label(self.home_frame, text="Azimuth angle :", font=("Helvetica", 12))
        azimuth_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        azimuth_entry = tk.Entry(self.home_frame)
        azimuth_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    
        inclination_label = tk.Label(self.home_frame, text="Elevation Angle :", font=("Helvetica", 12))
        inclination_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        inclination_entry = tk.Entry(self.home_frame)
        inclination_entry.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    
        radar_clock_frame = tk.Frame(self.home_frame, bg="white", height=200, width=200)
        radar_clock_frame.grid(row=2, column=2, rowspan=2, padx=20, pady=20, sticky="n")
        radar_clock_label = tk.Label(radar_clock_frame, text="RADAR CLOCK", font=("Helvetica", 12))
        radar_clock_label.pack(side="bottom")
        radar_clock_canvas = tk.Canvas(radar_clock_frame, width=200, height=200)
        radar_clock_canvas.create_oval(10, 10, 190, 190, outline="black")
        radar_clock_canvas.pack()

    
        update_button = tk.Button(self.home_frame, text="Update Radar", command=update_radar)
        update_button.grid(row=4, column=0, columnspan=3, pady=20)

    def create_config_layout(self):
    
        self.port_label = tk.Label(self.config_frame, text="Port:", font=("Helvetica", 12))
        self.port_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.port_options = ["COM1", "COM2", "COM3", "COM4"]  # Update with actual available ports
        self.port_var = tk.StringVar(value=self.port_options[0])
        self.port_menu = ttk.Combobox(self.config_frame, textvariable=self.port_var, values=self.port_options)
        self.port_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.baud_label = tk.Label(self.config_frame, text="Baud Rate:", font=("Helvetica", 12))
        self.baud_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.baud_options = [9600, 19200, 38400, 57600, 115200]  # Common baud rates
        self.baud_var = tk.IntVar(value=self.baud_options[0])
        self.baud_menu = ttk.Combobox(self.config_frame, textvariable=self.baud_var, values=self.baud_options)
        self.baud_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.parity_label = tk.Label(self.config_frame, text="Parity:", font=("Helvetica", 12))
        self.parity_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.parity_options = ["None", "Even", "Odd", "Mark", "Space"]
        self.parity_var = tk.StringVar(value=self.parity_options[0])
        self.parity_menu = ttk.Combobox(self.config_frame, textvariable=self.parity_var, values=self.parity_options)
        self.parity_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.stopbits_label = tk.Label(self.config_frame, text="Stop Bits:", font=("Helvetica", 12))
        self.stopbits_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.stopbits_options = [1, 1.5, 2]
        self.stopbits_var = tk.DoubleVar(value=self.stopbits_options[0])
        self.stopbits_menu = ttk.Combobox(self.config_frame, textvariable=self.stopbits_var, values=self.stopbits_options)
        self.stopbits_menu.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.connect_button = tk.Button(self.config_frame, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=4, column=0, columnspan=2, pady=10)

        
        self.connection_status = tk.Label(self.config_frame, text="", font=("Helvetica", 12), fg="red")
        self.connection_status.grid(row=5, column=0, columnspan=2, pady=5)

        
        self.output_frame = tk.Frame(self.config_frame, bg="white")
        self.output_frame.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="n")
        self.output_text = tk.Text(self.output_frame, state='disabled', width=90, height=10)
        self.output_text.pack()

    def connect_serial(self):
        port = self.port_var.get()
        baudrate = self.baud_var.get()
        parity = self.parity_var.get()
        stopbits = self.stopbits_var.get()

        if not port or not baudrate:
            self.connection_status.config(text="Port and Baud Rate must be specified", fg="red")
            return

        parity_dict = {"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD,
                       "Mark": serial.PARITY_MARK, "Space": serial.PARITY_SPACE}
        stopbits_dict = {1: serial.STOPBITS_ONE, 1.5: serial.STOPBITS_ONE_POINT_FIVE, 2: serial.STOPBITS_TWO}

        try:
            self.serial_connection = serial.Serial(
                port=port,
                baudrate=int(baudrate),
                parity=parity_dict[parity],
                stopbits=stopbits_dict[float(stopbits)]
            )
            self.connection_status.config(text="Connected to the serial port", fg="green")
            self.read_serial_data()
        except Exception as e:
            self.connection_status.config(text=f"Failed to connect: {e}", fg="red")

    def read_serial_data(self):
        def read_thread():
            while self.serial_connection.is_open:
                try:
                    data = self.serial_connection.readline().decode('utf-8').strip()
                    self.output_text.after(0, self.update_output, data)
                except Exception as e:
                    self.serial_connection.close()
                    self.connection_status.config(text=f"Serial connection error: {e}", fg="red")
                    break

        threading.Thread(target=read_thread, daemon=True).start()

    def update_output(self, data):
        self.output_text.config(state='normal')
        self.output_text.insert('end', data + '\n')
        self.output_text.config(state='disabled')
        self.output_text.yview('end')

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialConfigApp(root)
    root.mainloop()
