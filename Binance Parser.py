import threading
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import telebot

# import main

#EXE_PATH = r"F:\python\Anonymous-chat-telegram-master bkp\chromedriver.exe"  # EXE_PATH это путь до ранее загруженного нами файла chromedriver.exe

bot = telebot.TeleBot('Your Telegram Bot API')
name = []
tickers = []
numbers = []
chrome_options = Options()
chrome_options.add_argument("--headless")
# Using Chrome to access web
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))


# Open the website
def getconnect(driver):
    try:
        driver.get(
            'https://www.binance.com/ru/futures-activity/leaderboard?type=myProfile&encryptedUid=47E6D002EBB1173967A6561F72B9395C') # your link on binance profile
        time.sleep(5)
        id_box = driver.find_element(By.ID, 'tab-MYPOSITIONS')
        id_box.click()
        time.sleep(3)
        driver.save_screenshot("screenshot.png")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        print('Я работаю')
        return soup
    except Exception as E:
        print(E)


time1 = time.time()
t = threading.Thread(target=getconnect(driver), name='Chrome')

t.start()


@bot.message_handler(commands=['start', 'command1'])
def start_message(message):
    def get_data():
        print('Запрос получен')
        bot.send_message(message.chat.id, 'Собираю информацию...')
        # bot.send_message(message.chat.id,message.chat.id)
        table = []
        last = []
        soup = getconnect(driver)
        time.sleep(10)
        print(soup.find('tr', class_='bn-table-row'))
        trs = soup.find('tbody', class_='bn-table-tbody').find_all('tr')
        for tr in trs:
            club = tr.find_all('td', class_='bn-table-cell')

            for i in club:
                clubs = i.text.replace('\n', '')
                table.append(clubs)
        print(table)
        for i in range(0, int(len(table) / 6)):
            a = float(table[3 + (i * 6)].replace(',', '').replace("−", "-"))
            b = float(table[2 + (i * 6)].replace(',', '').replace("−", "-"))
            d = table[4 + (i * 6)].replace(',', '').replace("-", "-").partition('(')[0]

            c = float(d)
            if a - b > 0 and c > 0:
                last.append('LONG позиция')
                print('long')
            elif a - b > 0 and c < 0:
                last.append('SHORT позиция')
                print('short')
            elif a - b < 0 and c > 0:
                last.append('SHORT позиция')
                print('short')
            elif a - b < 0 and c < 0:
                last.append('LONG позиция')
                print('long')
            else:
                last.append('Не удалось узнать позицию')
                print('Не рассчитано ')
            level = abs((a - b) / abs(b)) * 100
            f = table[4 + (i * 6)].replace(',', '').replace("-", "").partition('(')[2].replace(')', '').replace('%', '')
            # print(float(f), float(level))
            if level == 0:
                level = 1
            lev = int(((float(f) / abs(float(level))) // 1))
            try:
                bot.send_message(message.chat.id,
                                 'Тикер: ' + str(table[0 + (i * 6)]) +
                                 '\nРазмер: ' + str(table[1 + (i * 6)]) +
                                 '\nЦена входа: ' + str(table[2 + (i * 6)]) +
                                 '\nЦена маркировки: ' + str(table[3 + (i * 6)]) +
                                 '\nPNL (ROE %): ' + str(table[4 + (i * 6)]) +
                                 '\nВремя: ' + str(table[5 + (i * 6)]) +
                                 '\n' + str(last[i]) +
                                 '\nПримерное плечо: x' + str(lev))

            except IndexError as e:
                print(e)

    get_data()


bot.polling(none_stop=True)
"""if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            bot.send_message(936853523, 'Я отключился')
            print(e)
            time.sleep(10)"""
