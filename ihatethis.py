import pyautogui
import tkinter
from PIL import ImageTk
import string
import random
import customtkinter as ctk

pyautogui.PAUSE = 0.65

letters = string.ascii_letters
random.seed(10)
X = random.choices(letters, k=10)
time_interval = 0.65
times = 0


class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.InspectCount = 0
        # create tabs
        self.add("Main Tab")
        self.add("Settings")


class App(ctk.CTk):
    def save_settings(self):
        super().__init__()
        with open("config.txt", "w") as f:
            f.write(self.defcount_entry.get() + "\n" + self.deftime_entry.get())
            f.close()

    def shuffle_and_type(self):
        Xshuff = list(X)
        random.shuffle(Xshuff)
        Xshuff = "".join(Xshuff)
        pyautogui.hotkey("ctrl", "e")
        pyautogui.typewrite(Xshuff)
        pyautogui.press("enter")

    def F12(self, InspectElement, InspectCount):
        if InspectElement == "t":
            pyautogui.press("F12")
            while InspectCount < 30:
                InspectCount += 1
                self.shuffle_and_type()

    def auto(self, Tnum, InspectElement):
        for _ in range(int(Tnum)):
            self.shuffle_and_type()
        self.F1
        2(InspectElement, 0)

    def get_value(self):
        pyautogui.sleep(5)
        Tnum = self.ENTRY_COUNT.get()
        InspectElement = self.ENTRY_INSPECT_ELEMENT.get().lower()
        pyautogui.PAUSE = float(self.ENTRY_TIME.get())
        self.auto(Tnum, InspectElement)

    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("Python autotyping script")
        self.tab_view = MyTabView(master=self, width=650, height=350)
        self.tab_view.grid(row=0, column=0, padx=30, pady=40)

        self.newfile = open("config.txt", "a")

        self.LABEL = ctk.CTkLabel(
            self,
            text="Python autotyping script",
            width=50,
            height=20,
            font=("Comic Sans", 20),
        )
        self.LABEL.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)

        self.LABEL_COUNT = ctk.CTkLabel(
            self.tab_view.tab("Main Tab"),
            text=("Enter the number of random text generated in the entry below"),
            font=("Comic Sans", 15),
        )
        self.LABEL_COUNT.place(relx=0.1, rely=0.2)

        self.LABEL_INSPECT_ELEMENT = ctk.CTkLabel(
            self.tab_view.tab("Main Tab"),
            text=("Do you want to do the same with mobile? Type t=true, f=false only"),
            font=("Comic Sans", 15),
        )
        self.LABEL_INSPECT_ELEMENT.place(relx=0.1, rely=0.5)

        self.LABEL_TIME = ctk.CTkLabel(
            self.tab_view.tab("Main Tab"),
            text="Time interval (def 0.65)",
            font=("Comic Sans", 15),
        )
        self.LABEL_TIME.place(relx=0.1, rely=0.8)

        self.ENTRY_COUNT = ctk.CTkEntry(
            self.tab_view.tab("Main Tab"), placeholder_text="enter a number here "
        )
        self.ENTRY_COUNT.place(relx=0.1, rely=0.32)

        self.ENTRY_INSPECT_ELEMENT = ctk.CTkEntry(
            self.tab_view.tab("Main Tab"), placeholder_text="T / F"
        )
        self.ENTRY_INSPECT_ELEMENT.insert(0, "t")
        self.ENTRY_INSPECT_ELEMENT.place(relx=0.1, rely=0.58)

        self.ENTRY_TIME = ctk.CTkEntry(
            self.tab_view.tab("Main Tab"), placeholder_text="(def 0.65)"
        )
        self.ENTRY_TIME.place(relx=0.1, rely=0.88)

        # settings tab
        self.defcount_label = ctk.CTkLabel(
            self.tab_view.tab("Settings"), text="Set Default Count to:"
        )
        self.defcount_label.place(relx=0.1, rely=0.1)

        self.defcount_entry = ctk.CTkEntry(self.tab_view.tab("Settings"))
        self.defcount_entry.place(relx=0.1, rely=0.2)

        self.deftime_label = ctk.CTkLabel(
            self.tab_view.tab("Settings"), text="Set Default Time Interval to:"
        )
        self.deftime_label.place(relx=0.1, rely=0.7)

        self.deftime_entry = ctk.CTkEntry(self.tab_view.tab("Settings"))
        self.deftime_entry.place(relx=0.1, rely=0.8)

        Save_button = ctk.CTkButton(
            self.tab_view.tab("Settings"), text="Save", command=self.save_settings
        )
        Save_button.place(relx=0.85, rely=0.86, anchor=tkinter.CENTER)

        Submit_button = ctk.CTkButton(
            self.tab_view.tab("Main Tab"), text="Submit", command=self.get_value
        )
        Submit_button.place(relx=0.85, rely=0.86, anchor=tkinter.CENTER)

        with open("config.txt", "r") as f:
            self.ENTRY_COUNT.insert(0, f.readline().strip())
            self.ENTRY_TIME.insert(0, f.readline().strip())
            f.close()


app = App()
app.resizable(width=False, height=False)
app.mainloop()
