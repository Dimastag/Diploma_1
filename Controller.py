import tkinter as tk
import model


class Chooser:
    def __init__(self, root):
        self.root = root
        self.root.title("Choose Mode")

        self.mode_var = tk.IntVar()
        self.mode_var.set(1)  # Устанавливаем значение по умолчанию

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
            print("Starting Real-time Video Mode")
            #  здесь код для запуска реального времени
            model.Model.open_video(self)
            model.Model.video_processing(self)
        elif selected_mode == 2:
            print("Starting Record Mode")
            # здесь код для запуска записи


if __name__ == "__main__":
    root = tk.Tk()
    chooser = Chooser(root)
    root.mainloop()
