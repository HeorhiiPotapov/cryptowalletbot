import json
from openpyxl import Workbook

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from openpyxl import Workbook
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver

import config
import undetected_chromedriver
import time
import httplib2


def save_to_excel(data: list, filename: str) -> None:
    # Initialize workbook and active sheet
    wb = Workbook()
    ws = wb.active
    # Define headers based on the keys of the first dictionary
    headers = ["token", "profit", "unr_profit", "gross", "trades", "bought",
               "sold", "avg_buy_price", "avg_sell_price", "last_type", "last", "first_in"]
    # Write headers to the first row
    ws.append(headers)
    # Write each dictionary in the list to the rows
    for item in data:
        ws.append([item["token"], item["profit"], item["unr_profit"], item["gross"],
                   item["trades"], item["bought"], item["sold"], item["avg_buy_price"],
                   item["avg_sell_price"], item["last_type"], item["last"], item["first_in"]])
    # Save the file
    wb.save(filename)


def parse_address(address: str) -> dict:
    # setup selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
    options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(options=options)
    browser.get('https://dexcheck.ai/app/wallet-analyzer/' + address)

    try:
        WebDriverWait(browser, 30).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="layout-scroll"]/div[2]/div[1]/div[2]/div/div[1]/p')))

        html = browser.page_source

        # parse static data
        soup = BeautifulSoup(html, "html.parser")
        dom = etree.HTML(str(soup))

        grass = dom.xpath('//*[@id="layout-scroll"]/div[2]/div[1]/div[2]/div/div[1]/p')[0].text
        roi = dom.xpath('//*[@id="layout-scroll"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/p')[0].text
        winrate = dom.xpath('//*[@id="layout-scroll"]/div[2]/div[1]/div[2]/div/div[3]/div[1]/p')[0].text
        volume = dom.xpath('//*[@id="layout-scroll"]/div[2]/div[1]/div[2]/div/div[4]/div[2]/p')[0].text
        total_trades = dom.xpath('//*[@id="layout-scroll"]/div[2]/div[1]/div[2]/div/div[4]/div[3]/p')[0].text
        print(grass, roi, winrate, volume, total_trades)
        main_data = (
            f"💵 Grass: {grass} \n"
            f"👑 ROI: {roi} \n"
            f"🏆 WinRate: {winrate} \n"
            f"🚥 Volume: {volume} \n"
            f"📊 Total trades {total_trades} \n"
        )
        # parsing dynamic table
        table = browser.find_element(By.XPATH, '//*[@id="layout-scroll"]/div[2]/div[1]/div[4]/table/tbody')
        actions = ActionChains(browser)
        actions.move_to_element(table).click().perform()

        data = []
        while True:
            rows = table.find_elements(
                By.XPATH,
          '/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[4]/table/tbody/div/div/div/div'
            )
            for row in rows:
                if row not in data:
                    element_soup = BeautifulSoup(row.get_attribute('outerHTML'), 'lxml')
                    text = element_soup.get_text(separator='\n', strip=True).split('\n')

                    token, profit, unr_profit, gross, trades, bought, sold, avg_buy_price, avg_sell_price, last_type, last, first_in = \
                        text[1], text[2], text[4], text[6], text[8], text[9], text[12], text[15], text[16], text[17], \
                            text[18], \
                            text[19]
                    data_element = {
                        "token": token,
                        "profit": profit,
                        "unr_profit": unr_profit,
                        "gross": gross,
                        "trades": trades,
                        "bought": bought,
                        "sold": sold,
                        "avg_buy_price": avg_buy_price,
                        "avg_sell_price": avg_sell_price,
                        "last_type": last_type.capitalize(),
                        "last": last,
                        "first_in": first_in
                    }
                    data.append(data_element)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            new_rows = table.find_elements(By.XPATH,
                                           '/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[4]/table/tbody/div/div/div/div')
            if rows == new_rows:
                break
        # data = list(set(data))
        # print("DATA ======>>>>>", str(data)[:50])
        # # writing to google sheet
        # credentials = ServiceAccountCredentials.from_json_keyfile_name(
        #     'creds.json',
        #     ['https://www.googleapis.com/auth/spreadsheets',
        #      'https://www.googleapis.com/auth/drive'])
        # print("CREDENTIALS ======>", credentials)
        # httpAuth = credentials.authorize(httplib2.Http())
        # print("HTTPAUTH ======>>>>>", httpAuth)
        # service = build('sheets', 'v4', http=httpAuth)
        # print("SERVICE ======>", service)
        # service.spreadsheets().values().clear(
        #     spreadsheetId=config.SHEETS_ID,
        #     range='A5:K1000'
        # ).execute()
        # service.spreadsheets().values().batchUpdate(
        #     spreadsheetId=config.SHEETS_ID,
        #     body={
        #         "valueInputOption": "USER_ENTERED",
        #         "data": [
        #             {"range": "A2:F2",
        #              "majorDimension": "ROWS",
        #              "values": [[address, grass, roi, winrate, volume, total_trades]]},
        #             {"range": f"A5:K{len(data) + 5}",
        #              "majorDimension": "ROWS",
        #              "values": [[element['token'], element['profit'],
        #                          element['unr_profit'], element['gross'],
        #                          element['trades'], element['bought'],
        #                          element['sold'], element['avg_buy_price'],
        #                          element['avg_sell_price'], element['last_type'] + ' ' + element['last'],
        #                          element['first_in']] for element in data]}
        #         ]
        #     }
        # ).execute()
        #
        # # save result to xlsx
        # sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=config.SHEETS_ID, range='Лист1').execute()
        # values = result.get('values', [])
        #
        # wb = Workbook()
        # ws = wb.active
        #
        # for row in values:
        #     ws.append(row)
        #
        # wb.save(f'{address}.xlsx')
        #
        # return f'{address}.xlsx'

        save_to_excel(data, filename=f'{address}.xlsx')
        return {
            'filename': f'{address}.xlsx',
            'main_data': main_data,
        }

    except Exception as e:
        print(e)
        return None
    finally:
        browser.quit()
