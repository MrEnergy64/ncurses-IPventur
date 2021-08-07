# coding: utf-8
#!/usr/bin/python3
# IPventur-Python-1.0v5
# recommend root rights, need nmap
# updated: 06.05.2021 Norman Woeske
# Version: beta v5
# for Windows needs pypiwin32, windows-curses, demjson, simplejson, python3-nmap
# for Linux needs simplejson, demjson, python3-nmap,



import curses
import nmap3
import json
import ipaddress
import sys,os,platform,datetime,time,subprocess
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
            User = "Normal User - linited scan"
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
            sys.exit()

def fenster(os_version,NmapOK,User):
    text = ("IPventur Python 1.0v5 by Norman Woeske")
    text2 = datetime.datetime.now()
    zeit = text2.strftime("%Y-%m-%d %H:%M:%S")
    h, w = screen.getmaxyx()
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
    screen.addstr(y, x, text)
    screen.addstr(y, x2+40, zeit)
    screen.addstr(y+1, x2+40, f'(OS is: {os_version})')
    screen.addstr(y+1, 2, f'(User is: {User})')
    screen.attroff(curses.color_pair(1))

def whichIP(ScreenDel):
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
            ip = ip[:-1]
        elif ip == "q" or ip == "Q":
            screen.addstr(10, 3, 'You would like to leave ')
            time.sleep(2)
            sys.exit()
        elif char == '\n':
            try:
                ipaddress.ip_network(f'{ip}')
                screen.addstr(10, 3, 'Valid IP adress(es) entered!', curses.A_REVERSE)
                time.sleep(2)
                screen.addstr(10, 3, f'OK, you would like to scan {ip}', curses.A_REVERSE)
                time.sleep(2)
                return ip, head
            except ValueError:
                screen.addstr(10, 3, 'No valid IP adress(es) entered! Restarting Program ....', curses.A_REVERSE)
                time.sleep(2)
                main()
                #os.system(f'{ScreenDel}')
                #sys.exit()

def scanOption(ip):
    technic = ''
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    q2 = f"Which nmap scan techniques would you like? IP: {ip}"
    box2 = curses.newwin(3, 4, 18, 2)
    box2.immedok(True)
    box2.box()
    while True:
        screen.attron(curses.color_pair(2))
        screen.addstr(6, 3, q2)
        screen.attroff(curses.color_pair(2))
        screen.attron(curses.color_pair(1))
        screen.addstr(8, 2, "for non root/admin rights:")
        screen.attroff(curses.color_pair(1))
        screen.addstr(9, 2, " 1. nmap_ping_scan \t2. nmap_list_scan \t3. nmap_dns_brute_script \t4. scan_top_ports")
        screen.attron(curses.color_pair(1))
        screen.addstr(11, 2, "for root/admin rights:")
        screen.attroff(curses.color_pair(1))
        screen.addstr(12, 2, " 5. nmap_detect_firewall \t 6. nmap_os_detection (not yet for Windows)")
        screen.addstr(13, 2, " 7. nmap_portscan_only \t 8. nmap_stealth_scan")
        screen.addstr(14, 2, " 9. nmap_subnet_scan \t\t10. nmap_version_detection")
        screen.attron(curses.color_pair(2))
        screen.addstr(17, 2, "Please choose scan technic number? (for exit use \"q\" and ENTER) ")
        screen.addstr(19, 3, technic)
        screen.attroff(curses.color_pair(2))

        char = screen.get_wch()
        if isinstance(char, str) and char.isprintable():
            # add scan technic number
            technic += char
        elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
            technic = technic[:-1]
        elif technic == "q" or technic == "Q":
            screen.addstr(19, 7, 'You would like to leave the program, bye....')
            time.sleep(2)
            sys.exit()
        elif technic in ("1","2","3","4","5","6","7","8","9","10"):
            if technic == "1":
                stechnic = "ping"
                return technic, stechnic
            if technic == "2":
                stechnic = "list"
                return technic, stechnic
            if technic == "3":
                stechnic = "dns"
                return technic, stechnic
            if technic == "4":
                stechnic = "top"
                return technic, stechnic
            if technic == "5":
                stechnic = "fw"
                return technic, stechnic
            if technic == "6":
                stechnic = "os_version"
                return technic, stechnic
            if technic == "7":
                stechnic = "ports"
                return technic, stechnic
            if technic == "8":
                stechnic = "stealth"
                return technic, stechnic
            if technic == "9":
                stechnic = "subnet"
                return technic, stechnic
            if technic == "10":
                stechnic = "version"
                return technic, stechnic

        else:
            screen.addstr(19, 8, f'Wrong Number {technic}')
            time.sleep(2)


