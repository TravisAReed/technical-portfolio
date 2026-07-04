#allows the running of commands from a python shell

print('running commands ...')

import subprocess

subprocess.run(f"echo hello",shell=True, check=True) #prints "hello" in the terminal as if the first argument was directly inputted into the terminal