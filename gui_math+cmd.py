from subprocess import Popen
from termcolor import cprint


args = ['python', 'gui_math.pyw']

print('===МАТЕМАТИКА====')
commands = 'Перезагрузка: <Enter>\nВыключение: <STOP>'
print(commands)
process = Popen(args)
print('====СТАРТ====\n')

start = 0
try:
    while True:
        if start == 1:
            process = Popen(args)
            start = 0
        command = input()
        if command == '':
            process.kill()
            print('Перезагрузка программы...')
            start = 1
        elif command == 'STOP':
            process.kill()
            break
except:
    print('Error!')
