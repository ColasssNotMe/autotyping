import json
import flet as ft
import pyautogui
import string
import random

# TODO: false and true is case sensitive
letters = string.ascii_letters
random.seed(10)
X = random.choices(letters, k=10)
time_interval = 0.65
times = 0


class userpage(ft.UserControl):
    def __init__(self, count, timeInt, isF12):
        super().__init__()
        self.stripCount = count
        self.stripTimeInt = timeInt
        self.stripIsF12 = isF12

    def build(self):
        self.count = ft.TextField(
            hint_text="Times (recommended:45)",
            value=self.stripCount,
        )
        self.timeInt = ft.TextField(
            hint_text="Time interval (def: 0.1)",
            value=self.stripTimeInt,
        )
        self.isF12 = ft.TextField(
            hint_text="Include mobile?",
            value=self.stripIsF12,
        )

        self.countDef = ft.TextField(hint_text="Enter default times here")
        self.timeDef = ft.TextField(hint_text="Enter default time interval here")
        self.isF12Def = ft.TextField(hint_text="Mobile on by default?")

        self.mainView = ft.Column(
            visible=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.LOGO_DEV),
                        ft.Text(
                            value="Autotyping",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.IconButton(icon=ft.icons.SETTINGS, on_click=self.settingC),
                    ],
                ),
                ft.Column(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        self.count,
                        self.timeInt,
                        self.isF12,
                        ft.FloatingActionButton(
                            icon=ft.icons.DIRECTIONS_RUN,
                            on_click=self.run,
                        ),
                    ],
                ),
            ],
        )
        self.settingView = ft.Column(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK_IOS, on_click=self.returnC
                        ),
                        ft.Text(
                            value="Settings",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.IconButton(icon=ft.icons.SAVE, on_click=self.saveC),
                    ],
                ),
                ft.Column(controls=[self.countDef, self.timeDef, self.isF12Def]),
            ],
        )
        return ft.Column(controls=[self.mainView, self.settingView])

    def shuffle_type(self):
        self.letter = string.ascii_letters + string.digits
        random.seed(10)
        self.value = self.count.value
        for _ in range(int(self.value)):
            self.shuff2()

    def shuff2(self):
        Xshuff = list(X)
        random.shuffle(Xshuff)
        Xshuff = "".join(Xshuff)
        pyautogui.hotkey("ctrl", "e")
        pyautogui.typewrite(Xshuff)
        pyautogui.press("enter")
        pyautogui.sleep(float(self.timeInt.value))

    def run(self, e):
        pyautogui.sleep(5)
        self.shuffle_type()
        if self.isF12.value == "true":
            print("complete")
            pyautogui.press("F12")
            for i in range(40):
                print(i)
                self.shuff2()

    def settingC(self, e):
        self.mainView.visible = False
        self.settingView.visible = True
        self.update()

    def returnC(self, e):
        self.mainView.visible = True
        self.settingView.visible = False
        self.update()

    def saveC(self, e):
        with open("config.txt", "w") as f:
            f.write(
                self.countDef.value
                + "\n"
                + self.timeDef.value
                + "\n"
                + self.isF12Def.value
            )
            f.close()

    def readFile(self):
        self.newfile = open("config.txt", "r")


def main(page: ft.Page):
    page.window_height = 350
    page.window_width = 500

    with open("config.txt", "r") as f:
        count = f.readline().strip()
        timeInt = f.readline().strip()
        isF12 = f.readline().strip()
        f.close()

    up = userpage(count, timeInt, isF12)
    page.add(up)


ft.app(main)
