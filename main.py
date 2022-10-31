import tkinter
import requests
from bs4 import BeautifulSoup
import urllib.parse
from tkinter import scrolledtext

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

        try:#リダイレクトする場合
            redirect_url = soup.find('p',{'data-orgtag':'meaning'}).find('a')['href']
            original_word = soup.find('p',{'data-orgtag':'meaning'}).text
            integrated += original_word + '\n\n'
            html_txt_de = requests.get('https://kotobank.jp'+redirect_url).text
            soup = BeautifulSoup(html_txt_de,'html.parser')
        except TypeError:
            pass
        
        #結果
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
    #apperance
    default = ('游明朝',18)
    color1 = "beige"
    color2 = "white"
    accentcolor = "pink"

    def __init__(self,master=None):
        super().__init__(master,borderwidth=1,bg=self.color1,relief='flat')
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        #検索バー
        self.searchbar = tkinter.Frame(self,relief=tkinter.GROOVE)
        self.text_box = tkinter.Entry(self.searchbar,font=self.default,width=30)
        self.text_box.bind('<Return>',self.submit)
        self.text_box.focus_set()
        self.button = tkinter.Button(self.searchbar,text='検索(E)',font=self.default,command=self.submit,width=10,bg=self.accentcolor)

        #言語選択
        items = ['ドイツ語','英語']        
        self.selection = tkinter.Spinbox(self,font=self.default,state='readonly',values=items)

        #検索結果領域
        self.view = scrolledtext.ScrolledText(self,bg=self.color1,font=self.default,bd=0)
        self.view.insert('1.0','単語を入力してボタンを押すと、ここに検索結果が表示されます。')
        self.view.config(state=tkinter.DISABLED)

        #配置
        self.searchbar.pack()
        self.selection.pack()
        self.view.pack()
        self.text_box.pack(side=tkinter.LEFT)
        self.button.pack(side=tkinter.LEFT)

        

    def submit(self,event):
        lang = self.selection.get()
        text = self.text_box.get()

        textv = search(lang,text)
        self.view.config(state=tkinter.NORMAL)
        self.view.delete(1.0,tkinter.END)
        self.view.insert('1.0',textv)
        self.view.config(state=tkinter.DISABLED)

root = tkinter.Tk()
root.title('DICTIONARIUM')
root.geometry('500x300')
app = Application(master=root)
app.mainloop()