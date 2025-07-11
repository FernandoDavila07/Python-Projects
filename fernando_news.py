from scraping_sites.site import *
import os
from threading import Thread
import time
from datetime import datetime
import sys
import pickle
import webbrowser
from math import ceil
from pytimedinput import timedInput

class fernandoNews:
    def __init__(self):
        self.dict_site = {}
        self.all_sites = ['globo', 'veja', 'cnn', 'bbc']

        self.screen = 0
        
        self.kill = False
        self.page = 1
        self.message = ''

        self.news = self._read_file('news') if 'news' in os.listdir() else []
        self._update_file(self.news, 'news')
        self.sites = self._read_file('sites') if 'sites' in os.listdir() else []
        self._update_file(self.sites, 'sites')

        for site in self.all_sites:
            self.dict_site[site] = Site(site)
        
        self.news_thread = Thread(target=self.update_news)
        self.news_thread.setDaemon(True)
        self.news_thread.start()

    def _update_file(self, lista, mode='news'):
        with open(mode, 'wb') as fp:
            pickle.dump(lista,fp)

    def _read_file(self, mode='news'):
        with open(mode,'rb') as fp:
            n_list = pickle.load(fp)
            return n_list

    def _receive_command(self, valid_commands, timeout=30):
        command, timed = timedInput('>>', timeout)
        while command.lower() not in valid_commands and not timed:
            print("Comando inválido. Digite novamente\n")
            command, timed = timedInput('>>', timeout)
        command = 0 if command == '' else command
        return command

    def main_loop(self):
        while True:
            if self.message:
                print(self.message)
                time.sleep(2)
                self.message = ''

            os.system('cls' if os.name == 'nt' else 'clear')
                
            match self.screen:
                case 0:
                    print('Seja bem vindo ao Fernando News!!')
                    print('Selecione algum item do menu')
                    print('')
                    print('1. Ultimas Noticias\n2. Adicionar site\n3. Remover sites\n4.Fechar Programa')
                    self.screen = int(self._receive_command(['1', '2', '3','4'], 5))
                    print(self.screen , type(self.screen))

                case 1:
                    self.display_news()
                    command = self._receive_command(['e', 'q', 'r', '0'], 500)
                    match command:
                        case 'e':
                            if self.page < self.max_page:
                                self.page += 1
                        
                        case 'q': 
                            if self.page > 1:
                                self.page -= 1
                            else:
                                self.message = 'Você já está na primeira página!'
                                
                        
                        case '0':
                            self.screen = 0
                            continue

                        case 'r':
                            link = int(input('>> Insira o numero da materia que deseja abrir: '))
                            if link < 1 or link > len(self.filtered_news):
                                self.message = 'A matéria não existe'
                                
                            else:
                                webbrowser.open(self.filtered_news[link-1]['link'])
                                # if platform == "linux" or platform == "linux2": # Linux
                                #     chrome_path = '/usr/bin/google-chrome %s'
                                # elif platform == "darwin": # OS X
                                #     chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
                                # elif platform == "win32": # Windows
                                #     chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                                # webbrowser.get(f"\"{chrome_path}\" %s").open(link)


                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Digite o numero correspondente do site que deseja adicionar para a lista de sites ativos.\nOu pressione 0 e retorne a tela de inicio')
                    print('\tSITES ATIVOS ---------------\n')
                    for i in self.sites:
                        print('\t', i)

                    print('\tSITES INATIVOS -------------\n')
                    offline_sites = [i for i in self.all_sites if i not in self.sites]
                    for i in range(len(offline_sites)):
                        print(f'\t{i+1}. {offline_sites[i]}')
                    
                    site = int(self._receive_command([str(i) for i in range(len(offline_sites)+1)], 50))
                    if site ==0:
                        self.screen = 0
                        continue
                    self.sites += [offline_sites[site-1]]
                    self._update_file(self.sites, 'sites')

                case 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Digite o numero do site que nao queira ver as noticias \nOu pressione o 0 para retornar a tela de inicio')

                    for i in range(len(self.sites)):
                        print(f'\t{i+1}. {self.sites[i]}')
                    site = int(self._receive_command([str(i) for i in range(len(self.sites)+1)], 50))
                    if site ==0:
                        self.screen = 0
                        continue
                    del self.sites[site-1]
                    self._update_file(self.sites,'sites')
                
                case 4:
                    self.kill = True
                    sys.exit()


    def display_news(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Ultima Atualização: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")

        self.filtered_news = [i for i in self.news if i['fonte'] in self.sites]
        self.max_page = ceil(len(self.filtered_news) / 20)



        if self.page > self.max_page: 
            self.page = 1

        
        const = (self.page - 1) * 10

        for i, article in enumerate(self.filtered_news[const:const+10]):
            print(f'{const+i+1}. {article['data'].strftime('%H:%M:%S %d/%m/%Y')} - {article['fonte'].upper()} - {article['materia']}')
        print(f'Page {self.page}/{self.max_page}')

        
        if not self.filtered_news:
            print('\n\nVocê não selecionou os motores de busca!\n\n')


        print('-------------------------------------------------------\n')
        print('Comandos: ')
        print('E - Proxima Pagina | Q - Pagina Anterior | R - Abrir noticia no navegador | 0 - Voltar')


    def update_news(self):
        while not self.kill:
            
            for site in self.all_sites:
                self.dict_site[site].update_news()

                for key, value in self.dict_site[site].news.items():
                    dict_aux = {}
                    dict_aux['data'] = datetime.now()
                    dict_aux['fonte'] = site  
                    dict_aux['materia'] = key
                    dict_aux['link'] = value

                    if len(self.news) == 0:
                        self.news.insert(0, dict_aux)
                        continue
                    
                    add_news = True
                    for news in self.news:
                        if dict_aux["materia"] == news["materia"] and dict_aux["fonte"] == news["fonte"]:
                            add_news = False
                            break

                    if add_news:
                        self.news.insert(0, dict_aux)
            self.news = sorted(self.news, key=lambda d: d['data'], reverse=True)
            self._update_file(self.news, 'news')
            time.sleep(10)
        



self = fernandoNews()
self.main_loop()