def scannen(technic,ip):
    stechnic = ''
    ipdone = ''
    results = ''
    if technic == "1":
        screen.addstr(6, 3, f'Scan-Technic: nmap.nmap_ping_scan ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmapscan.nmap_ping_scan(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "2":
        screen.addstr(6, 3, f'Scan-Technic: nmapscan.nmap_list_scan ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.nmap_list_scan(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "3":
        screen.addstr(6, 3, f'Scan-Technic: nmap_dns_brute_script ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.nmap_dns_brute_script(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "4":
        screen.addstr(6, 3, f'Scan-Technic: scan_top_ports ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.scan_top_ports(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "5":
        screen.addstr(6, 3, f'Scan-Technic: nmap_detect_firewall ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.nmap_detect_firewall(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "6":
        screen.addstr(6, 3, f'Scan-Technic: nmap_os_detection ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.nmap_os_detection(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "7":
        screen.addstr(6, 3, f'Scan-Technic: nmap_portscan_only ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmaphost.nmap_portscan_only(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "8":
        stechnic = "nmap_stealth_scan"
        screen.addstr(6, 3, f'Scan-Technic: nmap_stealth_scan ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.nmap_stealth_scan(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "9":
        screen.addstr(6, 3, f'Scan-Technic: nmap_subnet_scan ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.nmap_subnet_scan(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output
    elif technic == "10":
        screen.addstr(6, 3, f'Scan-Technic: nmap_version_detection ({ip})', curses.A_REVERSE)
        screen.addstr(8, 3, 'scanning now .....  (please wait, scan be long depends of the scan technique and subnet length)', curses.A_REVERSE)
        results = nmap.nmap_version_detection(f'{ip}')
        screen.addstr(10, 3, 'DONE!', curses.A_REVERSE)
        output = str(results)
        time.sleep(2)
        return output

def ausgabe(output,stechnic,head):
    outputformat = ''
    splitoutput = ''
    datum = datetime.date.today()
    q3 = "Which output file format would you like:"
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
            outputformat = outputformat[:-1]
        elif char == '\n' or char == curses.KEY_ENTER:
            if outputformat == "1":
                screen.addstr(13, 3, f'Output-Format: Text-Format, saving file......', curses.A_REVERSE)
                splitoutput = output.replace(",", "\n")
                sys.stdout = open(f"output-nmap-text-{stechnic}-{head}-{datum}.txt", "w")
                print(splitoutput)
                sys.stdout.close()
                screen.addstr(15, 3, f'Scan completed. Please check out file output-nmap-text-{stechnic}-{head}-{datum}.txt')
                t = 5
                while t > 0:
                    screen.addstr(17, 3, f'{t} Seconds to quit', curses.A_REVERSE)
                    t -= 1
                    time.sleep(1)
                cmd = f'''\n
                ******************************************************************************************
                *** type >> more output-nmap-text-{stechnic}-{head}-{datum}.txt << to see the results ***
                ******************************************************************************************\n\n'''
                sys.exit(cmd)
            if outputformat == "2":
                screen.addstr(13, 3, f'Output-Format: Json-Format, saving file......', curses.A_REVERSE)
                jsonoutput=(json.dumps(output, indent=4, sort_keys=True))
                sys.stdout = open(f"output-nmap-json-{stechnic}-{head}-{datum}.txt", "w")
                print(jsonoutput)
                sys.stdout.close()
                screen.addstr(15, 3, f'Scan completed. Please check out file output-nmap-json-{stechnic}-{head}-{datum}.txt')
                t = 5
                while t > 0:
                    screen.addstr(17, 2, f'{t} Seconds to quit', curses.A_REVERSE)
                    t -= 1
                    time.sleep(1)
                cmd2 = f'''\n
                ******************************************************************************************
                *** type >> more output-nmap-json-{stechnic}-{head}-{datum}.txt << to see the results ***
                ******************************************************************************************\n\n'''
                sys.exit(cmd2)
        elif technic == "q":
            sys.exit()
        else:
            screen.addstr(23, 38, f'Wrong Number {outputformat}')

def main():
    os_version,User,ScreenDel,cmd = whichOS_whichUser()
    NmapOK=exist_NMAP(cmd)
    fenster(os_version,NmapOK,User)
    ip, head = whichIP(ScreenDel)
    fenster(os_version,NmapOK,User)
    technic,stechnic=scanOption(ip)
    fenster(os_version,NmapOK,User)
    output = scannen(technic,ip)
    fenster(os_version,NmapOK,User)
    ausgabe(output,stechnic,head)


# Start Main Programm
main()
