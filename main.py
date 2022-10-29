import tkinter
import requests
from bs4 import BeautifulSoup
import urllib.parse
from tkinter import scrolledtext
import pprint


def search(lang,param):
    param = urllib.parse.quote(param) #urlエンコード

    if lang == '英語':
        weblio_en_url = 'https://ejje.weblio.jp/content/'+param
        html_txt = requests.get(weblio_en_url).text
        soup = BeautifulSoup(html_txt,'html.parser')

        definition_elements = soup.find_all('p',class_="lvlB")
        result=[]
        for el in definition_elements:
            result.append(el.text)
        integrated = ''#絶対簡略化できると思う、改善したい
        num = 1
        for i in result:
            if len(i)<=27:
                integrated += '【' + str(num) + '】' + i + '\n'
            else:
                integrated += '【' + str(num) + '】' + i[:27] + '\n' + i[27:] + '\n'
            num += 1

    if lang == 'ドイツ語':
        kotobank_de_url = 'https://kotobank.jp/dejaword/'+param
        html_txt_de = requests.get(kotobank_de_url).text
        soup = BeautifulSoup(html_txt_de,'html.parser')
        integrated = ''

        try:
            redirect_url = soup.find('p',{'data-orgtag':'meaning'}).find('a')['href']
            original_word = soup.find('p',{'data-orgtag':'meaning'}).text
            integrated += original_word + '\n\n'
            html_txt_de = requests.get('https://kotobank.jp'+redirect_url).text
            soup = BeautifulSoup(html_txt_de,'html.parser')
        except TypeError:
            pass

        definition_elements = soup.find_all('p',{'data-orgtag':'meaning'})
        result=[]
        for el in definition_elements:
            result.append(el.text)

        for i in result:
            if len(i)<=27:
                integrated += i + '\n'
            else:
                integrated += i[:27] + '\n'

    print(integrated)
    return integrated


class Application(tkinter.Frame):
    def __init__(self,root=None):
        super().__init__(root,width=900,height=500,borderwidth=1,relief='groove')
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        default=('Helvetica',18)

        self.text_box = tkinter.Entry(self,font=default,width=30)
        self.text_box.pack(fill='x',padx=100)

        items = ['ドイツ語','英語']        
        self.sp = tkinter.Spinbox(self,font=default,state='readonly',values=items)
        self.sp.pack()

        button = tkinter.Button(self,text='検索',font=default,command=self.submit)
        button.pack(fill='x',padx=130)
        
        self.view = scrolledtext.ScrolledText(self,font=default)
        self.view.insert('1.0','単語を入力してボタンを押すと、ここに検索結果が表示されます。')
        self.view.pack()
        
        #エンターで検索
        self.text_box.bind('<Return>',self.submit)
        #Entryにフォーカス
        self.text_box.focus_set()

    def submit(self,event):
        lang = self.sp.get()
        text = self.text_box.get()

        textv = search(lang,text)
        self.view.delete(1.0,tkinter.END)
        self.view.insert('1.0',textv)

root = tkinter.Tk()
root.title('調べてえら～い！')
root.geometry('500x300')
app = Application(root=root)
app.mainloop()