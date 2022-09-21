import customtkinter as ck
import random


KEYBOARD_FONT = ("Arial", 14)
WORD_FONT = ("Arial", 20)

WIDTH = 800
HEIGHT = 200
BUTTON_CORNER_RADIUS = 10
BORDER_WIDTH = 3
MIN_WORD_LENGTH = 3

global button_width
global button_height
global word_frame_weight

button_width = 15
button_height = button_width * 3
word_frame_weight = 0.25
ck.set_appearance_mode("dark")
ck.set_default_color_theme("blue")


class Hangman():
    def __init__(self):
        self.window = ck.CTk()
        self.window.title("Hangman")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=2)
        self.window.columnconfigure(0, weight=1)

        # Set frame dimensions
        self.word_frame_width = int(WIDTH *0.8)
        self.word_frame_height = int(HEIGHT * word_frame_weight)
        self.keyboard_frame_width = self.word_frame_width
        self.keyboard_frame_height = int(HEIGHT * (1 - word_frame_weight))
        self.side_frame_width = WIDTH - self.word_frame_width
        self.side_frame_height = HEIGHT

        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.v = ck.StringVar

        # Run widget functions
        self.word_list = self.load_word_list()
        self.word_frame = self.create_word_frame()
        self.keyboard_frame = self.create_keyboard_frame()
        self.side_frame = self.create_side_frame()
        self.create_keyboard_buttons()
        self.create_side_buttons()
        self.create_word_label()
        self.play_game()


    def load_word_list(self):
        words = []
        try:
            with open("word_list.txt", "r") as file:
                word_list = file.readlines()
            for word in word_list:
                word = word.rstrip("\n").upper()
                if len(word) >= MIN_WORD_LENGTH:
                    words.append(word)
        except:
            print("Missing file")
        return words


    def create_word_frame(self):
        frame = ck.CTkFrame(self.window, width=self.word_frame_width, height=self.word_frame_height, fg_color="black")
        frame.grid(row=0, column=0, sticky="nesw")
        return frame


    def create_keyboard_frame(self):
        frame = ck.CTkFrame(self.window, width=self.keyboard_frame_width, height=self.keyboard_frame_height, fg_color="green")
        frame.grid(row=1, column=0, sticky="nesw")
        return frame


    def create_side_frame(self):
        frame = ck.CTkFrame(self.window, width=self.side_frame_width, height=self.side_frame_height, fg_color="green")
        frame.grid(row=0, column=1, rowspan=2, sticky="nesw")
        return frame


    def create_button(self, frame, text, row, column, font, command):
        button = ck.CTkButton(frame, text=text, border_width=BORDER_WIDTH,
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=font, command=command)
        button.grid(row=row, column=column, sticky="nesw")


    def create_keyboard_buttons(self):
        row = 0
        column = 0
        for letter in self.alphabet:
            if column == len(self.alphabet) / 2:
                row += 1
                column = 0
            self.create_button(self.keyboard_frame, text=letter, row=row, column=column, 
                               font=KEYBOARD_FONT, command= lambda letter=letter: self.update_word(letter))
            self.keyboard_frame.rowconfigure(row, weight=1)
            self.keyboard_frame.columnconfigure(column, weight=1)
            column += 1


    def create_word_label(self):
        self.word_label = ck.StringVar()
        label = ck.CTkLabel(self.word_frame, textvariable=self.word_label, text_font=WORD_FONT)
        label.grid(row=0, column=0)
        label.place(relx=0.5, rely=0.5, anchor=ck.CENTER)


    def create_side_buttons(self):
        self.create_button(self.side_frame, text="Play Now", row=0, column=0, font=KEYBOARD_FONT, command=self.play_game)
        self.keyboard_frame.rowconfigure(0, weight=1)
        self.keyboard_frame.columnconfigure(0, weight=1)


    def play_game(self):
        self.secret_word = random.choice(self.word_list)
        word = "_ " * len(self.secret_word)
        word = word.strip()
        self.word_label.set(word)
        print(self.secret_word)


    def update_word(self, letter):
        word = self.word_label.get().split(" ")
        for index, char in enumerate(self.secret_word):
            if letter == char:
                word[index] = letter
        self.word_label.set(" ".join(word))
        return


if __name__ == "__main__":
    hangman = Hangman()
    hangman.window.mainloop()
    