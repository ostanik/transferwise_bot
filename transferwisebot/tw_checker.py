#!/usr/bin/python
# -*- coding: latin-1 -*-
import requests
import os

def rateCompare(actual_rate, ideal_rate):
    return actual_rate > ideal_rate

def fetchChatId():
    return os.environ['MASTER_CHAT']

def fetchIdealRate():
    return 0.23345

def sendMessageTo(chat_id):
    telegramKey = os.environ['BOT_KEY']
    url = "https://api.telegram.org/bot%s/sendMessage" % (telegramKey)
    data = {"chat_id": chat_id, "text": "The BRL => EUR rate is really good, maybe you should transfer some money today :)"}
    requests.post(url, json=data)

def fetchTransferwiseRate():
    url = "https://transferwise.com/gateway/v2/quotes/"
    data = {"sourceAmount":1000,"sourceCurrency":"BRL","targetCurrency":"EUR","preferredPayIn":"BANK_TRANSFER","guaranteedTargetAmount":False}
    return requests.post(url, json=data).json()['rate']

def rateCompareBot():
    ideal_rate = fetchIdealRate()
    chat_id = fetchChatId()
    actual_rate = fetchTransferwiseRate()

    if rateCompare(actual_rate, ideal_rate):
        sendMessageTo(chat_id)


rateCompareBot()