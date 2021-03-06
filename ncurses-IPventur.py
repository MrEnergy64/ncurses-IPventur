# coding: utf-8
#!/usr/bin/python3
# ncurses-IPventur.py
# recommend root rights, need nmap
# updated: 25.08.2021 Norman Woeske
# Version: 1.5
# for Windows needs tqdm,pypiwin32, windows-curses, demjson, simplejson, python3-nmap
# for Linux needs simplejson, demjson, python3-nmap,
IPversion = "1.5"


import curses
import nmap3
import json
import ipaddress
import sys,os,platform,datetime,time,subprocess
from tqdm import tqdm

screen = curses.initscr()
curses.start_color()
nmap = nmap3.Nmap()
nmapscan = nmap3.NmapScanTechniques()
nmaphost = nmap3.NmapHostDiscovery()


screen.immedok(True)
screen.keypad(True)

User = ''
Nmapwin = ''
Nmaplinux = ''
cmd = ''
NmapOK = ''
ScreenDel = ''
os_version = ''
output = ''
splitoutput = ''
ip = ''
mask = ''
ip_done = False
technic = ''
stechnic = ''
outputformat = ''
t = ''
cmd2 = ''
datum = ''
zeit = ''
outputformat = ''


def whichOS_whichUser():
    os_version = platform.system()
    if os_version == "Windows":
        ScreenDel = "cls"
        import win32api
        check = win32api.GetConsoleTitle()
        cmd = "where" if platform.system() == "Windows" else "which"
        if "Administrator" in check:
            User = "Administrator"
            return os_version, User, ScreenDel, cmd
        else:
            User = "Normal User - limited scan"
            return os_version, User, ScreenDel, cmd
    else:
        ScreenDel = "clear"
        cmd = "where" if platform.system() == "Windows" else "which"
        if os.geteuid()==0:
            User = "Root User"
            return os_version, User, ScreenDel, cmd
        else:
            User = "Normal User - limited scan"
            return os_version, User, ScreenDel, cmd

def exist_NMAP(cmd):
    if cmd=="where":
        Nmapwin = subprocess.call([cmd, "nmap.exe"], stdout=subprocess.PIPE)
        if Nmapwin == 0:
            NmapOK = "Windows nmap.exe exists!"
            return NmapOK
        else:
            os.system(ScreenDel)
            print("""
            ! No nmap exist! Please install nmap first. Leaving program.... !
            """)
            if os_version == "Linux":
                    fix = "stty sane"
                    os.system(fix)
            curses.endwin()
            sys.exit()
    if cmd=="which":
        Nmaplinux = subprocess.call([cmd, "nmap"], stdout=subprocess.PIPE)
        if Nmaplinux == 0:
            NmapOK = "Linux nmap.exe exists!"
            return NmapOK
        else:
            os.system(ScreenDel)
            print("""
            ! No nmap exist! Please install nmap first. Leaving program.... !
            """)
            fix = "stty sane"
            curses.endwin()
            if os_version == "Linux":
                    fix = "stty sane"
                    os.system(fix)
            sys.exit()

def fenster(os_version,NmapOK,User):
    text = (f"IPventur Python {IPversion} by Norman Woeske")
    text2 = datetime.datetime.now()
    zeit = text2.strftime("%d-%m-%Y %H:%M:%S")
    h, w = screen.getmaxyx()
    if h <= 32 or w <= 110:
        warning = f'\n!!! Sorry, but your windows terminal size is not h33 x w111 (actual: h{h} x w{w}). Program has been stopped !!! \n'
        sys.exit(warning)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    x = w//2 - len(text)//2
    x2 = w//2 - len(zeit)//2
    x3 = w//2 - len(os_version)//2
    y = 2
    screen.clear()
    screen.attron(curses.color_pair(1))
    screen.border(0)
    screen.addstr(y, 2, NmapOK)
    screen.addstr(y, x+3, text)
    screen.addstr(y+1, x+4, f"Your Screensize is: w{w} x h{h}", curses.A_REVERSE)
    screen.addstr(y, w-25, zeit)
    screen.addstr(y+1, w-25, f'OS is: {os_version}', curses.A_REVERSE)
    screen.addstr(y+1, 2, f'User is: {User}',curses.A_REVERSE)
    screen.attroff(curses.color_pair(1))

