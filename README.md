# ncurses-IPventur.py
IPventur nmap frontend for Python3 and curses with nmap3 module

This is v1.5 of ncurses-IPventur.py

Requirements:

Python 3.8 or higher

-----------------------------------------------------------
python3-nmap:

$ git clone https://github.com/nmmapper/python3-nmap.git

cd python3-nmap

chmod a+x build.sh

./build.sh

$ pip3 install -r requirements.txt && pip3 install -r requirements-dev.txt

-----------------------------------------------------------

additional requirements for ncurses-IPventur.py:

for Windows:

"pip3 install -r requirements-win.txt"


for Linux:

"pip3 install -r requirements-linux.txt"


nmap:

Linux:

"sudo apt install nmap"
or:
"sudo yum install nmap"

Windows:
https://nmap.org/download.html


start program (recommended as root) with: "python ncurses-IPventur.py"

Note:
goal for this program was to write an easy to use frontend for nmap. Any feedback welcome.

Update betav5 version:

- added IP format check
- added if nmap program exist
- restart program when IP address is wrong
- redesign windows design
- restructure python code

Still missing:
- ask after a complete scan for a new scan or leaving... (will be soon in v6)

Update betav6 version:

- added terminal window size check of 34 x 111, otherwise program will not starts
- added restart menu after a completed scan
- some minor design changes

Update betav7 version:

- resolved json format saving bug
- added actual screen size, to windows size error message
- minor design change

Update betav8 version:

- added notes that some nmap scan options are not valid for Windows OS yet
- added some new menu points
- changed some minor style issues

Note: new features will be added son! stay tune.

Update v1.1 version:

added final version 1.1:

- added screen size check and display actual screen size
- re-org menu list and add/removed some scan techniqs
- re-start within the menu window, and not the whole prog
- some minor style changes

Update v1.2 version:

- changed some scan techniques (udp scan has still an issue on Windows 10 machine, python3-nmap author is informed)
- added result output when you leave the program
- some minor style changes

Update v1.3 version:

- output files have new naming convention and correct file extension .json or .txt
- changed scan menu, because udp scan needs admin/root rights, also contacted the python3-nmap author to resolve the udp scan under Windows 10
- some minor style changes

Update 1.4 version:

- add time to the outputfile and change output file naming convetion
- change displaying date format to day-month-year

Update 1.5 version

- moved scan technic udp scan to the admin/root area
- input text can now delete with backspace
- added estimate scanning times, because of nmap the scan process can be very long (around 30 minutes) depends of the nmap technic like udp_scan and the size of the scanned network
- some minor cosmetic changes
