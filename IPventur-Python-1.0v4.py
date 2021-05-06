#!/usr/bin/python3
# IPventur-Python-1.0
# recommend root rights, need nmap
# updated: 06.05.2021 Norman Woeske
# Version: beta v4


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

os_version = platform.system()
if os_version == "Windows":
    ScreenDel = "cls"
    import win32api
    check = win32api.GetConsoleTitle()
    cmd = "where" if platform.system() == "Windows" else "which"
    Nmapwin = subprocess.call([cmd, "nmap.exe"])
    if "Administrator" in check:
        User = "Administrator"
    else:
        User = "Normal User"
else:
    ScreenDel = "clear"
    cmd = "where" if platform.system() == "Windows" else "which"
    Nmaplinux = subprocess.call([cmd, "nmap"])
    if os.geteuid()==0:
        User = "Root User"
    else:
        User = "Normal User"


if Nmapwin == 0:
    NmapOK = "Windows nmap.exe exist!"
elif Nmaplinux == 0:
    NmapOK = "Linux nmap exist!"
else:
    os.system(ScreenDel)
    print("""
    ! No nmap exist! Please install nmap first. Leaving program.... !
    """)
    sys.exit()



try:
    h, w = screen.getmaxyx()
    
    text = ("IPventur Python 1.0v3 by Norman Woeske")
    text2 = datetime.datetime.now()
    datum = datetime.date.today()
    q1 = "Which v4 IP/range (/32 for single IP) would you like to scan? (for exit use \"q\" and ENTER)"
    q2 = "Which nmap scan techniques would you like? (for exit use \"q\" and ENTER)"
    q3 = "Which output file format would you like: 1. Text-Format or 2. Json-Format ?"
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    zeit = text2.strftime("%Y-%m-%d %H:%M:%S")
        
    x = w//2 - len(text)//2
    x2 = w//2 - len(zeit)//2
    x3 = w//2 - len(os_version)//2
    
    y = 2
    
        
    screen.attron(curses.color_pair(1))
    screen.border(0)
    screen.addstr(y+1, x2-44, NmapOK)
    screen.addstr(y, x, text)
    screen.addstr(y+1, x2, zeit)
    screen.addstr(y+2, x3-7, os_version)
    screen.addstr(y+2, x3, f' ({User})')
    screen.attroff(curses.color_pair(1))
    
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
    
    box1 = curses.newwin(3, 30, 7, 2)
    box1.immedok(True)
    box1.box()
    
    while True:
        screen.attron(curses.color_pair(2))        
        screen.addstr(6, 2, q1)
        screen.addstr(8, 4, ip)
        screen.attroff(curses.color_pair(2))
        
        head, sep, tail = ip.partition('/')
        
                    
        char = screen.get_wch()
        if isinstance(char, str) and char.isprintable():
            # add IP address or range to variable ip
            ip += char
            
        elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
            ip = ip[:-1]
        elif technic == "q":
            sys.exit()
        elif char == '\n':
            try:
                ipaddress.ip_network(f'{ip}')
                screen.addstr(8, 33, 'Valid IP adress(es) entered!', curses.A_REVERSE)
                time.sleep(2)
                screen.addstr(8, 33, f'OK, you would like to scan {ip}', curses.A_REVERSE)
                box2 = curses.newwin(3, 4, 20, 38)
                box2.immedok(True)
                box2.box()
            except ValueError:
                screen.addstr(8, 33, 'No valid IP adress(es) entered! Exiting Programm....', curses.A_REVERSE)
                time.sleep(2)
                os.system(f'{ScreenDel}')
                sys.exit()
              
            while True:
                screen.attron(curses.color_pair(2))
                screen.addstr(11, 2, q2)
                screen.attroff(curses.color_pair(2))
                screen.attron(curses.color_pair(1))
                screen.addstr(13, 2, "for non root/admin rights:")
                screen.attroff(curses.color_pair(1))
                screen.addstr(14, 2, " 1. nmap_ping_scan \t2. nmap_list_scan \t3. nmap_dns_brute_script \t4. scan_top_ports")
                screen.attron(curses.color_pair(1))
                screen.addstr(16, 2, "for root/admin rights:")
                screen.attroff(curses.color_pair(1))
                screen.addstr(17, 2, " 5. nmap_detect_firewall \t 6. nmap_os_detection (not yet for Windows)")
                screen.addstr(18, 2, " 7. nmap_portscan_only \t 8. nmap_stealth_scan")
                screen.addstr(19, 2, " 9. nmap_subnet_scan \t\t10. nmap_version_detection")
                screen.attron(curses.color_pair(2))
                screen.addstr(21, 2, "Which number would you like to use? ")
                screen.attroff(curses.color_pair(2))
                screen.addstr(21, 39, technic)
                
                
                if ip_done:
                    screen.addstr(18, 87, 'DONE!', curses.A_REVERSE)
                    output = str(results)
                    box3 = curses.newwin(3, 4, 22, 80)
                    box3.immedok(True)
                    box3.box()
                    while True:
                        screen.attron(curses.color_pair(2))
                        screen.addstr(23, 2, q3)
                        screen.attroff(curses.color_pair(2))
                        screen.addstr(23, 81, outputformat)
                        
                        char = screen.get_wch()
                        if isinstance(char, str) and char.isprintable():
                            outputformat += char
                        elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
                            outputformat = outputformat[:-1]
                        elif char == '\n' or char == curses.KEY_ENTER:
                            if outputformat == "1":
                                screen.addstr(24, 2, f'Output-Format: Text-Format', curses.A_REVERSE)
                                splitoutput = output.replace(",", "\n")
                                sys.stdout = open(f"output-nmap-text-{stechnic}-{head}-{datum}.txt", "w")
                                print(splitoutput)
                                sys.stdout.close()
                                screen.addstr(26, 2, f'Scan completed. Please check out file output-nmap-text-{stechnic}-{head}-{datum}.txt')
                                t = 5
                                while t > 0:
                                    screen.addstr(28, 2, f'{t} Seconds to quit', curses.A_REVERSE)
                                    t -= 1
                                    time.sleep(1)
                                cmd = f'\n*** type >> more output-nmap-text-{stechnic}-{head}-{datum}.txt << to see the results ***\n'
                                sys.exit(cmd)
                            if outputformat == "2":
                                screen.addstr(24, 2, f'Output-Format: Json-Format', curses.A_REVERSE)
                                jsonoutput=(json.dumps(results, indent=4, sort_keys=True))
                                sys.stdout = open(f"output-nmap-json-{stechnic}-{head}-{datum}.txt", "w")
                                print(jsonoutput)
                                sys.stdout.close()
                                screen.addstr(26, 2, f'Scan completed. Please check out file output-nmap-json-{stechnic}-{head}-{datum}.txt')
                                t = 5
                                while t > 0:
                                    screen.addstr(28, 2, f'{t} Seconds to quit', curses.A_REVERSE)
                                    t -= 1
                                    time.sleep(1)
                                cmd2 = f'\n*** type >> more output-nmap-json-{stechnic}-{head}-{datum}.txt << to see the results ***\n'
                                sys.exit(cmd2)
                        elif technic == "q":
                            sys.exit()
                        else:
                            screen.addstr(23, 38, f'Wrong Number {outputformat}')    
                                    
                char = screen.get_wch()
                if isinstance(char, str) and char.isprintable():
                    technic += char
                elif char == curses.KEY_BACKSPACE or char == '\x08' or char == curses.KEY_LEFT:
                    technic = technic[:-1]
                elif char == '\n' or char == curses.KEY_ENTER:
                    if technic == "1":
                        screen.addstr(21, 44, f'Scan-Technic: nmap.nmap_ping_scan({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmapscan.nmap_ping_scan(f'{ip}')
                        stechnic = "ping"
                        ip_done = True
                    elif technic == "2":
                        screen.addstr(21, 44, f'Scan-Technic: nmapscan.nmap_list_scan({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.nmap_list_scan(f'{ip}')
                        stechnis = "list"
                        ip_done = True
                    elif technic == "8":
                        stechnic = "nmap_stealth_scan"
                        screen.addstr(21, 44, f'Scan-Technic: nmap_stealth_scan({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.nmap_stealth_scan(f'{ip}')
                        stechnic = "stealth"
                        ip_done = True
                    elif technic == "10":
                        screen.addstr(21, 44, f'Scan-Technic: nmap_version_detection({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.nmap_version_detection(f'{ip}')
                        stechnis = "version"
                        ip_done = True
                    elif technic == "5":
                        screen.addstr(21, 44, f'Scan-Technic: nmap_detect_firewall({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.nmap_detect_firewall(f'{ip}')
                        stechnic = "fw"
                        ip_done = True
                    elif technic == "3":
                        screen.addstr(21, 44, f'Scan-Technic: nmap_dns_brute_script({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.nmap_dns_brute_script(f'{ip}')
                        stechnic = "dns"
                        ip_done = True
                    elif technic == "4":
                        screen.addstr(21, 44, f'Scan-Technic: scan_top_ports({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.scan_top_ports(f'{ip}')
                        stechnic = "top"
                        ip_done = True
                    elif technic == "6":
                        screen.addstr(21, 44, f'Scan-Technic: nmap_os_detection({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.nmap_os_detection(f'{ip}')
                        stechnic = "os_version"
                        ip_done = True
                    elif technic == "7":
                        screen.addstr(21, 44, f'Scan-Technic: nmap_portscan_only({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmaphost.nmap_portscan_only(f'{ip}')
                        stechnic = "ports"
                        ip_done = True
                    elif technic == "9":
                        screen.addstr(21, 44, f'Scan-Technic: nmap_subnet_scan({ip})', curses.A_REVERSE)
                        screen.addstr(18, 66, 'scanning now .....', curses.A_REVERSE)
                        results = nmap.nmap_subnet_scan(f'{ip}')
                        stechnic = "subnet"
                        ip_done = True
                    elif technic == "q":
                        exit()
                    else:
                        screen.addstr(21, 44, f'Wrong Number {technic}')
                else:
                    screen.addstr(23, 38, f"You pressed wrong key: {char}")
        else:
            screen.addstr(8, 35, f"You pressed wrong key: {char}")
            
 
    screen.getch()

finally:
    curses.endwin()
	