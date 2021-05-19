import tkinter as tk
from tkinter import (
    Button, Entry, NORMAL, DISABLED, Label,
    LabelFrame, Checkbutton, RIGHT,
    CENTER, IntVar, Tk, END, LEFT,
    TOP, BOTTOM, Toplevel, BOTH,
    Scrollbar, VERTICAL,Y, Text,
    CENTER, 
)
from tkinter import messagebox
from random import randint, choice
from threading import Thread
from time import sleep
from math import ceil
from PIL import ImageTk, Image

class MathCMD(Toplevel):
    def __init__(self,  parent):
        super().__init__(parent)
        self.start()
        self.withdraw()
            
    def start(self):
        self.commands = {
                'A': self.get_answer,
                'S': self.skip_task,
                'STOP': self.stop_decide,
                'R': self.reload_app,
                'HELP': self.help,
                }
        self.set_window()
        self.set_widgets()
        
        self.insert_math_log('start', 'MathCMD v1.0')
        self.insert_math_log('help', self.help())
        
    def get_base(self, base):
        self.base = base
        
    def help(self):
        help = '=====КОМАНДЫ=====\nA-ответ на задачу\n'
        help += 'S-Пропуск примера\nR-перезагрузка программы\n'
        help += 'STOP-Закончить решать\nHELP-помощь'
        return help
        
    def set_window(self):
        self.title('Терминал Math')
        self.resizable(False, False)

        w = 400
        h = 150

        self.geometry(f'{w}x{h}')#+{self.x}+{self.y}')
        
        self.protocol("WM_DELETE_WINDOW", self.closing)
        
    def closing(self):
        self.withdraw()
        self.base.cmd_work = False
        
    def set_widgets(self):
        self.logs = Text(self, bd=0,bg='black', width=60, height=8, fg='#158078')
        self.logs.config(state=DISABLED)
        
        self.scroll_y = Scrollbar(self, orient=VERTICAL, command=self.logs.yview)
        self.logs['yscrollcommand'] = self.scroll_y.set
        self.scroll_y.pack(side=RIGHT, fill = Y)
        self.logs.pack(fill=BOTH)
        
        self.logs.tag_config('start', foreground='yellow')
        self.logs.tag_config('log', foreground='#158078')
        self.logs.tag_config('error', foreground='#FF0033')
        self.logs.tag_config('new_task', foreground='#0047AB')
        self.logs.tag_config('true_answer', foreground='#20603D')
        self.logs.tag_config('false_answer', foreground='#FFA000')
        self.logs.tag_config('answers', foreground='#228B22')
       
        self.scroll_y.config(command=self.logs.yview)
        
        self.entry = Entry(self, bd=1,bg='#7FFFD4',width=70)
        self.entry.bind('<Return>', self.command_send)
        self.entry.pack(side=BOTTOM)
        
    def command_send(self, *event):
        command = self.entry.get()
        if command in self.commands.keys():
            if command != 'HELP':
                text = '\n[LOGS]' + self.commands[command]()
            else:
                text = '\n' + self.commands[command]()
            if command != 'R':
                self.logs.config(state=NORMAL)
                self.logs.insert(END, text)
                self.logs.config(state=DISABLED)
                self.entry.delete('0', END)
        else:
            self.logs.config(state=NORMAL)
            self.logs.insert(END, '\n[LOGS]Неизвестная команда')
            self.logs.config(state=DISABLED)
        
    def reload_app(self):
        self.base.destroy()
        app = run_app()
        return 'Reload'
        
    def get_answer(self):
        try:
            answer = self.base.answer
            return 'Ответ на пример: {}'.format(answer)
        except AttributeError as e:
            return 'Error'
    
    def skip_task(self):
        self.base.task_label.config(text=self.base.get_task(self.base.count_nums))
        self.base.master.update()
        
        width = self.base.task_label.winfo_width()
        self.base.task_label.place(x=275+(210-width)/2, y=130)
                
        self.base.answer_input.delete(0, END)
        
        return 'Пример пропущен'
        
    def stop_decide(self):
        self.base.end_timer()
        self.base.timer_paused = False
        return 'Вы завершили решение'
        
    def insert_math_log(self, tag, logs):
        self.logs.config(state=NORMAL)
        if type(logs) == list:
            for log in logs:
                self.logs.insert(END, '\n'+log, tag)
        else:
            if tag == 'start':
                self.logs.insert(END, logs, tag)
            else:
                self.logs.insert(END, '\n'+logs, tag)
        self.logs.config(state=DISABLED)
        
    def mainloop(self):
        self.mainloop()
        

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
        
        self.cmd_work = False
        self.mathcmd = MathCMD(self.master)
        self.mathcmd.get_base(self)
        
        self.settings_img = ImageTk.PhotoImage(Image.open("settings.png"))
        self.cmd_img = ImageTk.PhotoImage(Image.open("cmd.png"))
        self.pause_img = ImageTk.PhotoImage(Image.open("pause.png"))
        
        self.start_seconds = None
        self.min_num = None
        self.max_num = None
        
        self.arithmetics = ['+', '-']
        self.count_nums = None
        
        self.timer_paused = False
        
        
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
        self.pause_btn = Button(self.master, text='', bd=0, image = self.pause_img, command=self.pause_decide)
        
        self.cmd_btn = Button(self.master, text='', bd=0, image = self.cmd_img, command = self.create_cmd)
        
        self.answer_input = Entry(self.master, bd=2, font="Tahoma 24", width=12, bg = '#a6caf0', justify=CENTER)
        self.answer_input.bind('<Return>', self.check_answer)
        
        self.task_label = Label(self.master, height=1, text='', font="Tahoma 60", bg="lightgreen", justify=CENTER)
        self.timer_label = Label(self.master, text=str(self.start_seconds), font=("Tahoma", "20", "bold"), fg='#a7fc00', justify=CENTER)
        self.finish = Label(self.master, text='', font="Tahoma 24", fg='green')
        
        self.restart_btn = Button(self.master, bd=4, text='Рестарт', fg='#1E90FF', font='Tahoma 24', command=self.restart)
        
        self.stop_btn = Button(self.master, bd=2, text='Стоп', fg='#1EAECC', font='Tahoma 24', command=self.end_timer)
        
    def validate(self, new_value):
        if self.not_validate == False:
            if new_value != '':
                try:
                    float(new_value)
                    return True
                except:
                    return False
            else:
                return True
        else:
            return True
        
    def settings_menu(self):
        self.not_validate = True
        
        self.validate_entry = self.master.register(self.validate)
        
        self.settings_frame_0 = LabelFrame(text='Арифметические\nзнаки', font='Tahoma 16 bold', fg='#F34723')
        list_symb = ['-', '+', '*', '/']
        self.symbs = [self.symb1, self.symb2, self.symb3, self.symb4]
        self.v0, self.v1, self.v2, self.v3 = [IntVar() for i in range(len(list_symb))]
        self.values = [self.v0, self.v1, self.v2, self.v3]
        self.check_btns = []
        for i, checkbtn in enumerate(list_symb):
            check_btn = Checkbutton(self.settings_frame_0, text=checkbtn, 
            onvalue=1, offvalue=0, command=self.symbs[i], variable=self.values[i], font='Tahoma 14')
            if checkbtn in self.arithmetics:
                check_btn.select()
            self.check_btns.append(check_btn)
            check_btn.pack(side=LEFT, padx=5, pady=5)
            
        self.settings_frame_1 = LabelFrame(text='Мин. и макс.\nчисла', font='Tahoma 16 bold', fg='#F4A900')
        self.min_num_entry = Entry(self.settings_frame_1, font='Tahoma 10', justify=CENTER, 
            validate="key", validatecommand=(self.validate_entry, "%P"))
        self.min_num_entry.insert(0, '1')
        self.max_num_entry = Entry(self.settings_frame_1, font='Tahoma 10', justify=CENTER,
            validate="key", validatecommand=(self.validate_entry, "%P"))
        self.max_num_entry.insert(0, '10')
        self.min_num_entry.pack(pady=2)
        self.max_num_entry.pack(pady=1)
        
        self.settings_frame_2 = LabelFrame(text='Время на\nрешение', font='Tahoma 16 bold', fg='#9ACD32')
        self.start_seconds_entry = Entry(self.settings_frame_2, font='Tahoma 10', justify=CENTER,
            validate="key", validatecommand=(self.validate_entry, "%P"))
        self.start_seconds_entry.insert(0, '60')
        self.start_seconds_entry.pack(padx=5)
        
        self.infinity_value = IntVar()
        self.infinity_time = Checkbutton(self.settings_frame_2, text='Бесконечное время', onvalue=1, offvalue=0, 
        variable=self.infinity_value, font='Tahoma 10')
        self.infinity_time.pack(padx=5)
        
        self.settings_frame_3 = LabelFrame(text='Количество чисел\nв примере', font='Tahoma 16 bold', fg='#1E90FF')
        self.count_nums_entry = Entry(self.settings_frame_3, font='Tahoma 10', justify=CENTER,
            validate="key", validatecommand=(self.validate_entry, "%P"))
        self.count_nums_entry.insert(0, '3')
        self.count_nums_entry.pack()
        
        self.settings_frame_4 = LabelFrame(text='Количествово чисел\nпосле запятой', font='Tahoma 16 bold', fg='#5D76CB')
        self.nums_after_zap = Entry(self.settings_frame_4, font='Tahoma 10', justify=CENTER,
            validate="key", validatecommand=(self.validate_entry, "%P"))
        self.nums_after_zap.insert(0, '2')
        self.nums_after_zap.pack()
        
        self.entrys = [self.min_num_entry, self.max_num_entry, self.nums_after_zap, 
            self.start_seconds_entry,self.count_nums_entry]
        
        self.not_validate = False
        
    def check_settings(self, *event):
        self.save_settings_btn.config(text='Сохранено', fg='green')
        
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
            
    def pause_decide(self, *event):
        if self.timer_paused == False:
            self.timer_paused = True
            self.answer_input.config(state=DISABLED)
            self.answer_input.place_forget()
        else:
            self.timer_paused = False
            self.answer_input.config(state=NORMAL)
            self.answer_input.place(x=275,y=270)
            
        if self.cmd_work:
            self.mathcmd.insert_math_log('log', 
                ['[MATH]Play', '[MATH]Pause'][int(self.timer_paused)])
        
    def start_menu(self):
        self.settings_btn['command'] = self.settings
        self.start_btn.pack(expand=1)
        self.settings_btn.place(relx=0.025, rely=0.025)
        self.cmd_btn.place(relx=.925, rely=.025)
        if self.infinity_value.get() == 1:
            self.stop_btn.pack(side=RIGHT)
        
    def hide_and_start_menu(self, *event):
        self.config()
        self.hide_settings()
        self.start_menu()
        
    def show_restart_menu(self, *event):
        self.config()
        self.finish.pack(expand=1)
        self.restart_btn.place(x=300,y=350)
        self.hide_settings()
        self.cmd_btn.place(relx=.925, rely=.025)
        
        self.settings_btn['command'] = self.hide_restart_menu
        
    def hide_restart_menu(self, *event):
        self.restart_btn.place_forget()
        self.finish.pack_forget()
        self.cmd_btn.place_forget()
        
        self.settings(1)
        
    def settings(self, func = 0):
        commands = [self.hide_and_start_menu, self.show_restart_menu]
        self.start_btn.pack_forget()
        self.cmd_btn.place_forget()
        self.settings_btn['command'] = commands[func]
        
        self.settings_frame_0.place(x=100, y=30)
        self.settings_frame_1.place(x=315, y=30)
        self.settings_frame_2.place(x=478, y=30)
        self.settings_frame_3.place(x=100, y=150)
        self.settings_frame_4.place(x=322, y=150)
        
    def hide_settings(self, *event):
        self.settings_frame_0.place_forget()
        self.settings_frame_1.place_forget()
        self.settings_frame_2.place_forget()
        self.settings_frame_3.place_forget()
        self.settings_frame_4.place_forget()
        
    def start_math(self):
        self.task_label.config(text=self.get_task(self.count_nums))
        self.set_widgets()
        self.start_thread_timer()
        self.start_btn.pack_forget()
        self.settings_btn.place_forget()
        self.cmd_btn.place_forget()
        
    def set_widgets(self):
        self.answer_input.place(x=275,y=270)
        self.task_label.config(bg='#f0f0f0', fg='#f0f0f0')
        self.task_label.place(x=275,y=130)
        self.master.update()
        self.task_label.place(x=275+(210-self.task_label.winfo_width())/2,y=130)
        self.task_label.config(bg='lightgreen', fg='black')
        self.cmd_btn.place(relx=.925, rely=.025)
        self.pause_btn.place(x=715, y=50)
        
        if self.infinity_value.get() == 0: self.timer_label.place(x=725,y=5)
        else: self.timer_label.place(x=15,y=5)
            
    def start_thread_timer(self):
        self.target = Thread(target=self.start_timer)
        self.target.start()
        
    def restart(self, *event):
        self.faws = 0
        self.taws = 0
        self.answers = []
        
        self.restart_btn.place_forget()
        self.finish.pack_forget()
        self.settings_btn.place_forget()
        self.cmd_btn.place_forget()
        
        self.answer_input['state'] = NORMAL
        
        self.task_label.config(text=self.get_task(self.count_nums))
        self.answer_input.delete(0, END)
        
        self.answer_input.place(x=275,y=270)
        
        self.task_label.config(bg='#f0f0f0', fg='#f0f0f0')
        self.task_label.place(x=275,y=130)
        self.master.update()
        self.task_label.place(x=275+(210-self.task_label.winfo_width())/2,y=130)
        self.task_label.config(bg='lightgreen', fg='black')
        
        if self.infinity_value.get() == 1:
             self.timer_label.config(text='Бесконечное время')
             self.timer_label.place(x=15,y=5)
        else:
            self.timer_label.config(text=str(self.start_seconds))
            self.timer_label.place(x=725,y=5)
            self.pause_btn.place(x=715, y=50)
            
        if self.infinity_value.get() == 1:
            self.stop_btn.pack(side=RIGHT)
        else:
            self.start_thread_timer()
        
    def start_timer(self):
        try:
            i = 0
            while i != self.start_seconds + 1:
                if self.timer_paused:
                    pass
                else:
                    self.update_timer()
                    sleep(0.98)
                    i += 1
        except:
            pass
            
    def end_timer(self):
        self.answer_input['state'] = DISABLED
        self.answer_input.place_forget()
        self.task_label.place_forget()
        
        self.timer_label.pack_forget()
        self.timer_label.place_forget()
            
        self.finish.config(text=self.get_statics())
        
        self.finish.pack(expand=1)
        self.restart_btn.place(x=300,y=350)
        
        self.settings_btn['command'] = self.hide_restart_menu
        self.settings_btn.place(relx=0.025, rely=0.025)
        
        self.cmd_btn.place(relx=.925, rely=.025)
        self.pause_btn.place_forget()
        
        if self.infinity_value.get() == 1:
            self.stop_btn.pack_forget()
        if self.cmd_work:
            text = self.answers
            self.mathcmd.insert_math_log('answers', text)
        
    def update_timer(self):
        seconds = int(self.timer_label['text'])
        if seconds == 0:
            self.end_timer()
        else:
            colors = ['green', 'orange', '#f80000']
            color = int((seconds-1)/ceil(self.start_seconds / len(colors)))+1
            self.timer_label.config(text=str(seconds-1), fg=colors[-color])
            
            
    def get_statics(self):
        word = ''
        if self.taws // 10 * 10 + 1 == self.taws:
            word = 'пример'
        elif 5 >= self.taws >=20 or int(str(self.taws)[-1]) in [5,6,7,8,9,0]:
            word = 'примеров'
        elif int(str(self.taws)[-1]) in [2,3,4]:
            word = 'примера'
            
        if self.taws > 0:
            if self.infinity_value.get() == 0:
                text = 'Вы решили {} {} за {} секунд\n'.format(self.taws, word, self.start_seconds)
                text += 'Ср. время решения: {} секунд\n'.format(round(self.start_seconds/self.taws, 2))
                text += 'Всего попыток: {}\n'.format(self.taws + self.faws)
            else:
                text = 'Вы решили {} {}\n'.format(self.taws, word)
                text += 'Всего попыток: {}\n'.format(self.taws + self.faws)
        else:
            if self.infinity_value.get() == 0: 
                text = 'Вы не решили ни один пример за {} секунд\n'.format(self.start_seconds)
                text += 'Всего попыток: {}\n'.format(self.taws + self.faws)
            else:
                text = 'Вы не решили ни один пример\n'
                text += 'Всего попыток: {}\n'.format(self.taws + self.faws)
        
        return text
        
    def check_answer(self, *event):
        try:
            user_answer = float(self.answer_input.get())
            if float(user_answer) == self.answer or int(user_answer) == self.answer:
                if self.cmd_work:
                    text = '[MATH]Правильный ответ! {0} = {1}'.format(self.task, self.answer)
                    self.mathcmd.insert_math_log('true_answer', text)
                self.task_label.config(text=self.get_task(self.count_nums))
                
                self.master.update()
                width = self.task_label.winfo_width()
                self.task_label.place(x=275+(210-width)/2, y=130)
                
                self.answer_input.delete(0, END)
                self.taws += 1
            else:
                if self.cmd_work:
                    text = '[MATH]Неправильный ответ!'
                    self.mathcmd.insert_math_log('false_answer', text)
                    
                self.faws += 1
        except ValueError as e:
            if self.cmd_work:
                text = '[MATH]Ошибка в вводе!'
                self.mathcmd.insert_math_log('error', text)
        
    def get_task(self, n=3):
        task = "";
        
        for i in range(n):
            task += str(randint(self.min_num, self.max_num))
            task += choice(self.arithmetics)
       
        self.task = self.check_task(task)
        self.answer = eval(self.task)
        if '/' in self.arithmetics:
            if type(self.answer) == float:
                dot = str(self.answer).find('.')
                self.answer = float(str(self.answer)[:1+dot + int(self.nums_after_zap.get())])
        if int(self.answer) == float(self.answer):
            self.answer = int(self.answer)
        else:
            self.answer = float(self.answer)
        self.answers.append('[MATH]Пример: {} Ответ: {}'.format(self.task, self.answer))
        if self.cmd_work:
            text = '[MATH]Пример: ' + self.task
            self.mathcmd.insert_math_log('new_task', text)
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
        
    def destroy(self):
        self.master.destroy()

    def closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()
            
    def create_cmd(self,*event):           
        if self.cmd_work:
            self.mathcmd.withdraw()
            self.cmd_work = False
        else:
            self.mathcmd.deiconify()
            self.cmd_work = True

    def mainloop(self):
        self.master.protocol("WM_DELETE_WINDOW", self.closing)
        self.master.mainloop()
        
def run_app():
    root = Tk()
    app = Math(root)
    return app


