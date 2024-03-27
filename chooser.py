import tkinter as tk
from model import RecordMode


class Chooser:
    def __init__(self, root):
        self.root = root
        self.root.geometry('400x200')
        self.model_instance = RecordMode()
        self.root.title("Choose Mode")
        self.mode_var = tk.IntVar()
        self.mode_var.set(1)  # Значение по умолчанию

        mode_label = tk.Label(self.root, text="Choose the mode:")
        mode_label.pack()

        video_mode_radio = tk.Radiobutton(self.root, text="Real-time Video Mode", variable=self.mode_var, value=1)
        video_mode_radio.pack()

        record_mode_radio = tk.Radiobutton(self.root, text="Record Mode", variable=self.mode_var, value=2)
        record_mode_radio.pack()

        start_button = tk.Button(self.root, text="Start", command=self.start_selected_mode)
        start_button.pack()

    def start_selected_mode(self):
        selected_mode = self.mode_var.get()
        if selected_mode == 1:

            #  здесь код для запуска реального времени

            self.model_instance.real_time()

        elif selected_mode == 2:

            # здесь код для запуска записи

            self.model_instance.record_mode()


if __name__ == "__main__":
    root = tk.Tk()
    chooser = Chooser(root)
    root.mainloop()
