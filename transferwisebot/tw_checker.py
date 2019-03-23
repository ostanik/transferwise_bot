#!/usr/bin/python
# -*- coding: latin-1 -*-
import requests
import os

def rate_compare(actual_rate, ideal_rate):
    return actual_rate > ideal_rate

def fetch_chat_id():
    return os.environ['MASTER_CHAT']

def fetch_ideal_rate():
    return 0.23345

def send_message_to(chat_id):
    telegramKey = os.environ['BOT_KEY']
    url = "https://api.telegram.org/bot%s/sendMessage" % (telegramKey)
    data = {"chat_id": chat_id, "text": "The BRL => EUR rate is really good, maybe you should transfer some money today :)"}
    requests.post(url, json=data)

def fetch_tw_rate():
    url = "https://transferwise.com/gateway/v2/quotes/"
    data = {"sourceAmount":1000,"sourceCurrency":"BRL","targetCurrency":"EUR","preferredPayIn":"BANK_TRANSFER","guaranteedTargetAmount":False}
    return requests.post(url, json=data).json()['rate']

def rate_compare_bot():
    ideal_rate = fetch_ideal_rate()
    chat_id = fetch_chat_id()
    actual_rate = fetch_tw_rate()

    if rate_compare(actual_rate, ideal_rate):
        send_message_to(chat_id)


rate_compare_bot()