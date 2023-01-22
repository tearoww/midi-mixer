from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import threading
import pulsectl
import rtmidi  # Required by mido
import mido


def about():
    license_text = (
        "MIDI Mixer allows you to use your MIDI devices' Control Change messages to adjust application volumes.\n"
        "Copyright (C) 2023 Tearow\n\n"

        "This program is free software: you can redistribute it and/or modify "
        "it under the terms of the GNU General Public License as published by "
        "the Free Software Foundation, either version 3 of the License, or "
        "(at your option) any later version.\n\n"

        "This program is distributed in the hope that it will be useful, "
        "but WITHOUT ANY WARRANTY; without even the implied warranty of "
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
        "GNU General Public License for more details.\n\n"

        "You should have received a copy of the GNU General Public License "
        "along with this program. If not, see https://www.gnu.org/licenses/.")

    messagebox.showinfo("About", license_text)


def get_ports():
    return mido.get_input_names()


def get_sink_inputs():
    with pulsectl.Pulse("midi-mixer") as pulse:
        return pulse.sink_input_list()


def splitter(old_list, type_of_list):
    new_list = []

    for item in old_list:
        if type_of_list == "sink input":
            new_list.append(str(item).split("'")[1])
        else:
            new_list.append(item.split(":")[1])

    return new_list


class Control:
    def __init__(self, frame, ports, rows):
        self.rows = rows
        self.frame = frame
        self.ports = ports
        self.channel_id = 127
        self.sink_inputs = get_sink_inputs()
        self.split_ports = splitter(self.ports, "port")
        self.device_label = tk.Label(frame, text="Select device:")
        self.split_sink_inputs = splitter(self.sink_inputs, "sink input")

        self.device_combobox = ttk.Combobox(
            self.frame,
            values=self.split_ports,
            state="readonly",
            postcommand=lambda: self.device_combobox.configure(values=splitter(get_ports(), "port")))

        self.control_label = tk.Label(self.frame, text="No control hooked")
        self.control_button = tk.Button(self.frame, text="Hook control", command=self.hook_thread)
        self.input_label = tk.Label(self.frame, text="Select sink input:")

        self.input_combobox = ttk.Combobox(
            self.frame,
            values=self.split_sink_inputs,
            state="readonly",
            postcommand=lambda: self.input_combobox.configure(values=splitter(get_sink_inputs(), "sink input")))

        self.device_label.grid(row=self.rows, column=1)
        self.device_combobox.grid(row=self.rows, column=2)
        self.control_label.grid(row=self.rows, column=3)
        self.control_button.grid(row=self.rows, column=4)
        self.input_label.grid(row=self.rows, column=5)
        self.input_combobox.grid(row=self.rows, column=6)
        self.input_combobox.bind("<<ComboboxSelected>>", self.volume_thread)

    def hook_thread(self):
        threading.Thread(target=self.hook, daemon=True).start()

    def hook(self):
        self.control_button.configure(text="Move control now...", state="disabled")

        for message in mido.open_input(self.ports[self.device_combobox.current()]):
            self.channel_id = int(str(message).split(" ")[1].split("=")[1]) + 1

            self.control_label.configure(text="Control channel ID: " + str(self.channel_id))
            self.control_button.configure(text="Hook control", state="normal")
            break

    def volume_thread(self, event_object):
        threading.Thread(target=self.volume, daemon=True).start()

    def volume(self):
        port = self.ports[self.device_combobox.current()]
        sink_input = get_sink_inputs()[self.input_combobox.current()]

        with pulsectl.Pulse("midi-mixer") as pulse:
            for message in mido.open_input(port):
                channel_id = int(str(message).split(" ")[1].split("=")[1]) + 1
                control_value = int(str(message).split(" ")[3].split("=")[1]) / 100

                if channel_id == self.channel_id:
                    pulse.volume_set_all_chans(sink_input, control_value)


class MIDIMixer:
    def __init__(self):
        self.rows = 1
        self.root = tk.Tk()
        self.ports = get_ports()
        self.frame = tk.Frame(self.root)
        self.menubar = tk.Menu(self.root)
        self.sink_inputs = get_sink_inputs()
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.first_control = Control(self.frame, self.ports, 0)
        self.new_control_button = tk.Button(self.frame, text="+", command=self.new_control)

    def new_control(self):
        if self.rows < 18:
            Control(self.frame, self.ports, self.rows)

            self.rows += 1
            self.new_control_button.grid(row=self.rows + 1, column=0)
        else:
            self.new_control_button.grid_forget()

    def main(self):
        self.root.title("MIDI Mixer")
        self.root.geometry("800x600")
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.help_menu.add_command(label="About", command=about)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.frame.pack(padx=10, pady=10)
        self.new_control_button.grid(row=1, column=0)
        self.root.config(menu=self.menubar)
        self.root.mainloop()


if __name__ == '__main__':
    MIDIMixer().main()
