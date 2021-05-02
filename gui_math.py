import tkinter as tk
from tkinter import *
from tkinter import messagebox
from random import randint
from threading import Thread
from time import sleep
from math import ceil
from PIL import ImageTk, Image

class Math:
    def __init__(self, config, master=None):     
        self.master = master
        self.set_window()
        self.config(config)
        self.start_menu()
        #self.set_widgets()
        
    def config(self, kwargs):
        self.taws = 0
        self.faws = 0
        
        self.settings_img = ImageTk.PhotoImage(Image.open("settings.png"))
        
        self.start_seconds = kwargs['start_seconds']
        self.min_num = kwargs['min_num']
        self.max_num = kwargs['max_num']
        
        self.arithmetics = kwargs['arithmetics']
        self.count_nums = kwargs['count_nums']
        
    def start_menu(self):
        self.start_btn = Button(self.master, text='Старт', bd=3, font='Tahoma 24', bg="#AC4535", fg='#dcb323', command=self.start_math)
        self.start_btn.pack(expand=1)
        
        self.settings_btn = Button(self.master, text='', bd=0, image = self.settings_img, command=self.settings)
        self.settings_btn.place(relx=0.025, rely=0.025)
        
    def settings_menu(self):
        self.settings_frame_0 = LabelFrame(text='Арифметические знаки')
        list_symb = ['-', '+', '*', '/']
        self.check_btns = []
        for checkbtn in list_symb:
            check_btn = Checkbutton(self.settings_frame_0, text=checkbtn, onvalue=1, offvalue=0)
            self.check_btns.append(check_btn)
            
        self.settings_frame_1 = LabelFrame(text='Числа')
        validate = self.master.register(self.validate_entry)
        self.min_num = Entry(self.settings_frame_1, validatecommand=(validate, "%P"))
        self.max_num = Entry(self.settings_frame_1, validatecommand=(validate, "%P"))
        
    def validate_entry(self, new_value):
        if1 = new_values.isdigit()
        if2 = float(self.max_num['text']) >= float(self.min_num['text'])
        if3 = int(new_value)==float(new_value)
        return if1 and if2 and if3
        
    def settings(self):
        self.start_btn.pack_forget()
        self.settings_btn['command'] = self.start_menu
        
    def hide_settings(self, *args):
        self.settings_frame_0.grid_forget()
        self.settings_frame_1.grid_forget()
        
    def start_math(self):
        self.set_widgets()
        self.start_thread_timer()

    def set_window(self):
        self.master.title('Математика')
        self.master.resizable(True, True)

        w = 800
        h = 600
        ws = self.master.winfo_screenwidth()
        wh = self.master.winfo_screenheight()

        self.x = ws // 2 - w // 2
        self.y = wh // 2 - h // 2

        self.master.geometry(f'{w}x{h}+{self.x}+{self.y}')
        
    def set_widgets(self):
        self.answer_input = Entry(self.master, bd=2, font="Tahoma 24", width=12, bg = '#a6caf0', justify=CENTER)
        self.answer_input.bind('<Return>', self.check_answer)
        self.answer_input.place(x=275,y=270)
        
        self.task_label = Label(self.master, width=6, height=1, text=self.get_task(3), font="Tahoma 48", bg="lightgreen")
        self.task_label.place(x=275,y=130)
        
        self.timer_label = Label(self.master, text=str(self.start_seconds), font=("Tahoma", "20", "bold"), fg='#a7fc00')
        self.timer_label.place(x=725,y=5)
        
        self.finish = Label(self.master, text='', font="Tahoma 24", fg='green')
        
        self.restart_btn = Button(self.master, bd=4, text='Рестарт', fg='#1E90FF', font='Tahoma 24', command=self.restart)
        
    def start_thread_timer(self):
        self.target = Thread(target=self.start_timer)
        self.target.start()
        
    def restart(self, *args):
        self.faws = 0
        self.taws = 0
        
        self.restart_btn.place_forget()
        self.finish.place_forget()
        
        self.answer_input.place(x=275,y=270)
        self.task_label.place(x=275,y=130)
        self.timer_label.config(text=str(self.start_seconds))
        self.timer_label.place(x=725,y=5)
        
        start_thread_timer()
        
    def start_timer(self):
        for i in range(self.start_seconds + 1):
            self.update_timer()
            sleep(1)
            
    def end_timer(self):
        self.answer_input.place_forget()
        self.task_label.place_forget()
        self.timer_label.place_forget()
            
        self.finish.config(text=self.get_statics())
        
        self.finish.place(x=100,y=200)
        self.restart_btn.place(x=300,y=350)
        
    def update_timer(self):
        seconds = int(self.timer_label['text'])
        if seconds == 0:
            self.end_timer()
        else:
            colors = ['#a7fc00', '#ffd800', '#f80000']
            color = int((seconds-1)/ceil(self.start_seconds / len(colors)))+1
            self.timer_label.config(text=str(seconds-1), fg=colors[-color])
            
            
    def get_statics(self):
        if self.taws > 0:
            text = 'Вы решили {} примеров за {} секунд\n'.format(self.taws, self.start_seconds)
            text += 'Ср. время решения примера: {} секунд\n'.format(round(self.start_seconds/self.taws, 2))
            text += 'Всего попыток: {}\n'.format(self.taws + self.faws)
        else:
            text = 'Вы не решили ни один пример за {} секунд'.format(self.start_seconds)
        
        return text
        
    def check_answer(self, *args):
        try:
            user_answer = int(self.answer_input.get())
            if user_answer == self.answer:
                print('Правильный ответ!')
                self.task_label.config(text=self.get_task(3))
                self.answer_input.delete(0, END)
                self.taws += 1
            else:
                print('Неправильный ответ!')
                self.faws += 1
        except:
            print('Неправильный ввод')
        
    def get_task(self, n=3):
        self.task = "";
        
        for i in range(n):
            self.task += str(randint(self.min_num, self.max_num))
            self.task += choice(self.arithmetics)
       
        self.task = self.task[:-1]
        self.answer = eval(self.task)
        return self.task

    def closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def mainloop(self):
        self.master.protocol("WM_DELETE_WINDOW", self.closing)
        self.master.mainloop()
        
base_config = {
    'start_seconds': 60,
    'min_num': -10,
    'max_num': 30,
    'count_nums': 3,
    'arithmetics': ['-', '+']
    }
        
root = Tk()
app = Math(base_config, root)
        
if __name__ == '__main__':
   app.mainloop()