def whichIP(ScreenDel, os_version):
    ip = ''
    q1 = "Which v4 IP/range (/32 for single IP) would you like to scan? (for exit use \"q\" and ENTER)"
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    box1 = curses.newwin(3, 30, 7, 2)
    box1.immedok(True)
    box1.box()


    while True:
        screen.attron(curses.color_pair(2))
        screen.addstr(6, 3, q1)
        screen.addstr(8, 4, ip)
        screen.attroff(curses.color_pair(2))

        head, sep, tail = ip.partition('/')

        char = screen.get_wch()
        if isinstance(char, str) and char.isprintable():
            # add IP address or range to variable ip
            ip += char

        elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
            screen.clrtoeol()
            ip = ip[:-1]
        elif ip == "q" or ip == "Q":
            screen.addstr(8, 32, ' Leaving program...... ')
            time.sleep(2)
            curses.endwin()
            if os_version == "Linux":
                    fix = "stty sane"
                    os.system(fix)
            sys.exit()
        elif char == '\n':
            try:
                ipaddress.ip_network(f'{ip}')
                screen.addstr(10, 3, 'Valid IP adress(es) entered!', curses.A_REVERSE)
                time.sleep(1)
                screen.addstr(10, 3, f'OK, you would like to scan {ip}', curses.A_REVERSE)
                time.sleep(1)
                return ip, head
            except ValueError:
                screen.addstr(10, 3, 'No valid IP adress(es) entered! Restarting Program ....', curses.A_REVERSE)
                time.sleep(2)
                main()


def scanOption(ip, os_version, User):
    technic = ''
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    q2 = f"Which nmap scan techniques would you like do with IP: {ip} ?"
    box2 = curses.newwin(3, 4, 22, 3)
    box2.immedok(True)
    box2.box()
    while True:
        screen.attron(curses.color_pair(2))
        screen.addstr(6, 3, q2)
        screen.attroff(curses.color_pair(2))
        screen.attron(curses.color_pair(1))
        screen.addstr(8, 3, "for non root/admin rights:")
        screen.attroff(curses.color_pair(1))
        screen.addstr(9, 3, " ( 1) nmap_ping_scan \t( 2) nmap_tcp_scan \t\t\t( 3) scan_top_ports \t\t")
        screen.addstr(10, 3, " ( 4) nmap_portscan_only \t( 5) nmap_list_scan ")
        screen.attron(curses.color_pair(1))
        screen.addstr(12, 3, "for root/admin rights:")
        screen.attroff(curses.color_pair(1))
        screen.addstr(13, 3, " ( 6) nmap_os_detection \t( 7) nmap_udp_scan (timeintensive) \t( 8) nmap_version_detection")
        screen.addstr(14, 3, " ( 9) nmap_arp_discovery (you must be in the same IP scan-range)")
        screen.attron(curses.color_pair(2))
        screen.attron(curses.color_pair(1))
        screen.addstr(16, 3, "some utils and infos:")
        screen.attroff(curses.color_pair(1))
        screen.addstr(17, 3, " (10) python3-nmap version \t(11) nmap3 author")
        screen.addstr(18, 3, " (12) nmap3 last modified \t(13) nmap version")
        screen.addstr(20, 3, "Please choose scan technic number? (for exit use \"q\" and ENTER) ")
        screen.addstr(23, 4, technic)
        screen.attroff(curses.color_pair(2))

        char = screen.get_wch()
        if isinstance(char, str) and char.isprintable():
            # add scan technic number
            technic += char
        elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
            screen.clrtoeol()
            technic = technic[:-1]
        elif technic == "q" or technic == "Q":
            screen.addstr(30, 3, 'You would like to leave the program, bye....')
            time.sleep(2)
            if os_version == "Linux":
                    fix = "stty sane"
                    os.system(fix)
            curses.endwin()
            sys.exit()
        elif technic in ("1","2","3","4","5","6","7","8","9","10","11","12","13"):
            if technic == "1":
                stechnic = "ping"
                return technic, stechnic
            if technic == "2":
                stechnic = "tcp"
                return technic, stechnic
            if technic == "7":
                if User == "Normal User - limited scan":
                    screen.addstr(27, 3, "Sorry, you are not a root user, this nmap scan will work for root/admin user only!")
                    screen.addstr(28, 3, "Please choice again...")
                    time.sleep(3)
                    screen.clear()
                    fenster(os_version,NmapOK,User)
                    scanOption(ip, os_version, User)
                stechnic = "udp"
                return technic, stechnic
            if technic == "3":
                stechnic = "top"
                return technic, stechnic
            if technic == "4":
                stechnic = "ports"
                return technic, stechnic
            if technic == "5":
                stechnic = "list"
                return technic, stechnic
            if technic == "6":
                if User == "Normal User - limited scan":
                    screen.addstr(27, 3, "Sorry, you are not a root/admin user, this nmap scan will work for root/admin user only!")
                    screen.addstr(28, 3, "Please choice again...")
                    time.sleep(3)
                    screen.clear()
                    fenster(os_version,NmapOK,User)
                    scanOption(ip, os_version, User)
                stechnic = "os"
                return technic, stechnic
            if technic == "8":
                if User == "Normal User - limited scan":
                    screen.addstr(27, 3, "Sorry, you are not a root/admin user, this nmap scan will work for root/admin user only!")
                    screen.addstr(28, 3, "Please choice again...")
                    time.sleep(3)
                    screen.clear()
                    fenster(os_version,NmapOK,User)
                    scanOption(ip, os_version, User)
                stechnic = "version"
                return technic, stechnic
            if technic == "9":
                if User == "Normal User - limited scan":
                    screen.addstr(27, 3, "Sorry, you are not a root/admin user, this nmap scan will work for root/admin user only!")
                    screen.addstr(28, 3, "Please choice again...")
                    time.sleep(3)
                    screen.clear()
                    fenster(os_version,NmapOK,User)
                    scanOption(ip, os_version, User)
                stechnic = "arp"
                return technic, stechnic
            if technic == "10":
                utils_result = nmap3.utils.__version__
                screen.attron(curses.color_pair(1))
                screen.addstr(23, 9, f" python3-nmap version is: {utils_result}")
                screen.attroff(curses.color_pair(1))
                time.sleep(4)
                screen.addstr(25, 10, "Back to menu...")
                time.sleep(2)
                screen.clear()
                fenster(os_version,NmapOK,User)
                scanOption(ip, os_version, User)
            if technic == "11":
                utils_result = nmap3.utils.__author__
                screen.attron(curses.color_pair(1))
                screen.addstr(23, 9, f" python3-nmap author is: {utils_result}")
                screen.attroff(curses.color_pair(1))
                time.sleep(4)
                screen.addstr(25, 10, "Back to menu...")
                time.sleep(2)
                screen.clear()
                fenster(os_version,NmapOK,User)
                scanOption(ip, os_version, User)
            if technic == "12":
                utils_result = nmap3.utils.__last_modification__
                screen.attron(curses.color_pair(1))
                screen.addstr(23, 9, f" python3-nmap was last modified on: {utils_result}")
                screen.attroff(curses.color_pair(1))
                time.sleep(4)
                screen.addstr(25, 10, "Back to menu...")
                time.sleep(2)
                screen.clear()
                fenster(os_version,NmapOK,User)
                scanOption(ip, os_version, User)
            if technic == "13":
                utils_result = nmap.nmap_version()
                screen.attron(curses.color_pair(1))
                screen.addstr(24, 9, f" You are using nmap version: \n\n{utils_result}")
                screen.attroff(curses.color_pair(1))
                time.sleep(4)
                screen.addstr(29, 9, " Back to menu...")
                time.sleep(2)
                screen.clear()
                fenster(os_version,NmapOK,User)
                scanOption(ip, os_version, User)

        else:
            screen.addstr(25, 8, f'Wrong Number {technic}')
            time.sleep(2)


