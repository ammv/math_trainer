# from subprocess import Popen
from termcolor import cprint
from gui_math import MathCMD, run_app
from threading import Thread
# from gui_math import Math, run_app



# args = ['python', 'gui_math.pyw']

# def thread_mainloop(app):
    # target_2 = Thread(target=app.mainloop)
    # target_2.start()

app = run_app()
# thread_mainloop(app)

def thread_timer():
    global app
    target = Thread(target=app.start_timer)
    target.start()
    
mathcmd = MathCMD(app)
app.set_thread_timer(thread_timer)

commands = '''
Перезагрузка: <Enter>\nВыключение: <STOP>\n
Узнать ответ: <A>\nНовый пример: <N>\nОстановить игру: <S>\n'''

print('===МАТЕМАТИКА====')
print(commands)
print('====СТАРТ====\n')

start = 0
try:
    while True:
        if start == 1:
            app = run_app()
            # thread_mainloop(app)
            start = 0
        command = input()
        if command == '':
            app.destroy()
            print('Перезагрузка программы...')
            start = 1
        elif command == 'A':
            mathcmd.get_answer()
        elif command == 'N':
            mathcmd.skip_task()
        elif command == 'S':
            mathcmd.stop_decide()
        elif command == 'STOP':
            app.destroy()
            break
except Exception as e:
    print('Error!', e)
