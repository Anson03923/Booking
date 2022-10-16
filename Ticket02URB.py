from logging import debug
from re import T
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
from multiprocessing import freeze_support
import os

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = uc.Chrome(use_subprocess=True)

debug = True
LINK = "https://ticket.urbtix.hk/internet/"
CLINK = "https://ticket.urbtix.hk/internet/zh_TW/eventDetail/43886"
ERRORLINK = "http://msg.urbtix.hk/"
driver.get(CLINK)
driver.implicitly_wait(180)

while(True):
    time.sleep(0.2)
    if(driver.find_elements(By.XPATH, "/html/body/table/tbody/tr[3]/td")):
        driver.get(CLINK)
        continue
    elif(driver.find_elements(By.XPATH, "/html/body/div[1]/div[4]/div[3]/div[3]/a")):
        break
driver.implicitly_wait(5)

print("Success login to timeslot page?\nInput ANY to continue.")
input()

    
timeslots = driver.find_elements(By.XPATH, '//*[@id="evt-perf-items-tbl"]/tbody/tr')

for i, timeslot in enumerate(timeslots):
    print("Input " + str(i) + " for:")
    print(timeslot.find_element(By.CLASS_NAME, 'perf-name-col').text)
    date = timeslot.find_elements(By.CLASS_NAME, 'perf-cal-div')
    for specific in date:
        print(specific.text, end = "")
    print(timeslot.find_element(By.CLASS_NAME, 'perf-time-col').text)
    print("\n")

print("Number of timeslot: " + str(len(timeslots)))

while(True):
    try:
        print("Input desired timeslot(Staring from 0): ")
        timeslot_id = int(input())
        timeslots[timeslot_id].find_element(By.CLASS_NAME, 'perf-purchase-col').click()
        break
    except IndexError:
        print("Input correct timeslot.")
    except ValueError:
        print("Input correct value.")
    except: 
        print("Unknown Error.")

print("\nLogin... \nPress ANY if login")
input()

fees = driver.find_elements(By.XPATH, '//*[@id="ticket-price-tbl"]/tbody/tr')

maximum_fee_index = 0
if(debug):
    print("Before, Length of fees list:" + str(len(fees)))

for i, fee in enumerate(fees):
    if(fee.find_elements(By.TAG_NAME, 'font')):
        maximum_fee_index = i
        for _ in range(len(fees) - maximum_fee_index):
            fees.pop()
        break

if(debug):
    print("After, Length of fees list:" + str(len(fees)))

for i, fee in enumerate(fees):   
    print("Input " + str(i) + " for: ")
    print((fee.find_element(By.TAG_NAME, 'label').text).strip())

while(True):
    try:
        print("\nInput ticket fee index: ")
        fee_index = int(input())
        print(fee_index)
        fees[fee_index].find_element(By.CLASS_NAME, 'pricezone-radio-input').click()
        break
    except IndexError:
        print("Input correct fee index.")
    except ValueError:
        print("Input correct value fee index")
    except:
        print("Unknown Error.")

print("---------------------------------------------------------------")

time.sleep(2)
driver.implicitly_wait(180)
tickets = driver.find_elements(By.XPATH, '//*[@id="ticket-type-tbl"]/tbody/tr')

for i, ticket in enumerate(tickets):
    print("Input " + str(i) + " for type: ")
    print(tickets[i].find_element(By.CLASS_NAME, 'ticket-type-col').text)
    #print("Maximum ticket number is: " + str(len(ticket.find_elements(By.XPATH, '//*[@id="ticket-quota-223-sel"]/option')) - 1))
    print("\n")
  
while(True): 
    print("Input ticket type:")
    t_ticket = int(input())
    if(debug):
        print(t_ticket)
        print(len(tickets))
    print("Input ticket number required: ")
    r_ticket = int(input())
    if(debug):
        print(r_ticket)
        print(len(ticket.find_elements(By.XPATH, '/html/body/div[2]/form/div[3]/div[2]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[2]/select/option')) - 1)
    if(t_ticket < len(tickets) and r_ticket < len(ticket.find_elements(By.XPATH, '/html/body/div[2]/form/div[3]/div[2]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[2]/select/option'))):
        break

tickets[t_ticket].find_element(By.XPATH, ('/html/body/div[2]/form/div[3]/div[2]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[2]/select/option[' + str(r_ticket + 1)+']')).click()

##tickets[t_ticket].find_element(By.CLASS_NAME, 'chzn-select ticket-quota-select').find_element(By.TAG_NAME, 'option[0]').click()

##print("Concatenate seat default reverse:")
##
##if(input() == "Yes"):
##    driver.find_element(By.ID, 'adjacent-seats-chk').click()

if(debug):
    print("Waiting for shopping cart page")

j = 1

while(True):
    driver.implicitly_wait(3)
    if(debug):
        print(str(j) + " tries.")
    driver.find_element(By.CLASS_NAME, 'btn-inner-blk').click()
    ##if(driver.find_elements(By.CLASS_NAME, 'ajax-loading')):
    ##    time.sleep(3)
    ##    if(driver.find_elements(By.XPATH, '//*[@id="reviewTicketForm"]/div[8]/div/div')):
    ##        break
    if(debug):
        print("Accessing")
    driver.implicitly_wait(1)
    if(driver.find_elements(By.XPATH, '//*[@id="reviewTicketForm"]/div[8]/div/div')):
        break
    driver.implicitly_wait(3)
    for i in range(1):
        print("Sleeping time: " + str(i))
        time.sleep(1)
    driver.implicitly_wait(10)
    fees = driver.find_elements(By.XPATH, '//*[@id="ticket-price-tbl"]/tbody/tr')
    fees[fee_index].find_element(By.CLASS_NAME, 'pricezone-radio-input').click()
    for i in range(3):
        print("Sleeping time: " + str(i))
        time.sleep(1)
    tickets = driver.find_elements(By.XPATH, '//*[@id="ticket-type-tbl"]/tbody/tr')
    tickets[t_ticket].find_element(By.XPATH, ('/html/body/div[2]/form/div[3]/div[2]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[2]/select/option[' + str(r_ticket + 1)+']')).click()
    j += 1

if(debug):
    print("Cart page loaded.")

driver.find_element(By.XPATH, '//*[@id="reviewTicketForm"]/div[8]/div/div').click()

if(debug):
    print("Successfully added to cart.")


## /html/body/div[7]/div/div[1]
## /html/body/div[7]/div/div[1]/img
## add waiting detection

time.sleep(1800)
driver.find_element(By.XPATH, '//*[@id="reviewTicketForm"]')## keep opening