def scannen(technic,ip, os_version):
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    text2 = 'scanning now .....  (scanning time can be long depends of the nmap scan technique and subnet length) '
    text3 = 'Estimate scanning time as root for a /24 subnet: '
    text4 = '- arp scan: 256 IP addresses (22 hosts up) scanned in 1072.20 seconds = around 18 minutes '
    text5 = '- udp scan: 256 IP addresses (22 hosts up) scanned in 1878.97 seconds = around 32 minutes '
    text6 = '- tcp scan: 256 IP addresses (20 hosts up) scanned in 1070.30 seconds = around 18 minutes '
    text7 = 'Please wait.... '
    stechnic = ''
    ipdone = ''
    results = ''
    if technic == "1":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmap.nmap_ping_scan ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmapscan.nmap_ping_scan(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "2":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmapscan.nmap_tcp_scan ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmapscan.nmap_tcp_scan(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "7":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmapscan.nmap_udp_scan ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmapscan.nmap_udp_scan(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "3":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: scan_top_ports ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmap.scan_top_ports(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "4":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmap_portscan_only ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmaphost.nmap_portscan_only(f'{ip}')
        warten = len(results)
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "5":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmap_list_scan ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmap.nmap_list_scan(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "6":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmap_os_detection ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmap.nmap_os_detection(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "8":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmap_version_detection ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmap.nmap_version_detection(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results
    elif technic == "9":
        screen.attron(curses.color_pair(3))
        screen.addstr(6, 3, f'Scan-Technic: nmap_arp_discovery ({ip})')
        screen.attroff(curses.color_pair(3))
        screen.addstr(8, 3, text2, curses.A_REVERSE)
        screen.addstr(12, 3, text3)
        screen.addstr(14, 3, text4)
        screen.addstr(15, 3, text5)
        screen.addstr(16, 3, text6)
        screen.addstr(18, 3, text7)
        screen.addstr(20, 3, "")
        results = nmaphost.nmap_arp_discovery(f'{ip}')
        screen.addstr(18, 20, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output, results


def ausgabe(output,results,stechnic,head,os_version):
    text2 = datetime.datetime.now()
    zeit = text2.strftime("%d%m%Y-%H%M")
    restart = ''
    outputformat = ''
    splitoutput = ''

    q3 = "Which output file format would you like (or q and ENTER to quit):"
    q4 = "1. Text-Format ?"
    q5 = "2. Json-Format ?"
    box3 = curses.newwin(3, 4, 10, 3)
    box3.immedok(True)
    box3.box()
    while True:
        screen.attron(curses.color_pair(2))
        screen.addstr(6, 3, q3)
        screen.addstr(7, 3, q4)
        screen.addstr(8, 3, q5)
        screen.attroff(curses.color_pair(2))
        screen.addstr(11, 4, outputformat)

        char = screen.get_wch()
        if isinstance(char, str) and char.isprintable():
            outputformat += char
        elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
            screen.clrtoeol()
            outputformat = outputformat[:-1]
        elif char == '\n' or char == curses.KEY_ENTER:
            if outputformat == "1":
                screen.addstr(13, 3, 'Output-Format: Text-Format, saving file......', curses.A_REVERSE)
                splitoutput = output.replace(",", "\n")
                sys.stdout = open(f"output-nmap-{stechnic}-{head}-{zeit}.txt", "w")
                print(splitoutput)
                sys.stdout.close()
                screen.addstr(15, 3, f'Scan completed. Please check out file output-nmap-{stechnic}-{head}-{zeit}.txt')
                outputformat="txt"
                return outputformat,zeit
            if outputformat == "2":
                screen.addstr(13, 3, 'Output-Format: Json-Format, saving file......', curses.A_REVERSE)
                jsonoutput=(json.dumps(results, indent=4, sort_keys=True))
                sys.stdout = open(f"output-nmap-{stechnic}-{head}-{zeit}.json", "w")
                print(jsonoutput)
                sys.stdout.close()
                screen.addstr(15, 3, f'Scan completed. Please check out file output-nmap-{stechnic}-{head}-{zeit}.json')
                outputformat="json"
                return outputformat,zeit
            if outputformat == "q":
                screen.addstr(15, 3, 'Leaving the program...... ')
                time.sleep(2)
                curses.endwin()
                if os_version == "Linux":
                    fix = "stty sane"
                    os.system(fix)
                sys.exit()
        else:
            screen.addstr(23, 38, f'Wrong Number {outputformat}')

def new_start(outputformat,stechnic,head,os_version,zeit):
    new_start = ''
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    box4 = curses.newwin(3, 4, 16, 59)
    box4.immedok(True)
    box4.box()
    while True:
        screen.attron(curses.color_pair(2))
        screen.addstr(17, 3, 'Do you want to scan another IP/range? [ y/n and ENTER ] ')
        screen.addstr(17, 60, new_start)
        screen.attroff(curses.color_pair(2))
        char = screen.get_wch()
        if isinstance(char, str) and char.isprintable():
            new_start += char
        elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
            screen.clrtoeol()
            new_start = new_start[:-1]
        elif char == '\n' or char == curses.KEY_ENTER:
            if new_start == "y" or new_start == "Y":
                main()
            if new_start == "n" or new_start == "N":
                t = 3
                while t > 0:
                    screen.addstr(19, 3, f'{t} Seconds to see scan result. Good bye.', curses.A_REVERSE)
                    t -= 1
                    time.sleep(1)
                if os_version == "Linux":
                    fix = "stty sane"
                    os.system(fix)
                cmd = f'''\033c\n
                *********************************************************************************************
                *** type >> more output-nmap-{stechnic}-{head}-{zeit}.{outputformat} << to see the results ***
                *********************************************************************************************\n\n'''
                curses.endwin()
                if os_version == "Linux":
                    fix = "stty sane"
                    os.system(fix)
                os.system(f"more output-nmap-{stechnic}-{head}-{zeit}.{outputformat}")
                time.sleep(2)
                sys.exit(cmd)
            else:
                screen.addstr(19, 3, f'Wrong input {new_start}')
                time.sleep(2)
                screen.addstr(17, 60, new_start)
        else:
            screen.addstr(19, 3, f'Wrong input {new_start}')
            time.sleep(2)


def main():
    os_version, User, ScreenDel, cmd = whichOS_whichUser()
    NmapOK = exist_NMAP(cmd)
    fenster(os_version, NmapOK, User)
    ip, head = whichIP(ScreenDel, os_version)
    fenster(os_version, NmapOK, User)
    technic, stechnic = scanOption(ip, os_version, User)
    fenster(os_version, NmapOK, User)
    output, results = scannen(technic, ip, os_version)
    fenster(os_version, NmapOK, User)
    outputformat, zeit = ausgabe(output, results, stechnic, head, os_version)
    new_start(outputformat, stechnic, head, os_version, zeit)

# Start Main Programm
main()
