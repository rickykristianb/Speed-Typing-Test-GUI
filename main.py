from tkinter import *
from tkinter import ttk, messagebox
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class Timer:

    def __init__(self):
        self.time = None
        self.time_remaining = None
        self.count_second = 0
        self.count_minute = 0

    def countdown_timer(self, count_num):
        """Timer Behaviour"""
        self.count_minute = count_num // 60
        self.count_second = count_num % 60

        minute_checking = self.count_minute in [1, 2, 3, 4, 5, 6, 7, 8, 9]

        if self.count_minute !=0 and self.count_second == 0:  # if timer starts other than 0
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"0{self.count_minute}:00", fg="black")
        elif self.count_minute == 10 and self.count_second == 0:  # if timer starts at 10 minutes
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"{self.count_minute}:00", fg="black")
        elif self.count_minute == 0 and self.count_second > 10:  # If timer start 1-9 minutes, and second counter is greater than 10
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"0{self.count_minute}:{self.count_second}", fg="black")
        elif minute_checking and self.count_second > 10:
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"0{self.count_minute}:{self.count_second}", fg="black")
        elif minute_checking and 10 > self.count_second >= 0:
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"0{self.count_minute}:0{self.count_second}", fg="black")
        elif minute_checking and self.count_second == 10:
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"0{self.count_minute}:{self.count_second}", fg="black")
        elif self.count_second == 10 and self.count_minute == 0:
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"0{self.count_minute}:{self.count_second}", fg="red")
        elif 10 > self.count_second >= 0 and self.count_minute == 0:
            windows.after(1000, self.countdown_timer, count_num - 1)
            self.time_remaining.config(text=f"0{self.count_minute}:0{self.count_second}", fg="red")

        if self.count_second == 0 and self.count_minute == 0:
            self.time = 0

class GetData:

    article = []
    URL = "https://randomwordgenerator.com/sentence.php"

    def __init__(self):
        pass

    @classmethod
    def scrap_data(cls):
        option = Options()
        option.add_experimental_option("detach", True)

        chrome_driver_path = "C:\\Developement\\chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=option)
        driver.get(cls.URL)
        insert_number_sentences = driver.find_element(By.ID, "qty")
        insert_number_sentences.send_keys(Keys.CONTROL)
        insert_number_sentences.send_keys("A")
        insert_number_sentences.send_keys(Keys.DELETE)
        insert_number_sentences.send_keys("50")
        generate_sentence_button = driver.find_element(By.ID, "btn_submit_generator")
        generate_sentence_button.click()

        sentences_data = driver.find_elements(By.CLASS_NAME, "support-sentence")
        for sentence in sentences_data:
            cls.article.append(sentence.text)
        cls.article = " ".join(cls.article)
        driver.close()


