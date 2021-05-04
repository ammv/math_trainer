import tkinter as tk
from tkinter import *
from tkinter import messagebox
from random import randint, choice
from threading import Thread
from time import sleep
from math import ceil
from PIL import ImageTk, Image

class Math:
    def __init__(self, master=None):     
        self.master = master
        self.set_window()
        self.pre_config()
        self.settings_menu()
        self.pre_load_widgets()
        self.config()
        self.start_menu()
        
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
        
    def pre_config(self):
        self.taws = 0
        self.faws = 0
        self.answers = []
        
        self.settings_img = ImageTk.PhotoImage(Image.open("settings.png"))
        
        self.start_seconds = None
        self.min_num = None
        self.max_num = None
        
        self.arithmetics = ['+', '-']
        self.count_nums = None
        
        
    def config(self):  
        self.start_seconds = int(self.start_seconds_entry.get())
        if self.infinity_value.get() == 0: self.timer_label.config(text=str(self.start_seconds))
        else: self.timer_label.config(text='Бесконечное время')
        
        self.min_num = int(self.min_num_entry.get())
        self.max_num = int(self.max_num_entry.get())
       
        self.count_nums = int(self.count_nums_entry.get())
        
    def pre_load_widgets(self):
        self.start_btn = Button(self.master, text='Старт', bd=3, font='Tahoma 24', bg="#AC4535", fg='#dcb323', command=self.start_math)
        self.settings_btn = Button(self.master, text='', bd=0, image = self.settings_img, command=self.settings)
        
        self.answer_input = Entry(self.master, bd=2, font="Tahoma 24", width=12, bg = '#a6caf0', justify=CENTER)
        self.answer_input.bind('<Return>', self.check_answer)
        
        self.task_label = Label(self.master, height=1, text='', font="Tahoma 48", bg="lightgreen")
        self.timer_label = Label(self.master, text=str(self.start_seconds), font=("Tahoma", "20", "bold"), fg='#a7fc00')
        self.finish = Label(self.master, text='', font="Tahoma 24", fg='green')
        
        self.restart_btn = Button(self.master, bd=4, text='Рестарт', fg='#1E90FF', font='Tahoma 24', command=self.restart)
        
        self.stop_btn = Button(self.master, bd=2, text='Стоп', fg='#1EAECC', font='Tahoma 24', command=self.end_timer)
        
    def settings_menu(self):
        self.settings_frame_0 = LabelFrame(text='Арифметические знаки')
        list_symb = ['-', '+', '*', '/']
        self.symbs = [self.symb1, self.symb2, self.symb3, self.symb4]
        self.v0, self.v1, self.v2, self.v3 = [IntVar() for i in range(len(list_symb))]
        self.values = [self.v0, self.v1, self.v2, self.v3]
        self.check_btns = []
        for i, checkbtn in enumerate(list_symb):
            check_btn = Checkbutton(self.settings_frame_0, text=checkbtn, 
            onvalue=1, offvalue=0, command=self.symbs[i], variable=self.values[i])
            if checkbtn in self.arithmetics:
                check_btn.select()
            self.check_btns.append(check_btn)
            check_btn.pack()
            
        self.settings_frame_1 = LabelFrame(text='Мин. и макс. числа')
        self.min_num_entry = Entry(self.settings_frame_1)
        self.min_num_entry.insert(0, '1')
        self.max_num_entry = Entry(self.settings_frame_1)
        self.max_num_entry.insert(0, '10')
        self.min_num_entry.pack()
        self.max_num_entry.pack()
        
        self.settings_frame_2 = LabelFrame(text='Время на решение')
        self.start_seconds_entry = Entry(self.settings_frame_2)
        self.start_seconds_entry.insert(0, 60)
        self.start_seconds_entry.pack()
        
        self.infinity_value = IntVar()
        self.infinity_time = Checkbutton(self.settings_frame_2, text='Бесконечное время', onvalue=1, offvalue=0, variable=self.infinity_value)
        self.infinity_time.pack()
        
        self.settings_frame_3 = LabelFrame(text='Количество чисел в примере')
        self.count_nums_entry = Entry(self.settings_frame_3)
        self.count_nums_entry.insert(0, '3')
        self.count_nums_entry.pack()
        
    def symb1(self):
        self.update_arithmetics(self.check_btns[0], self.values[0])
        
    def symb2(self):
        self.update_arithmetics(self.check_btns[1], self.values[1])
        
    def symb3(self):
        self.update_arithmetics(self.check_btns[2], self.values[2])
        
    def symb4(self):
        self.update_arithmetics(self.check_btns[3], self.values[3])   
        
    def update_arithmetics(self, event, value):
        text, value = event['text'], value.get()
        if value == 1:
            self.arithmetics.append(text)
        else:
            self.arithmetics.remove(text)
        
    def start_menu(self):
        self.settings_btn['command'] = self.settings
        self.start_btn.pack(expand=1)
        self.settings_btn.place(relx=0.025, rely=0.025)
        if self.infinity_value.get() == 1:
            self.stop_btn.pack(side=RIGHT)
        
    def hide_and_start_menu(self, *event):
        self.config()
        self.hide_settings()
        self.start_menu()
        
    def show_restart_menu(self, *event):
        self.config()
        self.finish.place(x=100,y=200)
        self.restart_btn.place(x=300,y=350)
        self.hide_settings()
        
        self.settings_btn['command'] = self.hide_restart_menu
        
    def hide_restart_menu(self, *event):
        self.restart_btn.place_forget()
        self.finish.place_forget()
        
        self.settings(1)
        
    def settings(self, func = 0):
        commands = [self.hide_and_start_menu, self.show_restart_menu]
        self.start_btn.pack_forget()
        self.settings_btn['command'] = commands[func]
        
        self.settings_frame_0.pack()
        self.settings_frame_1.pack()
        self.settings_frame_2.pack()
        self.settings_frame_3.pack()
        
    def hide_settings(self, *event):
        self.settings_frame_0.pack_forget()
        self.settings_frame_1.pack_forget()
        self.settings_frame_2.pack_forget()
        self.settings_frame_3.pack_forget()
        
    def start_math(self):
        self.set_widgets()
        if self.infinity_value.get() == 0:
            self.start_thread_timer()
        
        self.start_btn.pack_forget()
        self.settings_btn.place_forget()
        
        self.task_label.config(text=self.get_task(self.count_nums))
        
    def set_widgets(self):
        self.answer_input.place(x=275,y=270)
        self.task_label.place(x=275,y=130)
        if self.infinity_value.get() == 0: self.timer_label.place(x=725,y=5)
        else: self.timer_label.place(x=0.75,y=0.075)
            
    def start_thread_timer(self):
        self.target = Thread(target=self.start_timer)
        self.target.start()
        
    def restart(self, *event):
        self.faws = 0
        self.taws = 0
        self.answers = []
        
        self.restart_btn.place_forget()
        self.finish.place_forget()
        self.settings_btn.place_forget()
        
        self.answer_input['state'] = NORMAL
        
        self.task_label.config(text=self.get_task(self.count_nums))
        self.answer_input.delete(0, END)
        
        self.answer_input.place(x=275,y=270)
        self.task_label.place(x=275,y=130)
        self.timer_label.config(text=str(self.start_seconds))
        self.timer_label.place(x=725,y=5)
        
        self.start_thread_timer()
        
    def start_timer(self):
        for i in range(self.start_seconds + 1):
            self.update_timer()
            sleep(1)
            
    def end_timer(self):
        self.answer_input['state'] = DISABLED
        self.answer_input.place_forget()
        self.task_label.place_forget()
        self.timer_label.place_forget()
            
        self.finish.config(text=self.get_statics())
        
        self.finish.place(x=100,y=200)
        self.restart_btn.place(x=300,y=350)
        
        self.settings_btn['command'] = self.hide_restart_menu
        self.settings_btn.place(relx=0.025, rely=0.025)
        
        if self.infinity_value == 1:
            self.stop_btn.pack_forget()
        
        print(''.join(i + '\n' for i in self.answers))
        
    def update_timer(self):
        seconds = int(self.timer_label['text'])
        if seconds == 0:
            self.end_timer()
        else:
            colors = ['green', 'yellow', '#f80000']
            color = int((seconds-1)/ceil(self.start_seconds / len(colors)))+1
            self.timer_label.config(text=str(seconds-1), fg=colors[-color])
            
            
    def get_statics(self):
        if self.taws > 0:
            if self.infinity_value.get() == 0:
                text = 'Вы решили {} примеров за {} секунд\n'.format(self.taws, self.start_seconds)
                text += 'Ср. время решения примера: {} секунд\n'.format(round(self.start_seconds/self.taws, 2))
                text += 'Всего попыток: {}\n'.format(self.taws + self.faws)
            else:
                text = 'Вы решили {} примеров'.format(self.taws)
                text += 'Всего попыток: {}\n'.format(self.taws + self.faws)
        else:
            if self.infinity_value.get() == 0: 
                text = 'Вы не решили ни один пример за {} секунд'.format(self.start_seconds)
            else:
                text = 'Вы не решили ни один пример'
        
        return text
        
    def check_answer(self, *event):
        user_answer = int(self.answer_input.get())
        if user_answer == self.answer:
            print('Правильный ответ!', self.task, self.answer)
            print(self.max_num_entry['text'])
            self.task_label.config(text=self.get_task(self.count_nums))
            self.answer_input.delete(0, END)
            self.taws += 1
        else:
            print('Неправильный ответ!')
            self.faws += 1
        
        #print('Неправильный ввод', e)
        
    def get_task(self, n=3):
        task = "";
        
        for i in range(n):
            task += str(randint(self.min_num, self.max_num))
            task += choice(self.arithmetics)
       
        self.task = self.check_task(task)
        self.answer = eval(self.task)
        self.answers.append('Пример: {} Ответ: {}'.format(self.task, self.answer))
        print('Пример:', self.task)
        return self.task
        
    def check_task(self, task):
        task = task.replace('--', '-(-').replace('+-', '+(-')
        find = False
        find_i = 0
        for i in range(len(task)-1):
            if find == False:
                if task[i:i+2] == '(-':
                    find = True
                    i += 2
                    find_i = i + 2
            else:
                if task[i] in self.arithmetics or task[i] == task[-1]:
                    task = task[:find_i-1] + task[find_i:i] + ')' + task[i+(i+find_i):]
                    find = False
                    
        return task[:-1] if task[-1] != ')' else task

    def closing(self):
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.master.destroy()
        except:
            pass

    def mainloop(self):
        self.master.protocol("WM_DELETE_WINDOW", self.closing)
        self.master.mainloop()
        
root = Tk()
app = Math(root)
        
if __name__ == '__main__':
   app.mainloop()


