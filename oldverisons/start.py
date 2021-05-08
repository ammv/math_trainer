from subprocess import Popen

args = ['python', 'gui_math.pyw']
try:
    while True:
        process = Popen(args)
        input()
        process.kill()
except:
    print('Error!')