class TypingSpeed(Timer, GetData):

    words_input = []
    data_start = 0
    data_end = 8
    comparison_data = []

    def __init__(self):
        super().__init__()
        self.default_option = None
        self.dropdown_time = None
        self.start_button = None
        self.label_text_test = None
        self.counter_accuracy = None
        self.label_accuracy = None
        self.counter_NWPM = None
        self.label_NWPM = None
        self.counter_net_words = None
        self.label_net_words = None
        self.counter_GWPM = None
        self.label_GWPM = None
        self.counter_gross_words = None
        self.gross_words = None
        self.label_gross_words = None
        self.input_field = None
        self.input_value = None
        self.data = None

    def show_test_words(self):
        """Return data with and max list is 8. Data is fetch from scrapping"""
        data = GetData()
        data.scrap_data()
        self.data = GetData().article.split()
        self.label_text_test.config(text=" ".join(self.data[:8]))
        self.comparison_data.extend(" ".join(self.data[:8]))

    def test_onchange(self):  # TODO: Check how if user click backspace until previous sentence. revert back the sentence
        """Receive each character that user type-in into the input_field"""
        print(f"Len Words Input {len(self.words_input)}, Comparison data: {len(self.comparison_data)}")
        if len(self.words_input) < len(self.comparison_data): # Check if user insert char still less than the text on the label\
            try:
                self.words_input.append(self.input_value.get()[-1])
            except IndexError:
                pass
            # print(self.words_input)
            print("".join(self.words_input).split())
        else:  # change the label to the next 8 words text
            self.words_input.append(" ")  # if the list already at index 8, add " " to the last index in order to avoid word joining between index 8 and 8, ex: "thishouse", should be "this house"
            self.data_start, self.data_end = self.data_end + 1, self.data_end + 8  # start from 0 to 8 in the list, next iteration data_start will be data_end + 1 and data_end will be data_end + 8
            print(f"Data Start: {self.data_start}, Data End: {self.data_end}")
            self.label_text_test.config(text=" ".join(self.data[self.data_start:self.data_end]))
            self.comparison_data.append(" ")  # Add " " to the last index to avoid comparison data joining, ex: "thishouse", should be "this house"
            self.comparison_data.extend(" ".join(self.data[self.data_start:self.data_end]))

        self.input_field.bind("<BackSpace>", lambda e: [self.pop_last_value(), self.pop_last_value()])  # If user type "BackSpace" to delete character, then remove the last char from the list
        # We use two times of pop_last_value() because we need to remove two times the last char to avoid the last word after deleting is inserting again, ex. ['House'] - > remove e -> result: ['Houss']: s before e inserted again

    def pop_last_value(self):
        try:
            return self.words_input.pop()
        except IndexError:
            pass

    def start_typing(self):
        """Create a user input field and send the data/key each time user typing by character"""
        self.input_value = StringVar()
        self.input_value.trace("w", lambda l, idx, mode: self.test_onchange())
        self.input_field = Entry(textvariable=self.input_value, width=51, font=("Arial", 15))  # Send key pressed to test_onchange()
        self.input_field.place(x=60, y=400)

    def timer_on(self, user_time):
        """Start the timer"""
        self.countdown_timer(user_time)
        Thread(target=self.is_timer_done).start()  # Run the code simultaneously to check if the timer have finished

    def is_timer_done(self):
        """Check the self.time status. If 0, then the calculation is started"""
        check = False
        while not check:
            if self.time == 0:
                self.input_field.config(state="disabled")
                self.calculate_wpm()
                check = True

    def calculate_wpm(self):
        """Calculate the WPM"""
        user_input = "".join(self.words_input)
        computer_data = "".join(self.comparison_data)
        print("".join(self.words_input))
        print("".join(self.comparison_data))
        wrong_words = 0
        correct_words = 0
        for x, y in zip(user_input.split(), computer_data.split()):
            if x != y:
                wrong_words += 1
                print("salah", x, y)
            else:
                correct_words += 1
                print("benar", x, y)
        print(wrong_words)
        gross_words = wrong_words + correct_words
        gwpm = gross_words/int(self.default_option.get())
        nwpm = correct_words/int(self.default_option.get())
        accuracy = (nwpm * 100) / gwpm
        self.counter_gross_words.config(text=gross_words)
        self.counter_net_words.config(text=correct_words)
        self.counter_GWPM.config(text=gwpm)
        self.counter_NWPM.config(text=nwpm)
        try:
            self.counter_accuracy.config(text="{:.2f}".format(accuracy))
        except ZeroDivisionError:
            messagebox.showinfo(message="You have not inserted any words.")

    def show_interface(self):
        """Showing Interface"""
        self.label_gross_words = Label(text="Gross Words: ", font=("Arial", 10), bd=4, bg="white", pady=10)
        self.label_gross_words.grid(column=0, row=0, padx=(50, 0), pady=20)
        self.counter_gross_words = Label(text="0", font=("Arial", 10), bd=4, bg="white", pady=10, padx=20)
        self.counter_gross_words.grid(column=1, row=0)

        self.label_GWPM = Label(text="Gross Words per min (GWPM): ", font=("Arial", 10), bd=4, bg="white", pady=10)
        self.label_GWPM.grid(column=2, row=0, padx=(50, 0), pady=20)
        self.counter_GWPM = Label(text="0", font=("Arial", 10), bd=4, bg="white", pady=10, padx=20)
        self.counter_GWPM.grid(column=3, row=0)

        self.label_net_words = Label(text="Net Words: ", font=("Arial", 10), bd=4, bg="white", pady=10, )
        self.label_net_words.grid(column=4, row=0, padx=(50, 0), pady=20)
        self.counter_net_words = Label(text="0", font=("Arial", 10), bd=4, bg="white", pady=10, padx=20)
        self.counter_net_words.grid(column=5, row=0)

        self.label_NWPM = Label(text="Net words per min (NWPM): ", font=("Arial", 10), bd=4, bg="white", pady=10, )
        self.label_NWPM.place(relx=0.15, rely=0.2)
        self.counter_NWPM = Label(text="0", font=("Arial", 10), bd=4, bg="white", pady=10, padx=20)
        self.counter_NWPM.place(relx=0.4, rely=0.2)

        self.label_accuracy = Label(text="Accuracy: ", font=("Arial", 10), bd=4, bg="white", pady=10, )
        self.label_accuracy.place(relx=0.6, rely=0.2)
        self.counter_accuracy = Label(text="0", font=("Arial", 10), bd=4, bg="white", pady=10, padx=20)
        self.counter_accuracy.place(relx=0.7, rely=0.2)

        # Separator Object
        separator = ttk.Separator(windows, orient="horizontal")
        separator.place(relx=0, rely=0.35, relwidth=1.4)

        # Text Test Label
        self.label_text_test = Label(text="", font=("Cursive", 14, 'bold'), width=47, height=5, bg="white")
        self.label_text_test.place(x=60, y=210)
        self.show_test_words()

        # Checking get data from list and show it in label
        self.time_remaining = Label(text=f"00:00", font=("Arial", 15))
        self.time_remaining.place(relx=0.445, rely=0.9)

        # Dropdown Time
        dropdown_label = Label(text="Time", font=("Cursive", 12))
        dropdown_label.place(x=200, y=354)
        options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.default_option = StringVar()
        self.default_option.set(options[0])
        self.dropdown_time = OptionMenu(windows, self.default_option, *options)
        self.dropdown_time.place(x=250, y=350)
        label_minutes_word = Label(text="Minute", font=("Cursive", 12))
        label_minutes_word.place(x=308, y=354)

        # Start Button
        self.start_button = Button(
            text="Start", width=10,
            command=lambda: [self.start_typing(), self.timer_on(int(self.default_option.get()) * 60)]  # Run 2 function at a time
        )

        self.start_button.place(x=400, y=350)


if __name__ == "__main__":
    windows = Tk()
    windows.title("Typing Speed Test")
    windows.geometry("700x500")
    windows.maxsize(width=700, height=500)
    windows.minsize(width=700, height=500)
    start = TypingSpeed()
    start.show_interface()

    windows.mainloop()
