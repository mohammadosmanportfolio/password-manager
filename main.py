from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

def find_password():
    if website_input.get() == "":
        messagebox.showerror(title="No website entered", message="You must enter a website!")
        return
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="No Data File", message="No Data File Found")
    else:
        website = website_input.get()
        if website in data or website.lower() in data:
            password = data[website]['password']
            email = data[website]['email']
            messagebox.showinfo(title=f"Information for {website}", message=f"Here is the data for {website}:\n"
                                f"Password: {password}\n"
                                f"Email: {email}")
        else:
            messagebox.showinfo(title=f"No Data Found", message=f"No details for the website {website} exists")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_random_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    letter_list = [random.choice(letters) for x in range(nr_letters)]
    password_list.extend(letter_list)

    symbol_list = [random.choice(symbols) for x in range(nr_symbols)]
    password_list.extend(symbol_list)

    number_list = [random.choice(numbers) for x in range(nr_numbers)]
    password_list.extend(number_list)

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, string=password)
    pyperclip.copy(text=password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def put_password_into_file():
    website = website_input.get()
    password = password_input.get()
    email = email_input.get()
    new_data = {website:
                {"email": email,
                 "password": password,
                }}

    #checking if the user left out any details
    if len(password) == 0 or len(website) == 0 or len(email) == 0:
        messagebox.showerror(title='Empty Fields', message="Please do not leave any fields empty!")
        return
    
    #asking the user if they're okay with all the details they entered
    is_ok = messagebox.askokcancel(title=website, message=f"You entered the following details:\n"
                           f"Website: {website}\n"
                           f"Email: {email}\n"
                           f"Password: {password}\n"
                           "Is this okay?")
    
    #if they are okay with all details, save it into data.json file
    if is_ok:
        data = None
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            reset_interface()

def reset_interface():
    website_input.delete(0, END)
    password_input.delete(0, END)
    website_input.focus()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(bg='white', padx=20, pady=20)
window.title('Password Manager')

canvas = Canvas(window, height=200, width=200)
canvas.config(bg='white', highlightthickness=0)
canvas.grid(column=1, row=0)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, anchor='center', image=logo)

website_label = Label(text="Website:", fg='black', font=('Times New Roman', 10), bg='white')
website_label.grid(column=0, row=1, pady=5)

website_input = Entry(width=25)
website_input.grid(column=1, row=1, pady=5, padx=(5, 0))
website_input.focus()

email_label = Label(text="Email/Username:", fg='black', font=('Times New Roman', 10), bg='white')
email_label.grid(column=0, row=2, pady=5)

email_input = Entry(width=35)
email_input.grid(column=1, row=2, columnspan=2, pady=5, padx=(0, 48))
email_input.insert(0, 'mohammad@gmail.com')

password_label = Label(text='Password:', fg='black', font=('Times New Roman', 10), bg='white')
password_label.grid(column=0, row=3, pady=5)

password_input = Entry(width=25)
password_input.grid(column=1, row=3, pady=5, padx=(5, 0))

generate_password = Button(text="Generate Password", fg='black', font=('Times New Roman', 10), bg='white', command=generate_random_password)
generate_password.grid(column=2, row=3, pady=5)

add = Button(text="Add", bg='white', fg='black', font=('Times New Roman', 10), 
             width=36, command=put_password_into_file)
add.grid(column=1, row=4, pady=5, columnspan=2)

search_button = Button(text='Search', font=('Times New Roman', 10), width=15, 
                       command=find_password, fg='black', bg='white')
search_button.grid(column=2, row=1, pady=5)

window.mainloop()