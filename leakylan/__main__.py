
# Leaky LAN
# Copyright (c) 2021 ANISH M < aneesh25861@gmail.com >

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
A simple file sharing service using python http.server and flask module
developed by M.Anish <aneesh25861@gmail.com> to avoid third party code .

'''
import os
import sys
import platform
import socket
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/files"
TEMPLATES_FOLDER = os.getcwd()

app = Flask(__name__, template_folder = TEMPLATES_FOLDER)
# To clear screen.
os.system('cls' if platform.system().lower() == 'windows' else 'clear')

print('''

##       ########    ###    ##    ## ##    ##    ##          ###    ##    ## 
##       ##         ## ##   ##   ##   ##  ##     ##         ## ##   ###   ## 
##       ##        ##   ##  ##  ##     ####      ##        ##   ##  ####  ## 
##       ######   ##     ## #####       ##       ##       ##     ## ## ## ## 
##       ##       ######### ##  ##      ##       ##       ######### ##  #### 
##       ##       ##     ## ##   ##     ##       ##       ##     ## ##   ### 
######## ######## ##     ## ##    ##    ##       ######## ##     ## ##    ## 


                      Simple File sharing over LAN.
           
              Developed by M.Anish <aneesh25861@gmail.com>  
 
 Note: Files shared using this tool is available to each and every device 
 connected to LAN. Don't use on public Networks! 
              
''')

def getip(port = ':8000'):

    flag=0
    # Code specific to windows operating system.
    if platform.system().lower() == 'windows':
        os.system('ipconfig >temp.txt')
        if os.path.exists('temp.txt'):
            with open('temp.txt') as f:
                buff = f.readlines()
                for x in range(len(buff) - 1):

                     # To get ip address if user is connected to ethernet or wifi and ignore all other network interfaces.
                    if 'Ethernet adapter Ethernet' in buff[x] or 'Wireless LAN adapter' in buff[x]:
                        for i in range(6):
                            x += 1
                            try:
                                if 'IPv4' in buff[x]:
                                    print('Enter in Browser :',buff[x].split()[-1],port)
                                    flag = 1
                                    break

                            # Ignore index errors , it wont affect program functionality anyway.     
                            except IndexError:
                                pass
                    
            os.remove('temp.txt')

        # error message incase temp.text couldnot be created.                           
        else:
            print('Permission Denied!')
    else:
          os.system('ip a >temp.txt')
          if os.path.exists('temp.txt'):
              with open('temp.txt') as f:
                  for x in f:
                      if ('inet ' in x) and ('127.0.0.1' not in x):
                          print('Enter in Browser :',x.split()[1].split('/')[0],port)
                          flag = 1
                          break
              os.remove('temp.txt') 

          # error message incase temp.text couldnot be created.    
          else:
              print('Permission Denied!')

    return flag
 

# variable to mark recieving mode.
xflag = 0

# Flag is set to 1 if sharing is successful.
flag = 0

# function to recieve files
def recieve():

    # set xflag to mark recieving mode.
    xflag = 1

    app.config['UPLOAD_FOLDER'] = os.getcwd() + UPLOAD_FOLDER
    # start copying required files to recieve files.
    if os.path.exists("files") is False:
        os.mkdir("files")
        print("All your recieved files will be stored at " + os.getcwd() + "/files")

    flag = getip(':9000')
    
    # Recieving mode.
    if xflag == 1 and flag == 1:
        try:
            # Run the flask app.
            app.run(host = '0.0.0.0', port = 9000)
        except KeyboardInterrupt:
            print('Program Exited Successfully!')
            sys.exit(0)
    
    # Throw error if ipv4 address couldnot be obtained.    
    else:
        print("It seems Your Device is NOT connected to any Network !")

def serve():
    # To get Folder whose files are to be shared. 
    folder = input('Enter Folder name:')

    # To check if folder entered by user is valid or not.
    try:
        os.chdir(folder)
    except Exception as e:
        print('Folder Not Found :(')
        choice = input("\nDo you want to share "+ os.getcwd()  + " in the local network ? (yes/no)\n=>>")
        print()
        if choice.lower() != "yes":
           sys.exit()

    flag = getip()

    # If getting an ipv4 address for sharing successful start server.
    if flag == 1:
        try:
            # start python http.server at default port 8000
            os.system('py -m http.server ' if platform.system().lower() == 'windows' else 'python3 -m http.server')
        except KeyboardInterrupt:
            print('Program Exited Successfully!')
            sys.exit(0)
    
    # Throw error if ipv4 address couldnot be obtained.    
    else:
        print("It seems Your Device is NOT connected to any Network !")

# menu
def menu():
    
    print(" Menu :-")
    print("\n 1) Share Files \n 2) Recieve Files")
    ch = input("\nEnter choice:")
    while 1:
        if ch not in ('1','2','c','close','exit'):
            print("\n\ainvalid choice selected!\n")
            ch = input("\n Enter choice:")
        else:
            break

    if ch == '2':
        
        recieve()

        # To clear screen.
        os.system('cls' if platform.system().lower() == 'windows' else 'clear')
        menu()

    elif ch in ('c','close','exit'):
        sys.exit()

    else:
        serve()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        ip_address = get_ip_address()
        return render_template('index.tmpl', server_ip_address = ip_address)
    elif request.method == 'POST':
        file = request.files['filename']
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            return "File is saved"
        except FileNotFoundError:
            return "File not found"
        except IsADirectoryError:
            return "File not chosen"

if __name__ == "__main__":
    menu()


