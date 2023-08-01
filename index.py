import requests
import bs4
import pdb
import os
import shutil
import send2trash
import random
import re


class Crowler:
    source = ''   
    url = "https://virgool.io/JavaScript8/%D9%85%D8%B9%D8%B1%D9%81%DB%8C-8-%D9%85%D9%88%D8%B1%D8%AF-%D8%A7%D8%B2-%D8%A8%D8%B1%D8%AA%D8%B1%DB%8C%D9%86-%D9%81%D8%B1%DB%8C%D9%85-%D9%88%D8%B1%DA%A9-%D9%87%D8%A7%DB%8C-%D8%AC%D8%A7%D9%88%D8%A7-%D8%A7%D8%B3%DA%A9%D8%B1%DB%8C%D9%BE%D8%AA-p1nvywoef6pa"

    def __init__(self) -> None:
        send2trash.send2trash("files")
        os.mkdir("files")

    def setUrl(self,url):
        self.url = url

    def getContentUrl(self):
        result = requests.get(self.url)
        self.source = result


    def converToHtml(self):
        self.soup = bs4.BeautifulSoup(self.source.text)
    
    def store_images(self):
        if os.path.isdir("files/images") !=True:
            os.makedirs("files/images")

        images = self.soup.select("img")
        for img in images:
            image_link = requests.get(img['src'])
            name = str(random.randint(10000,10000000000))+".png"
            f= open(name,"wb")
            f.write(image_link.content)
            f.close()
            shutil.move(name,"files/images")

    def store_source(self):
        fsource = open("source.txt","a",encoding="utf-8")
        fsource.write(self.source.text)
        fsource.close()
        shutil.move("source.txt","files")

    def store_content(self):
        head = self.soup.select("h1")
        title = self.soup.select("title")
        post_body = self.soup.select("p")
        fs = open("content_post.txt","a",encoding="utf-8")
        fs.write(head[0].text)
        for content in post_body:
            try:
                text = content.text.encode()
                if content.getText() != "":
                    fs.write(f"{content.text} \n")
                else:
                    image = content.find("img")["src"]
                    image_link = requests.get(image)
                    name = str(random.randint(10000,10000000000))+".png"
                    f= open(name,"wb")
                    f.write(image_link.content)
                    f.close()
                    shutil.move(name,"files/images")
                    continue
            except Exception as e:
                print(e)
                continue
        fs.close()
        shutil.move("content_post.txt","files")

    def generate_zip(self):
        domainName = self.getDomainUrl()
        shutil.make_archive(f"compress_content_{domainName}_{random.randint(0,1000000)}","zip","files")

    def getDomainUrl(self):
        url = self.url
        url_pattern = re.compile(r"https?://([A-Za-z_0-9.-]+).*")
        result = re.search(url_pattern,url)
        return result.group(1)

    def crowler_web(self):
        self.getContentUrl()
        self.converToHtml()
        self.store_content()
        self.store_images()
        self.store_source()

crowler = Crowler()
crowler.setUrl("https://virgool.io/personal-development/%D8%A2%DA%A9%D8%B1%D8%A7%D8%B3%DB%8C%D8%A7%D8%9B-%DB%8C%D8%A7-%DA%86%D8%B1%D8%A7-%D8%A7%D9%86%D8%AC%D8%A7%D9%85-%DA%A9%D8%A7%D8%B1%DB%8C-%DA%A9%D9%87-%D9%85%D9%87%D9%85-%D8%A7%D8%B3%D8%AA-%D8%B1%D8%A7-%D8%A8%D9%87-%D8%AA%D8%B9%D9%88%DB%8C%D9%82-%D9%85%DB%8C%D8%A7%D9%86%D8%AF%D8%A7%D8%B2%DB%8C%D9%85-h5l1weygl9ai")
crowler.crowler_web()
crowler.generate_zip()
    






