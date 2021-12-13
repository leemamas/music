import requests as rq
from jsonpath import jsonpath
from prettytable import PrettyTable
import cmd
import os


class Console(cmd.Cmd):
    intro = 'Music World!'
    prompt = 'music>'

    def do_search(self, arg):

        key = input('song:')
        tb, self.playlist = display(craw_music(key))
        print(tb)

    def do_love(self, arg):
        print('my love!')

    def do_play(self, arg):
        key = input('Enter the ID to play:')
        id = int(key) - 1
        try:
            cmd = 'mpg123\mpg123.exe -q ' + self.playlist[id] + ''
            print('playing....')
            try:
                os.system(cmd)
                print('finish...')
            except:
                print('oh my god!')
        except:
            print('no playlist!')

    def do_exit(self, arg):
        print('Bye')



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
    info = res.json()
    return info


def display(info):
    tb = PrettyTable()
    tb.field_names = ['序号', '歌曲', '歌手', 'link', 'url']
    lt = []
    for i in range(0, 10):
        try:
            title = jsonpath(info, '$..title')[i]
            author = jsonpath(info, '$..author')[i]
            link = jsonpath(info, '$..link')[i]
            url1 = jsonpath(info, '$..url')[i]
            lt.append(url1)
            pic = jsonpath(info, '$..pic')[i]
            tb.add_row([i + 1, title, author, link, url1])
        except:
            pass
    return tb, lt


if __name__ == '__main__':

    try:
        c = Console()
        c.cmdloop()
    except:
        exit()
