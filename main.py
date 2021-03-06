import requests as rq
from jsonpath import jsonpath
from prettytable import PrettyTable
import cmd
import os
import time
import pygame

class Console(cmd.Cmd):
    intro = '''
            ⭐Music World⭐
    ---------------------------- 
    相关命令列表       
    search           搜索音乐
    love             喜爱音乐
    exit             退出'''
    prompt = 'music>'

    def do_s(self,arg):
        self.do_search(arg)

    def do_search(self, arg):
        print('Search the music you want')
        key = input('song:')
        json = craw_music(key)
        playlist = info(json)
        # print(playlist)
        if playlist:
            console(playlist)

            while 1:
                key = input('choice (1/play 2/play with Lyric 3/collect 4/quit) :')

                def play():
                    self.play(playlist)

                def playwithlyric():
                    self.playwithlyric(playlist)

                def collect():
                    try:
                        key = input('Enter the ID to collect:')
                        id = int(key) - 1
                        title = playlist[id]['title']
                        author = playlist[id]['author']
                        url = playlist[id]['url']
                        f = open("love.txt", 'a')
                        f.write(title + '|' + author + '|' + url + '\n')
                        print('Collect song【' + title + '】 success!')
                        f.close()
                    except:
                        pass

                def quit():
                    print('quit....')
                    pass

                switch = {
                    '1': play,
                    '2': playwithlyric,
                    '3': collect,
                    '4': quit
                }
                try:
                    switch[key]()
                    break
                except KeyError as e:
                    print('Error instruction!')
        else:
            print('No relevant information was found!')

    def do_love(self, arg):
        print('My favorite playlist')
        playlist = []
        try:
            f = open("love.txt", "r")
            for line in f.readlines():
                line = line.strip()
                value = line.split('|')
                key = ['title', 'author', 'url']
                playlist.append(dict(zip(key, value)))
            if playlist:
                console(playlist)

                while 1:
                    key = input('choice (1/single play 2/all play 3/edit list 4/quit) :')

                    def singlePlay():
                        self.play(playlist)

                    def allPlay():
                        print('developing...')

                    def edit():
                        delkey=input('Want to delete the song ID:')
                        try:
                            delid = int(delkey)
                        except:
                            print('please id number')

                        with open("love.txt", "r") as f1:
                            lines = f1.readlines()

                        with open("love.txt", "w") as f2_w:
                            count = 1
                            for line in lines:

                                if count != delid:
                                    f2_w.write(line)
                                count += 1
                        f1.close()
                        f2_w.close()
                    def quit():
                        print('quit....')
                        pass

                    switch = {
                        '1': singlePlay,
                        '2':allPlay,
                        '3':edit,
                        '4': quit
                    }
                    try:
                        switch[key]()
                        break
                    except KeyError as e:
                        print('Error instruction!')
            else:
                print('No playlist!')

        except:
            print('No playlist!')

    def play(self, playlist):
        key = input('Enter the ID to play:')
        id = int(key) - 1
        try:
            cmd = 'mpg123\mpg123.exe -q ' + playlist[id]['url'] + ''
            try:
                os.system(cmd)
                print('finish...')
            except:
                print('oh my god!')
        except:
            print('no playlist!')


    def playwithlyric(self,playlist):
        key = input('Enter the ID to play:')
        id = int(key) - 1
        try:
            downloadMusic(playlist[id]['url'])
            pygame.mixer.init()
            track = pygame.mixer.music.load('1.mp3')
            pygame.mixer.music.play()
            print('playing....【' + playlist[id]['title'] + '】')

            with open("lrc.lrc", "w", encoding='utf-8') as f:
                f.write(playlist[id]['lrc'])
            self.printLyric(playlist[id]['lrc'])
            try:
                print('finish...')
            except:
                print('oh my god!')
        except:
            print('no playlist!')



    def printLyric(self,lrc):
        # print(lrc)
        lyricList = []
        timeTable = []
        with open('lrc.lrc', 'r', encoding='utf-8') as fread:
            for line in fread:
                str = line.split(']')
                mm = int(str[0][1:3])
                ss = int(str[0][4:6])
                SS = int(str[0][7:9])
                t = mm * 60 + ss + SS * 0.01
                timeTable.append(t)
                lyricList.append(str[1])
        temp=0
        count=0
        for t in timeTable:
            time.sleep(t - temp)
            temp = t
            print(lyricList[count],end='')
            count+=1

    def do_exit(self, arg):
        print('Bye')
        exit()


def downloadMusic(url):
    try:
        res = rq.get(url,stream=True)
        print('Download Music ing。。。。')
        with open('1.mp3', 'wb') as fd:
            for chunk in res.iter_content():
                fd.write(chunk)
        print(' Success！')
    except:
        print("程序错误")

def craw_music(title, type='netease', page=1):
    url = 'http://www.xmsj.org/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.110.430.128 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    proxies = {
        'http': 'http://88.88.88.88:8888',
    }
    params = {'input': title, 'filter': 'name', 'type': type, 'page': page}
    res = rq.post(url, params, headers=headers)
    json = res.json()
    return json


def info(json):
    playlist = []
    for i in range(0, 10):
        try:
            title = jsonpath(json, '$..title')[i]
            author = jsonpath(json, '$..author')[i]
            link = jsonpath(json, '$..link')[i]
            url1 = jsonpath(json, '$..url')[i]
            lrc = jsonpath(json, '$..lrc')[i]
            playlist.append({'title': title, 'author': author, 'url': url1,'lrc':lrc})
            pic = jsonpath(json, '$..pic')[i]

        except:
            pass
    return playlist


def console(playlist):
    tb = PrettyTable()
    tb.field_names = ['序号', '歌曲', '歌手', 'url']
    for i in range(0, len(playlist)):
        tb.add_row([i + 1, playlist[i]['title'], playlist[i]['author'], playlist[i]['url']])
    print(tb)


if __name__ == '__main__':

    try:
        c = Console()
        c.cmdloop()
    except:
        exit()
