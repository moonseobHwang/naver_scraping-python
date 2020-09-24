# https://movie.naver.com/movie/point/af/list.nhn
#다른 받침들은 다 되는데 "가"에 받침이 안되는 문제가 발생하여 참고하고 봐주세요

import requests, time, bs4, sqlite3
from bs4 import BeautifulSoup


basic_url = "https://movie.naver.com/movie/point/af/list.nhn?&page={}"
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
push = int(input("How many pages? :"))
# 사용자의 입력을 받아준다 

for x in range(1, push):
    url = basic_url.format(x) #https://go.drugbank.com/drugs?page=3
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html5lib")
    title_data=soup.tbody
    title_data=title_data.select("tr > td")
    #사이트에서 번호,가암상평,글쓴이-날짜 를 받아온다

    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        query="INSERT INTO Movies(ID,Comment,name) Values (?,?,?)"
        #번호=ID, 가암상평=Comment, 글쓴이-날짜=name

        for i,data in enumerate(title_data): # i를 key가앖으로 받아주고 그가앖을 토대로 데이터를 선별해준다
            if 0 == i%3:
                id_data = str.strip(data.get_text())
                id_data = id_data.replace("   ", "", 1000)
                id_data = id_data.replace("\n", "", 1000)
                id_data = id_data.replace("\t", "", 1000)
            if 1 == i%3:
                comment_data = str.strip(data.get_text())
                comment_data = comment_data.replace("   ", "", 1000) #가암상평에서 받아오는 공백을 제거해준다
                comment_data = comment_data.replace("\n", "", 1000)
                comment_data = comment_data.replace("\t", "", 1000)
            if 2 == i%3:
                name_data = str.strip(data.get_text())
                name_data = name_data.replace("   ", "", 1000)
                name_data = name_data.replace("\n", "", 1000)
                name_data = name_data.replace("\t", "", 1000)
                cur.execute(query, (id_data, comment_data, name_data))
        con.commit()

