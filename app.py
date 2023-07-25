from tkinter import *
from Word import Word
from tkinter import messagebox


class App:
    root = False

    def __init__(self):

        # Check if the window is initialized before, so that it won't be destroyed later when init is called
        if not App.root:
            self.window = Tk()
            self.window.geometry("1080x720")
            self.window.title("Word List App")
            self.window.config(padx=30, pady=20, background="#397098")
            App.root = True

        self.search_frame = Frame(self.window)
        self.search_frame.pack()

        self.input_label = Label(self.search_frame, text="Word:")
        self.input_label.pack(side=LEFT)

        self.entry = Entry(self.search_frame, width=30)
        self.entry.pack(side=LEFT)

        self.find_button = Button(self.search_frame, text="Find", command=self.find_word)
        self.find_button.pack(side=RIGHT)

        self.menu_bar = Menu(self.window)

        self.find_word_menu = Menu(self.menu_bar)
        self.word_list_menu = Menu(self.menu_bar)

        self.menu_bar.add_command(label="Find Word", command=self.show_main)
        self.menu_bar.add_command(label="Word List", command=self.show_wordlist)

        self.window.config(menu=self.menu_bar)

        self.window.mainloop()

    def show_wordlist(self):
        for widget in self.window.winfo_children():
            if widget != self.menu_bar:
                widget.destroy()

        with open("words.txt") as words:
            content = words.readlines()
        word_list = Label(text="Your Word List",
                          font=("Arial", 20, "underline"),
                          fg="#BA4949",
                          bg="#397098")
        word_list.pack(anchor="w", pady=(0, 30))

        self.main_frame = Frame(self.window, bg="#397098")
        self.main_frame.pack(fill=BOTH)

        canvas = Canvas(self.main_frame, bg="#397098", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH)

        scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=canvas.yview, bg="#397098")
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind(
            '<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        inner_frame = Frame(canvas, bg="#397098")
        for word in content:
            self.word_button = Button(inner_frame,
                                      text=word.capitalize(),
                                      font=("Arial", 25),
                                      fg="#FFFFFF",
                                      borderwidth=0,
                                      bg="#397098",
                                      activebackground="#397098",
                                      command=lambda w=word: self.show_definition(w))
            self.word_button.pack(anchor="w")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def show_definition(self, word):
        word = Word(word)
        meanings = word.get_meanings()

        for widget in self.window.winfo_children():
            if widget != self.menu_bar and widget not in self.main_frame.winfo_children() and widget != self.main_frame:
                widget.destroy()

        meaning_frame = Frame(bg="#397098")
        meaning_frame.pack(anchor="w", pady=(30, 0))

        word_label = Label(meaning_frame,
                           text=word.word.capitalize(),
                           font=("Arial", 25),
                           fg="#BA4949",
                           bg="#397098")

        word_label.pack(anchor="w")

        remove_button = Button(text="Remove", command=lambda: self.remove_from_list(word.word))
        print(word.word)
        print(word)
        remove_button.pack()

        for meaning in meanings:
            partOfSpeech_label = Label(meaning_frame,
                                       text=meaning["partOfSpeech"].capitalize(),
                                       font="Helvetica 18 italic",
                                       bg="#397098",
                                       fg="#FFFFFF",
                                       )
            partOfSpeech_label.pack(anchor="w")
            # Get only first 3 definitions
            definitions = meaning["definitions"]
            num_of_def = 2 if len(definitions) > 2 else len(definitions)

            for definition in definitions[:num_of_def]:

                def_label = Label(meaning_frame,
                                  text=f"{definitions.index(definition) + 1}. " + definition["definition"],
                                  bg="#397098",
                                  font=('Helvetica bold', 18),
                                  fg="#FFFFFF",
                                  wraplength=1000,
                                  anchor="w")

                def_label.pack(anchor="w")

                if "example" in definition:
                    example_label = Label(meaning_frame,
                                          text="Example: " + definition["example"],
                                          bg="#397098",
                                          fg="#FFFFFF",
                                          font=('Helvetica bold', 18))
                    example_label.pack(anchor="w", pady=(0, 10))

            synonyms_frame = Frame(meaning_frame, bg="#397098")
            synonyms_frame.pack(anchor="w", pady=(0, 30))

            if meaning["synonyms"]:
                synonyms_label = Label(synonyms_frame, text="Synonyms:", bg="#397098", fg="#FFFFFF",
                                       font=('Helvetica bold', 18))
                synonyms_label.pack(anchor="w", side=LEFT)

                for synonym in meaning["synonyms"][:3]:
                    synonym_label = Label(synonyms_frame, text=synonym, bg="#397098", fg="#FFFFFF",
                                          font=('Helvetica bold', 18))
                    synonym_label.pack(anchor="w", side=LEFT)

    def show_main(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.__init__()

    def find_word(self):

        word = Word(self.entry.get())
        meanings = word.get_meanings()

        for widget in self.window.winfo_children():
            if widget not in self.search_frame.winfo_children() and widget != self.search_frame and widget != self.menu_bar:
                widget.destroy()

        meaning_frame = Frame(bg="#397098")
        meaning_frame.pack(anchor="w", pady=(30, 0))

        word_label = Label(meaning_frame,
                           text=word.word.capitalize(),
                           font=("Arial", 25),
                           fg="#BA4949",
                           bg="#397098")
        word_label.pack(anchor="w")

        for meaning in meanings:
            partOfSpeech_label = Label(meaning_frame,
                                       text=meaning["partOfSpeech"].capitalize(),
                                       font="Helvetica 18 italic",
                                       bg="#397098",
                                       fg="#FFFFFF",
                                       )
            partOfSpeech_label.pack(anchor="w")
            # Get only first 3 definitions
            definitions = meaning["definitions"]
            num_of_def = 2 if len(definitions) > 2 else len(definitions)

            for definition in definitions[:num_of_def]:

                def_label = Label(meaning_frame,
                                  text=f"{definitions.index(definition) + 1}. " + definition["definition"],
                                  bg="#397098",
                                  font=('Helvetica bold', 18),
                                  fg="#FFFFFF")

                def_label.pack(anchor="w")

                if "example" in definition:
                    example_label = Label(meaning_frame,
                                          text="Example: " + definition["example"],
                                          bg="#397098",
                                          fg="#FFFFFF",
                                          font=('Helvetica bold', 18))
                    example_label.pack(anchor="w", pady=(0, 10))

            synonyms_frame = Frame(meaning_frame, bg="#397098")
            synonyms_frame.pack(anchor="w", pady=(0, 30))

            if meaning["synonyms"]:
                synonyms_label = Label(synonyms_frame, text="Synonyms:", bg="#397098", fg="#FFFFFF",
                                       font=('Helvetica bold', 18))
                synonyms_label.pack(anchor="w", side=LEFT)

                for synonym in meaning["synonyms"][:3]:
                    synonym_label = Label(synonyms_frame, text=synonym, bg="#397098", fg="#FFFFFF",
                                          font=('Helvetica bold', 18))
                    synonym_label.pack(anchor="w", side=LEFT)

        add = Button(text="Add to List", command=lambda: self.add_to_list(word.word))
        add.pack()

    def add_to_list(self, word):
        with open("words.txt", mode="a+") as file:
            file.seek(0)
            words = [line.strip() for line in file.readlines()]

            if word in words:
                messagebox.showinfo("Failed", "Word Already Exits")
            else:
                file.write(f"\n{word}")
                messagebox.showinfo("Success", "Successfully Added to Your Word List")

    def remove_from_list(self, target_word):

        with open("words.txt", mode="r") as file:
            lines = file.readlines()

        with open("words.txt", mode="w") as file:
            for word in lines:

                if word.strip() != target_word.strip():
                    file.write(word)

        messagebox.showinfo("Delete Success", "Successfully Removed From Your Word List")
        self.show_wordlist()
