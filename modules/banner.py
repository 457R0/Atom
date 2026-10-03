"""
COPYRIGHT DISCLAIMER

Script : Atom - All in One Android Hacking ADB Toolkit

Original work Copyright (C) 2026  Azeem Idrisi (github.com/AzeemIdrisi)
Fork Copyright (C) 2026  TezukaLabs

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Forked from PhoneSploit Pro by Azeem Idrisi (github.com/AzeemIdrisi).
Fork maintained by TezukaLabs.

For any queries, Contact: github.com/TezukaLabs
"""

version = "v2.3"

instruction = """
This attack will launch Metasploit-Framework    (msfconsole)

Use 'Ctrl + C' to stop at any point

1. Wait until you see:

    [green]meterpreter >      [/green]

2. Then use 'help' command to see all meterpreter commands:

    [green]meterpreter > [yellow]help       [/yellow][/green]

3. To exit meterpreter enter 'exit' or To exit Metasploit enter 'exit -y':

    [green]meterpreter > [yellow]exit       [/yellow][/green]

    [green]msf6 > [yellow]exit -y       [/yellow][/green]

[bold red]\\[Atom][/bold red]   Press 'Enter' to continue attack / '0' to Go Back to Main Menu
    """

# banner2 — block-pipe style (figlet block font)
banner2 = """
                                            
  _|_|    _|_|_|_|_|    _|_|    _|      _|  
_|    _|      _|      _|    _|  _|_|  _|_|  
_|_|_|_|      _|      _|    _|  _|  _|  _|  
_|    _|      _|      _|    _|  _|      _|  
_|    _|      _|        _|_|    _|      _|  
                                            


            [bold red]{version}[/bold red]                    [bold white]By TezukaLabs[/bold white]
""".format(version=version)

# banner3 — bubble style
banner3 = """
  _   _   _   _  
 / \\ / \\ / \\ / \\ 
( A | T | O | M )
 \\_/ \\_/ \\_/ \\_/ 


            [bold red]{version}[/bold red]             [bold white]By TezukaLabs[/bold white]
""".format(version=version)

# banner4 — standard style
banner4 = """
    _  _____ ___  __  __ 
   / \\|_   _/ _ \\|  \\/  |
  / _ \\ | || | | | |\\/| |
 / ___ \\| || |_| | |  | |
/_/   \\_\\_| \\___/|_|  |_|
                         


        [bold red]{version}[/bold red]                             [bold white]By TezukaLabs[/bold white]
""".format(version=version)

# banner5 — slant style
banner5 = """
    ___  __________  __  ___
   /   |/_  __/ __ \\/  |/  /
  / /| | / / / / / / /|_/ / 
 / ___ |/ / / /_/ / /  / /  
/_/  |_/_/  \\____/_/  /_/   
                            


        [bold red]{version}[/bold red]        [bold white]By TezukaLabs[/bold white]
""".format(version=version)

# banner6 — lean style
banner6 = """
                                                 
      _/_/    _/_/_/_/_/    _/_/    _/      _/   
   _/    _/      _/      _/    _/  _/_/  _/_/    
  _/_/_/_/      _/      _/    _/  _/  _/  _/     
 _/    _/      _/      _/    _/  _/      _/      
_/    _/      _/        _/_/    _/      _/       
                                                 
                                                 

           [bold red]{version}[/bold red]               [bold white]By TezukaLabs[/bold white]
""".format(version=version)

# banner10 — script / calligraphic style
banner10 = """
  ___,                     
 /   |                     
|    | _|_  __   _  _  _   
|    |  |  /  \\_/ |/ |/ |  
 \\__/\\_/|_/\\__/   |  |  |_/
                           
                           

            [bold red]{version}[/bold red]                                [bold white]By TezukaLabs[/bold white]
""".format(version=version)

# banner11 — digital / box style
banner11 = """
+-+-+-+-+
|A|T|O|M|
+-+-+-+-+


            [bold red]{version}[/bold red]                            [bold white]By TezukaLabs[/bold white]
""".format(version=version)

# banner12 — shadow style
banner12 = """
    \\ __ __| _ \\   \\  | 
   _ \\   |  |   | |\\/ | 
  ___ \\  |  |   | |   | 
_/    _\\_| \\___/ _|  _| 
                        


            [bold red]{version}[/bold red]                            [bold white]By TezukaLabs[/bold white]
""".format(version=version)

banner_list = [
    banner2,
    banner3,
    banner4,
    banner5,
    banner6,
    banner10,
    banner11,
    banner12,
]

instructions_banner = """[bold cyan]
        ____           __                  __  _
       /  _/___  _____/ /________  _______/ /(_)___  ____  _____
       / // __ \\/ ___/ __/ ___/ / / / ___/ __/ / __ \\/ __ \\/ ___/
     _/ // / / (__  ) /_/ /  / /_/ / /__/ /_/ / /_/ / / / (__  )
    /___/_/ /_/____/\\__/_/   \\__,_/\\___/\\__/_/\\____/_/ /_/____/
[/bold cyan]"""

hacking_banner = """[bold green]
    █░█ ▄▀█ █▀▀ █▄▀ █ █▄░█ █▀▀ ░ ░ ░
    █▀█ █▀█ █▄▄ █░█ █ █░▀█ █▄█ ▄ ▄ ▄
[/bold green]"""
