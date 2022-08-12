# DSC 510
# Week 10
# Program for forecasting weather information based on the user input.
# Programming Assignment Week 10
# Author Sharath Chandra Tummanapally
# 8/13/2021

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import Controller
temp_var = ''  # Defining global temperature variable.


class WeatherForecast(Frame):

    def __init__(self):
        super().__init__()

        # tkinter window settings.
        self.master.geometry('1000x700+210+50')  # Setting the size and position of tkinter window.
        self.master.iconbitmap('wf_icon.jpeg')  # Setting the image icon on tkinter window title bar.
        self.master.title('Welcome to Weather Forecast!')  # Setting the title on tkinter window title bar.
        self.master.option_add('*font', ('Avenir', 18, 'italic')) # Adding style to tkinter window.
        self.master.resizable(False, False)  # Disabling window resize.

        # Creating the main frame.
        self.mainBg = ImageTk.PhotoImage(Image.open('WeatherBg.png'))
        self.mainFrame = Frame(self.master)
        self.mainFrame.pack(fill=BOTH, expand=True)
        self.mainLbl = Label(self.mainFrame, image=self.mainBg).place(x=0, y=0)

        # Creating city button frame inside the main frame.
        self.cityBtnFrame = Frame(self.mainFrame, bg='#071242')
        # Creating zipcode button frame inside the main frame.
        self.zipBtnFrame = Frame(self.mainFrame, bg='#071242')
        # Creating the ask frame inside the main frame.
        self.askFrame = Frame(self.mainFrame, bg='#071242')
        self.askFrame.pack(pady=(150, 30))

        # Creating label and buttons for the user selection inside the ask frame.
        Label(self.askFrame, text='Search weather by : ', fg='white', bg='#071242').grid(row=0, column=0)
        Button(self.askFrame, text=' US City ', highlightbackground='#abfaff', command=self.city_btn).grid(row=0, column=1)
        Label(self.askFrame, text=' or ', fg='white', bg='#071242').grid(row=0, column=2)
        Button(self.askFrame, text=' Zip Code ', highlightbackground='#abfaff', command=self.zip_btn).grid(row=0, column=3)

        # Creating common label for displaying the error/weather message.
        self.msg_lbl = Label(self.mainFrame, bg='#071242', font=('Avenir', 20))
        # Creating label for displaying user note.
        self.user_note = Label(self.mainFrame, fg='white',bg='#071242', font=('Avenir', 14))
        # Creating labels for displaying the message for mandatory fields.
        self.city_req_lbl = Label(self.cityBtnFrame, text='*', fg='red', bg='#071242')
        self.state_req_lbl = Label(self.cityBtnFrame, text='*', fg='red', bg='#071242')
        self.zip_req_lbl = Label(self.zipBtnFrame, text='*', fg='red', bg='#071242')

        # Creating treeview for displaying weather data to user.
        self.tv = ttk.Treeview(self.mainFrame, show='tree')
        # Styling the treeview.
        self.tv_style = ttk.Style(self.master)
        self.tv_style.configure('Treeview', rowheight=25, fieldbackground='#071242', background='#071242', foreground='white', font=('Avenir', 18, 'italic'), borderwidth=0)
        # Defining the columns of treeview.
        self.tv['columns'] = ('Weather', 'Data')
        self.tv.column('#0', width=0)
        self.tv.column('Weather')
        self.tv.column('Data', stretch=TRUE, width=400, minwidth=400)

        # Adding validation for user inputs to tkinter window.
        self.check_int = self.master.register(self.validate_zip)
        self.check_city_txt = self.master.register(self.validate_city_txt)
        self.check_st_abv_txt = self.master.register(self.validate_st_abv_txt)

    def validate_zip(self, inp):
        """Function for validating the zipcode is integer and it's max length."""

        self.zip_req_lbl.grid_forget()
        if inp.isdigit() and len(inp) < 6:
            return True
        elif inp == '':
            return True
        else:
            return False

    def validate_city_txt(self, inp):
        """Function for validating the city name and it's max length."""

        self.city_req_lbl.grid_forget()

        if (inp.isalpha() or ' ' in inp) and not any(c.isdigit() for c in inp):
            return True
        elif inp == '':
            return True
        else:
            return False

    def validate_st_abv_txt(self, inp):
        """Function for validating the state abv and it's max length."""

        self.state_req_lbl.grid_forget()
        if inp.isalpha() and len(inp) < 3:
            return True
        elif inp == '':
            return True
        else:
            return False

    @staticmethod
    def load_radio_btn(frame):
        """Function for loading radio buttons on to the screen"""

        Label(frame, text='Select temperature in (Fahrenheit or Celsius or Kelvin) :', fg='white', bg='#071242').grid(row=3, column=0)
        temp_type = ['F', 'C', 'K']
        global temp_var
        temp_var = StringVar()

        # Creating and adding the radio buttons to the frame.
        i = 1
        for val in temp_type:
            Radiobutton(frame, text=val, value=val, variable=temp_var, fg='white', bg='#071242').grid(row=3, column=i)
            i += 1

        # Setting the default value to 'F'
        temp_var.set('F')

    def city_btn(self):
        """Function to load the form under city button."""

        self.zipBtnFrame.pack_forget()
        self.msg_lbl.pack_forget()
        self.user_note.pack_forget()
        self.zip_req_lbl.grid_forget()
        self.tv.pack_forget()
        self.cityBtnFrame.pack()
        city_txt = StringVar()
        state_abv_txt = StringVar()

        Label(self.cityBtnFrame, text='Please enter the city name :', fg='white', bg='#071242').grid(row=1, column=0, sticky=W)
        Entry(self.cityBtnFrame, width=20, highlightbackground='black', textvariable=city_txt, validate='key', validatecommand=(self.check_city_txt, '%P')).grid(row=1, column=1, columnspan=3)
        Label(self.cityBtnFrame, text='Please enter the state abbreviation :', fg='white', bg='#071242').grid(row=2, column=0, sticky=W)
        Entry(self.cityBtnFrame, width=20, highlightbackground='black', textvariable=state_abv_txt, validate='key', validatecommand=(self.check_st_abv_txt, '%P')).grid(row=2, column=1, columnspan=3)
        WeatherForecast.load_radio_btn(self.cityBtnFrame)
        Button(self.cityBtnFrame, text=' Search ', highlightbackground='#abfaff', command=lambda: self.search(self.cityBtnFrame, city_txt.get().strip(), state_abv_txt.get())).grid(row=4, column=1, columnspan=3, sticky=E, pady=10)

    def zip_btn(self):
        """Function to load the form under zip code button."""

        self.cityBtnFrame.pack_forget()
        self.msg_lbl.pack_forget()
        self.user_note.pack_forget()
        self.city_req_lbl.grid_forget()
        self.state_req_lbl.grid_forget()
        self.tv.pack_forget()
        self.zipBtnFrame.pack()
        zip_txt = StringVar()

        Label(self.zipBtnFrame, text='Please enter the zip code :', fg='white', bg='#071242').grid(row=1, column=0, sticky=W)
        Entry(self.zipBtnFrame, width=15, highlightbackground='black', textvariable=zip_txt, validate='key', validatecommand=(self.check_int, '%P')).grid(row=1, column=1, columnspan=3)
        WeatherForecast.load_radio_btn(self.zipBtnFrame)
        Button(self.zipBtnFrame, text='Search', highlightbackground='#abfaff',  command=lambda: self.search(self.zipBtnFrame, '', '', zip_txt.get())).grid(row=4, column=1, columnspan=3, sticky=E, pady=10)

    def search(self, frame, city_name='', state_abv='', zip_code=''):
        """Function for getting the weather data on the search button."""

        self.msg_lbl.pack(pady=5)
        self.user_note.pack_forget()
        frame_name = ''
        # Deleting the previous treeview data.
        for i in self.tv.get_children():
            self.tv.delete(i)

        # Setting the frame name based on the button selection.
        if frame == self.cityBtnFrame:
            frame_name = 'cityBtnFrame'
            # Display the required fields to the user, if no input is given.
            if not bool(city_name) and not bool(state_abv):
                self.city_req_lbl.grid(row=1, column=4, sticky=W)
                self.state_req_lbl.grid(row=2, column=4, sticky=W)
                self.tv.pack_forget()
                self.msg_lbl.configure(text='* Please fill the city name, state abbreviation fields.', fg='red')
                return False
            elif not bool(city_name):
                self.city_req_lbl.grid(row=1, column=4, sticky=W)
                self.tv.pack_forget()
                self.msg_lbl.configure(text='* Please fill the city name field.', fg='red')
                return False
            elif not bool(state_abv):
                self.state_req_lbl.grid(row=2, column=4, sticky=W)
                self.tv.pack_forget()
                self.msg_lbl.configure(text='* Please fill the state abbreviation field.', fg='red')
                return False

        elif frame == self.zipBtnFrame:
            frame_name = 'zipBtnFrame'
            # Display the required field to the user, if no input is given.
            if not bool(zip_code):
                self.zip_req_lbl.grid(row=1, column=4, sticky=W)
                self.tv.pack_forget()
                self.msg_lbl.configure(text='* Please fill the zip code field.', fg='red')
                return False

        if temp_var is not None:
            temp_type = temp_var.get()

        # Calling function to get weather data on search.
        weather_data, err_msg, user_note = Controller.weather_forecast(frame_name, city_name, state_abv, zip_code, temp_type)

        # Displaying requested weather data to the user.
        if bool(weather_data):
            # Weather data title.
            self.msg_lbl.config(text='Current Weather Conditions:', fg='#abfaff')

            # Adding weather data to treeview.
            for k, v in weather_data.items():
                self.tv.insert('', 'end', values=(k, ': ' + v))
            self.tv.pack(padx=(230, 0), pady=5)
        else:
            # Displays error message if no data is returned.
            self.msg_lbl.config(text=err_msg, fg='red')

        # Displays a note to user if invalid state code is given
        self.user_note.config(text=user_note)
        self.user_note.pack(side=BOTTOM)


def main():
    root = Tk()  # Instantiating the tinker window.
    app = WeatherForecast()  # Instantiating the class.
    root.mainloop()


if __name__ == '__main__':
    main()
