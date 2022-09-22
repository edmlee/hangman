from settings import *
import customtkinter as ck
import random


class Hangman():
    def __init__(self):
        ck.set_appearance_mode("dark")
        ck.set_default_color_theme("blue")

        self.window = ck.CTk()
        self.window.title("Hangman")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.minsize(WIDTH, HEIGHT)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.word_list = []
        self.word_variable = ck.StringVar()
        self.used_letters = set()
        self.status = STATUS[0]
        self.keyboard_buttons = {}

        self.load_word_list()
        self.create_frames()
        self.create_keyboard_buttons()
        self.create_side_buttons()
        self.create_labels()
        self.play_game()


    def load_word_list(self):
        try:
            with open("word_list.txt", "r") as file:
                words = file.readlines()
            for word in words:
                word = word.rstrip("\n").upper()
                if len(word) >= MIN_WORD_LENGTH:
                    self.word_list.append(word)
        except:
            print("Missing file")


    def create_frames(self):
        self.word_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.word_frame.grid(row=0, column=0, sticky="nesw")

        self.keyboard_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.keyboard_frame.grid(row=1, column=0, sticky="nesw")

        self.side_frame = ck.CTkFrame(self.window, fg_color=SIDE_BAR_COLOR)
        self.side_frame.grid(row=0, column=1, rowspan=2, sticky="nesw")


    def create_button(self, frame, text, row, column, font, command):
        button = ck.CTkButton(frame, text=text, border_width=BORDER_WIDTH,
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=font, command=command)
        button.grid(row=row, column=column, sticky="nesw")
        return button


    def create_keyboard_buttons(self):
        row = 0
        column = 0
        i = 0
        for letter in ALPHABET:
            if column == len(ALPHABET) / 2:
                row += 1
                column = 0
            self.keyboard_buttons[i] = self.create_button(self.keyboard_frame, text=letter, row=row, column=column, font=KEYBOARD_FONT, 
                                                          command= lambda letter=letter: self.update_word(letter))
            self.keyboard_buttons[i].configure(height=BUTTON_HEIGHT)
            self.keyboard_frame.columnconfigure(column, weight=1)
            column += 1
            i += 1


    def create_side_buttons(self):
        self.new_game_button = self.create_button(self.side_frame, text="New Game", row=0, column=0, 
                                             font=KEYBOARD_FONT, command=self.play_game)
        self.new_game_button.configure(fg_color=GREEN, text_color=INNER_TEXT_COLOR, hover_color=GREEN_HOVER_COLOR)
        
        self.quit_button = self.create_button(self.side_frame, text="Quit", row=5, column=0, 
                                         font=KEYBOARD_FONT, command=self.window.quit)
        self.quit_button.configure(fg_color=RED, text_color=INNER_TEXT_COLOR, hover_color=RED_HOVER_COLOR)


    def create_labels(self):
        self.lives = NUMBER_OF_LIVES

        self.word_label = ck.CTkLabel(self.word_frame, textvariable=self.word_variable, text_font=WORD_FONT)
        self.word_label.grid(row=0, column=0)
        self.word_label.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

        self.lives_text_label = ck.CTkLabel(self.side_frame, width=1, text=f"Lives: {self.lives}", text_font=KEYBOARD_FONT)
        self.lives_text_label.grid(row=1, column=0, pady=20)

    
    def new_game(self):
        self.status = STATUS[0]
        self.lives = NUMBER_OF_LIVES
        self.lives_text_label.configure(text=f"Lives: {self.lives}")
        for keys in self.keyboard_buttons:
            self.keyboard_buttons[keys].configure(state=ck.NORMAL)


    def play_game(self):
        self.new_game()        
        self.secret_word = random.choice(self.word_list)
        word = "_ " * len(self.secret_word)
        self.word_variable.set(word.strip())
        print(self.secret_word)


    def update_word(self, letter):
        word = self.word_variable.get().split(" ")
        for index, char in enumerate(self.secret_word):
            if letter == char:
                word[index] = letter
        self.word_variable.set(" ".join(word))
        self.update_lives(word, letter)


    def update_lives(self, word, letter):
        if letter not in self.used_letters and self.status == STATUS[0]:
            self.used_letters.add(letter)
            if letter not in self.secret_word:
                self.lives -= 1
            self.lives_text_label.configure(text=f"Lives: {self.lives}")
            print(self.used_letters)
        if self.lives == 0:
            self.status = STATUS[1]
            print(self.status)
        elif set(word).issubset(self.used_letters):
            self.status = STATUS[2]
            print(self.status)
        if self.status == STATUS[1] or self.status == STATUS[2]:
            for keys in self.keyboard_buttons:
                self.keyboard_buttons[keys].configure(state=ck.DISABLED)


    def select_difficulty(self):
        pass


if __name__ == "__main__":
    hangman = Hangman()
    hangman.window.mainloop()
    