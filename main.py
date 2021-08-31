# -*- coding: utf-8 -*-

from selenium import webdriver
import pickle


def get_cookies():
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")
    answ = input("If you are logged in write: Y")
    while answ != "Y":
        answ = input("To continue, enter: Y")
    pickle.dump(driver.get_cookies(), open("cookies", "wb"))
    driver.close()
