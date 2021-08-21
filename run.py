import pickle
import selenium.webdriver
import time
from random import triangular
import os
from urllib.request import urlretrieve
from os.path import isfile
from main import get_cookies


class IntstParser:
    def __init__(self):
        self.driver = selenium.webdriver.Chrome()
        self.cookies = pickle.load(open("cookies", "rb"))
        self.txt_link = input("Укажите путь до txt файла: ")
        while not isfile(self.txt_link):
            self.txt_link = input("Укажите правильный путь: ")
        else:
            print("Файл найден")
        self.sumbol_count = int(input("Укажите минимальное количество символов в посте: "))

    def start(self):
        self.driver.get("https://www.instagram.com/")
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

        time.sleep(triangular(0.0, 3.0))

        self.profile_find()

    def save_data(self, post_data, folder_link):
        with open(f"{folder_link}/info.txt", mode="w", encoding="utf8") as text:
            text.write(post_data)

        article = self.driver.find_element_by_class_name("_97aPb ")

        try:
            img = article.find_element_by_tag_name("img").get_attribute('src')
        except Exception:
            img = article.find_element_by_tag_name("video").get_attribute('poster')

        urlretrieve(img, f"{folder_link}/pic.png")

    def get_post_link(self, url):
        data = []
        cheker = count = 0

        self.driver.get(url)
        height = 200
        time.sleep(triangular(0.0, 2.0))

        while True:
            for elem in self.driver.find_element_by_class_name("ySN3v").find_elements_by_tag_name("a"):
                link = elem.get_attribute("href")
                if link not in data:
                    data.append(link)
            if count >= 5:
                break
            if len(data) == cheker:
                count += 1
            else:
                count = 1
            self.driver.execute_script(f"window.scrollTo(0, {height})")

            height += triangular(600, 800)

            time.sleep(triangular(0.0, 1.0))

            cheker = len(data)

        return data

    def chek_posts(self, post_link, post_author):
        self.driver.get(post_link)
        try:
            data = self.driver.find_element_by_class_name("C4VMK").find_elements_by_tag_name("span")
            author = data[0].text
            if author == post_author:
                info = data[1].text
            else:
                info = ""
        except IndexError:
            info = ""
        return info

    def profile_create_folders(self, prfl_name):
        try:
            os.mkdir(prfl_name)
            url = f"https://www.instagram.com/{prfl_name}"
            posts_data = self.get_post_link(url)
            count = 1
            for post_url in posts_data:
                info = self.chek_posts(post_url, prfl_name)
                if len(info) >= self.sumbol_count:
                    link = f"{prfl_name}/{count}"
                    os.mkdir(path=link)
                    self.save_data(info, link)
                    count += 1

        except FileExistsError:
            print("Данная папка уже существует")

    def profile_find(self):
        with open(self.txt_link, mode="r", encoding="utf8") as data:
            for name in data.readlines():
                self.profile_create_folders(name.strip())


if __name__ == "__main__":
    get_cookies()
    st = IntstParser()
    try:
        st.start()
        st.driver.close()
    except Exception as ex:
        print(ex)
        st.driver.close()
