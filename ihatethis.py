import pyautogui
import string
import random
import customtkinter as ctk
import threading
import json
import github
import semver
import webbrowser

# check for update
repo = "ColasssNotMe/autotyping"
g = github.Github()
releases = g.get_repo(repo).get_releases()

latest_release = releases[0]
latest_version = latest_release.tag_name

current_version = "2.4.0"

latest_semver = semver.VersionInfo.parse(latest_version)
current_semver = semver.VersionInfo.parse(current_version)

##testing purpose only
# latest_version = "2.4.0"
# current_version = "2.3.0"
# latest_semver = semver.VersionInfo.parse("2.3.0")
# current_semver = semver.VersionInfo.parse("2.2.0")

letters = string.ascii_lowercase
random.seed(10)

# time_interval = 0.65
times = 0
ctk.set_default_color_theme("green")


class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.InspectCount = 0
        # create tabs
        self.add("Main Tab")
        self.add("Settings")


class App(ctk.CTk):
    # init json file
    with open("config.json", "w") as f:
        data = {"normal": "35", "startTime": "0", "endTime": "1"}
        json.dump(data, f)

    def save_settings(self):
        super().__init__()
        normal = self.defcount_entry.get()
        startTime = self.deftime_entry_start.get()
        endTime = self.deftime_entry_end.get()
        userInput = {
            "normal": normal,
            "startTime": startTime,
            "endTime": endTime,
        }

        with open("config.json", "w+") as f:
            json.dump(userInput, f)
            f.close()

    def shuffle_and_type(self):
        X = random.choices(letters, k=random.randint(1, 25))
        Xshuff = list(X)
        random.shuffle(Xshuff)
        Xshuff = "".join(Xshuff)
        pyautogui.hotkey("ctrl", "e")
        typingSpeed = random.uniform(
            int(self.entry_time_start.get()), int(self.entry_time_end.get())
        )
        pyautogui.typewrite(Xshuff, interval=typingSpeed)
        pyautogui.press("enter")

    def F12(self, InspectElement, InspectCount):
        if InspectElement == 1:
            pyautogui.press("F12")
            while InspectCount < 30:
                InspectCount += 1
                self.shuffle_and_type()
            self.running_label.configure(text="Stopped", text_color="red")
        else:
            self.running_label.configure(text="Stopped", text_color="red")

    def auto(self, Tnum, InspectElement):
        for _ in range(int(Tnum)):
            self.shuffle_and_type()
        self.F12(InspectElement, 0)

    def get_value(self):
        self.running_label.configure(text="Running", text_color="green")
        pyautogui.sleep(5)
        Tnum = self.ENTRY_COUNT.get()
        InspectElement = self.ENTRY_INSPECT_ELEMENT.get()
        self.auto(Tnum, InspectElement)

    def start_thread(self):
        thread = threading.Thread(target=self.get_value)
        thread.start()

    def destroy(self):
        self.tab_view.destroy()
        self.after_cancel(RecursionError)
        self.quit()
        super().destroy()

    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("Python autotyping script")
        self.tab_view = MyTabView(master=self, width=650, height=350)
        self.tab_view.grid(row=0, column=0, padx=30, pady=40)

        self.newfile = open("config.json", "a")

        def closeUpdateTab():
            updateWindow.destroy()
            updateWindow.update()

        if latest_semver > current_semver:
            print("There is a new release available:", latest_version)
            updateWindow = ctk.CTkToplevel()
            updateWindow.title("Update Available")
            updateWindow.geometry("300x100")
            updateWindow.resizable(False, False)
            updateText = ctk.CTkLabel(updateWindow, text="New release available")
            updateText.pack()
            updateButton = ctk.CTkButton(
                updateWindow,
                text="Update",
                command=lambda: [
                    webbrowser.open("https://github.com/ColasssNotMe/autotyping"),
                    closeUpdateTab(),
                ],
            )
            updateButton.pack()

        else:
            print("No new releases available")

        self.LABEL = ctk.CTkLabel(
            self,
            text="Python autotyping script",
            width=50,
            height=20,
            font=("Comic Sans", 20),
        )
        self.LABEL.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        self.LABEL_COUNT = ctk.CTkLabel(
            self.tab_view.tab("Main Tab"),
            text=("Enter the number of random text generated in the entry below"),
            font=("Comic Sans", 15),
        )
        self.LABEL_COUNT.place(relx=0.1, rely=0.2)

        self.LABEL_INSPECT_ELEMENT = ctk.CTkLabel(
            self.tab_view.tab("Main Tab"),
            text=("Do you want to do the same with mobile?"),
            font=("Comic Sans", 15),
        )
        self.LABEL_INSPECT_ELEMENT.place(relx=0.1, rely=0.5)

        self.LABEL_TIME = ctk.CTkLabel(
            self.tab_view.tab("Main Tab"),
            text="Insert the time interval between each text generated",
            font=("Comic Sans", 15),
        )
        self.LABEL_TIME.place(relx=0.1, rely=0.8)

        self.ENTRY_COUNT = ctk.CTkEntry(
            self.tab_view.tab("Main Tab"), placeholder_text="enter a number here "
        )
        self.ENTRY_COUNT.place(relx=0.1, rely=0.32)

        self.ENTRY_INSPECT_ELEMENT = ctk.CTkSwitch(
            self.tab_view.tab("Main Tab"), text=""
        )
        self.ENTRY_INSPECT_ELEMENT.select()
        self.ENTRY_INSPECT_ELEMENT.place(relx=0.1, rely=0.58)

        self.entry_time_start = ctk.CTkEntry(self.tab_view.tab("Main Tab"), width=10)
        self.entry_time_start.place(relx=0.1, rely=0.9)
        self.text = ctk.CTkLabel(self.tab_view.tab("Main Tab"), text="to")
        self.text.place(relx=0.15, rely=0.9)
        self.entry_time_end = ctk.CTkEntry(self.tab_view.tab("Main Tab"), width=10)
        self.entry_time_end.place(relx=0.20, rely=0.9)

        # settings tab
        self.defcount_label = ctk.CTkLabel(
            self.tab_view.tab("Settings"), text="Set Default Count to:"
        )
        self.defcount_label.place(relx=0.1, rely=0.1)

        self.defcount_entry = ctk.CTkEntry(self.tab_view.tab("Settings"))
        self.defcount_entry.place(relx=0.1, rely=0.2)

        self.deftime_label = ctk.CTkLabel(
            self.tab_view.tab("Settings"),
            text='Time interval changed, check "Main Tab"',
        )
        self.deftime_label.place(relx=0.1, rely=0.7)

        self.deftime_entry_start = ctk.CTkEntry(self.tab_view.tab("Settings"), width=10)
        self.deftime_entry_end = ctk.CTkEntry(self.tab_view.tab("Settings"), width=10)
        self.deftime_entry_start.place(relx=0.1, rely=0.8)
        self.deftime_entry_end.place(relx=0.2, rely=0.8)

        self.text = ctk.CTkLabel(self.tab_view.tab("Settings"), text="to")
        self.text.place(relx=0.15, rely=0.8)

        Save_button = ctk.CTkButton(
            self.tab_view.tab("Settings"), text="Save", command=self.save_settings
        )
        Save_button.place(relx=0.85, rely=0.86, anchor=ctk.CENTER)

        Submit_button = ctk.CTkButton(
            self.tab_view.tab("Main Tab"),
            text="Submit",
            command=self.start_thread,
        )
        Submit_button.place(relx=0.85, rely=0.86, anchor=ctk.CENTER)

        self.status = ctk.CTkLabel(self.tab_view.tab("Main Tab"), text="Status:")
        self.status.place(relx=0.8, rely=0.10, anchor=ctk.CENTER)

        self.running_label = ctk.CTkLabel(
            self.tab_view.tab("Main Tab"), text="Idle", text_color="grey"
        )
        self.running_label.place(relx=0.9, rely=0.1, anchor=ctk.CENTER)

        self.progressbar = ctk.CTkProgressBar

        with open("config.json", "r") as file:
            data = json.load(file)
            self.ENTRY_COUNT.insert(0, data["normal"])
            self.entry_time_start.insert(0, data["startTime"])
            self.entry_time_end.insert(0, data["endTime"])


app = App()
app.resizable(width=False, height=False)
app.mainloop()
