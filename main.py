from selenium import webdriver
import pickle


def get_cookies():
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")
    answ = input("Если вы авторизировались напишите Y: ")
    while answ != "Y":
        answ = input("Для продолжения введите Y: ")
    pickle.dump(driver.get_cookies(), open("cookies", "wb"))
    driver.close()
