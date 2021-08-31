   # -*- coding: utf-8 -*-

import pickle
import selenium.webdriver
import time
from random import triangular
import os
from urllib.request import urlretrieve
from os.path import isfile, isdir
from main import get_cookies
import shutil


class IntstParser:
    def __init__(self, work_dir, txt_link, sumbol_count):
        self.work_dir = work_dir
        self.driver = selenium.webdriver.Chrome()
        self.cookies = pickle.load(open("cookies", "rb"))
        self.txt_link = txt_link
        self.sumbol_count = sumbol_count

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

    def get_post_link(self, url, work_dir):
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

            height += triangular(500, 800)

            time.sleep(triangular(1.0, 3.0))

            cheker = len(data)
            print(cheker)

        with open(f"{work_dir}/posts_link.txt", mode="w", encoding="utf8") as text:
            for post in data:
                text.write(post + "\n")

        print(len(data))

        with open(f"{work_dir}/posts_num.txt", mode="w", encoding="utf8") as text:
            text.write(f"1/{len(data)}")

    def chek_posts(self, post_link, post_author):
        self.driver.get(post_link)
        time.sleep(triangular(1.0, 3.0))
        try:
            data = self.driver.find_element_by_class_name("C4VMK").find_elements_by_tag_name("span")
            author = data[0].text
            if author == post_author:
                info = data[1].text
            else:
                info = ""
        except IndexError:
            info = ""
        except Exception as ex:
            print(f"Found Exception: {ex}")
            info = ""
            self.driver.close()
        return info

    def profile_create_folders(self, prfl_name):
        dir_for_prof = f"{self.work_dir}/{prfl_name}"

        if isdir(dir_for_prof):
            print("The directory exists, do you want to continue working?")
            answ = input("Write Y: ")
            while answ != "Y":
                answ = input("Write Y: ")
        else:
            os.mkdir(dir_for_prof)
            url = f"https://www.instagram.com/{prfl_name}"
            self.get_post_link(url, dir_for_prof)

        with open(f"{dir_for_prof}/posts_link.txt", mode="r", encoding="utf8") as posts_data:
            with open(f"{dir_for_prof}/posts_num.txt", mode="r", encoding="utf8") as posts_num:
                num = int(posts_num.read().split("/")[0])
                count = num
                if isdir(f"{dir_for_prof}/{num}"):
                    shutil.rmtree(f"{dir_for_prof}/{num}")
                for post_url in posts_data.readlines()[num - 1 if num - 1 >= 0 else 0:]:
                    info = self.chek_posts(post_url.strip(), prfl_name)
                    with open(f"{dir_for_prof}/posts_num.txt", mode="r", encoding="utf8") as text:
                        nums = text.read().split("/")
                    with open(f"{dir_for_prof}/posts_num.txt", mode="w", encoding="utf8") as text:
                        text.write(f"{count}/{nums[1]}")
                    if len(info) >= self.sumbol_count:
                        link = f"{self.work_dir}/{prfl_name}/{count}"
                        os.mkdir(path=link)
                        self.save_data(info, link)
                        count += 1

    def profile_find(self):
        with open(self.txt_link, mode="r", encoding="utf8") as data:
            for name in data.readlines():
                self.profile_create_folders(name.strip())


if __name__ == "__main__":
    print("Provide the directory for the parser to work: ")
    work_folder = input().replace("\\", "/")

    while not isdir(work_folder):
        work_folder = input("Provide the true path!").replace("\\", "/")
    else:
        print("Directory selected")

    file_link = input("Provide the path to the .txt file: ").replace("\\", "/")
    while not isfile(file_link):
        file_link = input("Provide the correct path: ").replace("\\", "/")
    else:
        print("File found")

    while True:
        try:
            number = int(input("Specify the minimum number of characters in a post:"))
            break
        except TypeError:
            pass

    if not isfile("cookies"):
        get_cookies()

    st = IntstParser(work_folder, file_link, number)
    try:
        st.start()
        st.driver.close()
        print("The work has been completed.")
    except Exception as ex:
        print(ex)
        st.driver.close()
