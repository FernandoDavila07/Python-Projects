import requests
from bs4 import BeautifulSoup

class Site:
    def __init__(self, site):
        self.site = site

    def update_news(self): # Método para atualizar as notícias do site
        if self.site.lower() == 'globo': #dicionario de noticias da globo
            url = 'https://www.globo.com/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url,headers = browsers)

            response = page.text
            soup = BeautifulSoup(response, 'html.parser')

            noticias = soup.find_all('a')

            tg_class1 = 'post__title'
            tg_class2 = 'post-multicontent__link--title__text'


            news_dict_globo = {}
            for noticia in noticias:
                if noticia.h2 != None:
                    if tg_class1 in noticia.h2.get('class') or tg_class2 in noticia.h2.get('class'): 
                        news_dict_globo[noticia.h2.text] = noticia.get('href')
            self.news = news_dict_globo



        if self.site.lower() == 'veja': #dicionario de noticias da veja
            url = 'https://veja.abril.com.br/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url,headers = browsers)

            response = page.text
            soup = BeautifulSoup(response, 'html.parser')



            noticias = soup.find_all('a')
            tg_class1 = 'title'
            tg_class2 = 'related-article'
            news_dict_veja = {}


            for noticia in noticias:
                if (noticia.get('class') != None) and (tg_class2 in noticia.get('class')):
                    news_dict_veja[noticia.text] = noticia.get('href')
                if (noticia.h2 != None) and (noticia.h2.get('class') != None) and (tg_class1 in noticia.h2.get('class')):
                    news_dict_veja[noticia.h2.text] = noticia.get('href')
                if (noticia.h3 != None) and (noticia.h3.get('class') != None) and (tg_class1 in noticia.h3.get('class')):
                    news_dict_veja[noticia.h3.text] = noticia.get('href')
                if (noticia.h4 != None) and (noticia.h4.get('class') != None) and (tg_class1 in noticia.h4.get('class')):
                    news_dict_veja[noticia.h4.text] = noticia.get('href')
            self.news = news_dict_veja 
        
        
        if self.site.lower() == 'cnn': #dicionario de noticias da cnn
            url = 'https://www.cnnbrasil.com.br/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url,headers = browsers)

            response = page.text
            soup = BeautifulSoup(response, 'html.parser')

            noticias = soup.find_all('a')

            tg_class1 = 'text-base font-bold flex w-fit'
            news_dict_cnn = {}

            for noticia in noticias:
                if (noticia.get('class') != None):
                    news_dict_cnn[noticia.text] = noticia.get('href')
                if (noticia.h2 != None) and (noticia.h2.get('class') != None) and (tg_class1 in noticia.h2.get('class')):
                    news_dict_cnn[noticia.h2.text] = noticia.get('href')
                if (noticia.h3 != None) and (noticia.h3.get('class') != None) and (tg_class1 in noticia.h3.get('class')):
                    news_dict_cnn[noticia.h3.text] = noticia.get('href')
                if (noticia.h4 != None) and (noticia.h4.get('class') != None) and (tg_class1 in noticia.h4.get('class')):
                    news_dict_cnn[noticia.h4.text] = noticia.get('href')
            self.news = news_dict_cnn


        if self.site.lower() == 'bbc': #dicionario de noticias da bbc
            url = 'https://www.bbc.com/portuguese'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url,headers = browsers)

            response = page.text
            soup = BeautifulSoup(response, 'html.parser')

            noticias = soup.find_all('a')

            tg_class1 = 'bbc-14nw343 e47bds20'
            tg_class2 = 'bbc-pam0zn e47bds20' 
            tg_class3 = 'bbc-1slyjq2 e47bds20'
            tg_class4 = 'bbc-14zb6im'
            news_dict_bbc = {}

            for noticia in noticias:
                if (noticia.get('class') != None):
                    news_dict_bbc[noticia.text] = noticia.get('href')
                if(noticia.h2 != None) and (noticia.h2.get('class') != None) and (tg_class1 in noticia.h2.get('class') or tg_class2 in noticia.h2.get('class') or tg_class3 in noticia.h2.get('class') or tg_class4 in noticia.h2.get('class')):
                    news_dict_bbc[noticia.h2.text] = noticia.get('href')
                if(noticia.h3 != None) and (noticia.h3.get('class') != None) and (tg_class1 in noticia.h3.get('class') or tg_class2 in noticia.h3.get('class') or tg_class3 in noticia.h3.get('class') or tg_class4 in noticia.h3.get('class')):
                    news_dict_bbc[noticia.h3.text] = noticia.get('href')
                if(noticia.h4 != None) and (noticia.h3.get('class') != None) and (tg_class1 in noticia.h4.get('class') or tg_class2 in noticia.h4.get('class') or tg_class3 in noticia.h4.get('class') or tg_class4 in noticia.h4.get('class')):
                    news_dict_bbc[noticia.h4.text] = noticia.get('href')
            self.news = news_dict_bbc

