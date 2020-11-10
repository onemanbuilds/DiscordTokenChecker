import requests
from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from random import choice
from threading import Thread,Lock,active_count
from sys import stdout
from time import sleep

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {}
        if self.proxy_type == 1:
            proxies = {
                "http":"http://{0}".format(choice(proxies_file)),
                "https":"https://{0}".format(choice(proxies_file))
            }
        elif self.proxy_type == 2:
            proxies = {
                "http":"socks4://{0}".format(choice(proxies_file)),
                "https":"socks4://{0}".format(choice(proxies_file))
            }
        else:
            proxies = {
                "http":"socks5://{0}".format(choice(proxies_file)),
                "https":"socks5://{0}".format(choice(proxies_file))
            }
        return proxies

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'One Man Builds Discord Token Checker Tool ^| HITS: {self.hits} ^| BADS: {self.bads} ^| RETRIES: {self.retries} ^| THREADS: {active_count()-1}')
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.clear()
        self.SetTitle('One Man Builds Discord Token Checker Tool')
        self.title = Style.BRIGHT+Fore.RED+"""
                              ╔═══════════════════════════════════════════════════════════════╗
                                 ╔╦╗╦╔═╗╔═╗╔═╗╦═╗╔╦╗  ╔╦╗╔═╗╦╔═╔═╗╔╗╔  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
                                  ║║║╚═╗║  ║ ║╠╦╝ ║║   ║ ║ ║╠╩╗║╣ ║║║  ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
                                 ═╩╝╩╚═╝╚═╝╚═╝╩╚══╩╝   ╩ ╚═╝╩ ╩╚═╝╝╚╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═  
                              ╚═══════════════════════════════════════════════════════════════╝                                                                                    
                                                                                    
        """
        print(self.title)
        self.hits = 0
        self.bads = 0
        self.retries = 0
        self.lock = Lock()

        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        
        if self.use_proxy == 1:
            self.proxy_type = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Https ['+Fore.RED+'2'+Fore.CYAN+']Socks4 ['+Fore.RED+'3'+Fore.CYAN+']Socks5: '))
        
        self.threads_num = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))

        print('')


    def TokenCheck(self,token):
        try:
            
            headers = {
                'User-Agent': self.GetRandomUserAgent(),
                'Authorization':token
            }

            response = ''

            link = 'https://discord.com/api/v8/users/@me'

            if self.use_proxy == 1:
                response = requests.get(link,headers=headers,proxies=self.GetRandomProxy())
            else:
                response = requests.get(link,headers=headers)

            if 'username' in response.text:
                username = response.json()['username']
                self.PrintText(Fore.CYAN,Fore.RED,'VALID',f'{token} -> {username}')
                with open('valids.txt','a',encoding='utf8') as f:
                    f.write(token+'\n')
                self.hits += 1
            elif '401: Unauthorized' in response.text:
                self.PrintText(Fore.CYAN,Fore.RED,'BAD',token)
                with open('bads.txt','a',encoding='utf8') as f:
                    f.write(token+'\n')
                self.bads += 1
            else:
                self.retries += 1
                self.TokenCheck(token)
        except:
            self.retries += 1
            self.TokenCheck(token)

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        tokens = self.ReadFile('tokens.txt','r')
        for token in tokens:
            Run = True
            while Run:
                if active_count()<=self.threads_num:
                    Thread(target=self.TokenCheck,args=(token,)).start()
                    Run = False

if __name__ == '__main__':
    main = Main()
    main.Start()