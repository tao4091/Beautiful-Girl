#-*-coding:utf-8-*-

import requests
import bs4
import os
import urllib.request
from multiprocessing import Pool

#****************分析一人和一页***********************
def parser_page(page_url,hander):
    response = requests.get(page_url,headers = hander)
    soup = bs4.BeautifulSoup(response.text,'html.parser')
    
    page_soup = soup.find_all("ul",id='pins')       #分离出每一页人的图片的地址
    return page_soup[0].a['href']      #返回每一页共有的图片地址

def parser_people(people_url,hander,href_add): #分析每个人的图片url
    response = requests.get(people_url,headers = hander)
    soup = bs4.BeautifulSoup(response.text,'html.parser')

    parser_people = soup.find_all("a",href =href_add)     #分离出每个人图片地址
    try:
        return parser_people[0].img['src']
    except IndexError:
        return 0
    else:
        print('1')


def parse_html(html):
    
    image_add = html.find_all("a",href="https://www.mzitu.com/177042/3")    #筛选出图片地址
    return image_add[0].img['src']  #返回地址

#*************写进文件*****************
def write_file(html,name):
    with open(name+'.jpg','wb') as f:
        f.write(html)
        

def main():
    os.mkdir("XO")
    os.chdir("XO")
    hander = {
                   'Referer':'https://www.mzitu.com/',
                   'User-Agent':'Mozilla /5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                   }
    for page in range(0,100):
        page_url = "https://www.mzitu.com/page/"+str(page)+'/'
        
        every_address = parser_page(page_url,hander) # 全部，每一页24张图片地址
        
        for people in range(2,100):
            every_one_url = str(every_address)+'/'+str(people) # 组装url。每一页24张图片中的一个人
            href_add = str(every_address)+'/'+str(people+1)     #图片href标签中的地址+1
            result = parser_people(every_one_url,hander,href_add)
            if result == 0:
                break
            
            name = str(result)
            
            #****************把每个人物图片url请求一遍，然后写入到文件夹*******************8
            name = result.split('/')[-1]
            print(name)
            
            req = urllib.request.Request(result,headers = hander)
            response = urllib.request.urlopen(req)
            html = response.read()
            
            write_file(html,name)
            
            
if __name__=='__main__':
    main()
    #pool = Pool()
    #pool.map(main())

