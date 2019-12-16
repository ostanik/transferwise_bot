#!/usr/bin/python
# -*- coding: latin-1 -*-
import requests
import locale
import os

def rate_compare(actual_rate, ideal_rate):
    return actual_rate > ideal_rate

def fetch_chat_id():
    return os.environ['MASTER_CHAT']

def fetch_ideal_rate():
    return 0.22

def send_message_to(chat_id, savings, actual_rate):
    telegramKey = os.environ['BOT_KEY']
    url = "https://api.telegram.org/bot%s/sendMessage" % (telegramKey)

    spacer = "\n------\n"
    header = "The BRL => EUR rate is really good\n\n"
    body = "You can earn more %s since your last transfer\n\n Actual rate: %.5f\n Last rate: %.5f" % (savings, actual_rate, fetch_ideal_rate())
    message = spacer+header+body+spacer

    data = {"chat_id": chat_id, "text": message}
    requests.post(url, json=data)

def fetch_tw_object():
    url = "https://transferwise.com/gateway/v2/quotes/"
    data = {"sourceAmount":5000,"sourceCurrency":"BRL","targetCurrency":"EUR","preferredPayIn":"BANK_TRANSFER","guaranteedTargetAmount":False}
    return requests.post(url, json=data).json()

def savings_from_last_transfer(tw_object):
    value = tw_object['paymentOptions'][1]['targetAmount']
    diff = float(value) - 1138.07
    return locale.currency(diff)

def rate_compare_bot():
    locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')
    ideal_rate = fetch_ideal_rate()
    chat_id = fetch_chat_id()
    tw_object = fetch_tw_object()
    actual_rate = tw_object['rate']
    savings = savings_from_last_transfer(tw_object)

    if rate_compare(actual_rate, ideal_rate):
        send_message_to(chat_id, savings, actual_rate)

rate_compare_bot()