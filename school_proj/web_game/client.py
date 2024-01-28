import requests
import time
import json
import pandas as pd


class Client:

    def __init__(self, nick: str, ip: str, port: str):
        self.nick = nick
        self.ip = ip
        self.port = port
        self.link = f"http://{ip}:{port}/main"

    def connect(self):
        responce = requests.post(self.link + '/connect', self.nick).text
        return responce

    def start_game(self):
        flag = True
        while flag:
            responce = requests.get(self.link + '/start').text
            if responce == '1':
                flag = False
            else:
                return False
        return True

    def get_info(self):
        responce = requests.get(self.link + '/get').text
        print(responce)

    def info(self):
        responce = requests.get(self.link + '/info').text
        print(responce)

    def buy_info(self):
        recpoce = requests.get(self.link + '/buy_info').text
        print(recpoce)

    def buy_p_info(self):
        response = requests.get(self.link + '/buy_plane').text
        print(response)

    def make_aircraft(self, count):
        responce = requests.post(self.link + '/produce', json={'Name': self.nick, 'Count': count}).json()
        return responce

    def sell_aircraft(self, count, money):
        recponce = requests.post(self.link + '/sell_plane',
                                 json={'Name': self.nick, 'Count': count, 'Money': money}).json()
        return recponce

    def finish_turn(self):
        flag = True
        while flag:
            responce = requests.get(self.link + '/finish_all').text
            if responce == '1':
                flag = False
            else:
                return False
        return True

    def finish(self):
        responce = requests.get(self.link + '/finish_turn', json={'Name': self.nick}).json()
        return responce

    def finish_transactions(self):
        responce = requests.get(self.link + '/finish', json={'Name': self.nick}).json()
        return responce

    def make_angar(self):
        response = requests.get(self.link + '/build', json={'Name': self.nick}).json()
        return response

    def end_build(self):
        responce = requests.get(self.link + '/end_build', json={'Name': self.nick}).json()
        return responce

    def send(self, count, money):
        responce = requests.get(self.link + '/buy_raw', json={'Name': self.nick, 'Count': count, 'Money': money}).json()
        return responce

    def pay(self):
        responce = requests.get(self.link + '/pay', json={'Name': self.nick}).json()
        print(responce)

    def end_game(self):
        responce = requests.get(self.link + '/end_game').text
        return responce


def connect_user():
    succes = True
    print("Connection")
    while succes:
        print('Write your nick')
        name = input()
        print('Write Server IP')
        IP = input()
        print('Write port')
        port = input()
        user = Client(name, IP, port)
        if user.connect() == '0':
            print('Write another name')
        else:
            print(f'Hello! {name}')
            succes = False
    return user


def user1():
    monthes = []
    Player = connect_user()
    counter_connect = 0
    counter_end = 0
    times = 0
    times1 = 0
    times2 = 0
    times3 = 0
    while True:
        counter_connect += 1
        if not Player.start_game():
            if counter_connect == 1:
                print('Waiting for players')
        else:
            break
    Player.get_info()
    Player.info()
    while True:
        print('What you want to do, pls print\nMake Aircraft\nGet Info\nFinish\nBuild\nBuy\nSell')
        print('WARNING: You can send one application once, if you app rejected by the bank, please wait the next move')
        user_choice = input().title()
        if user_choice == 'Make Aircraft':
            times += 1
            if times < 2:
                print('How many?')
                how = int(input())
                print(Player.make_aircraft(how))
            else:
                print('You can only do this action once')
        elif user_choice == 'Get Info':
            Player.get_info()
            Player.info()
            Player.buy_info()
            Player.buy_p_info()
        elif user_choice == 'Build':
            times1 += 1
            if times1 < 2:
                print(Player.make_angar())
            else:
                print('You can only do this action once')
        elif user_choice == 'Buy':
            times2 += 1
            if times2 < 2:
                print('How many')
                c = input()
                print('Price?')
                p = input()
                print(Player.send(c, p))
            else:
                print('You can only do this action once')
        elif user_choice == 'Sell':
            times3 += 1
            if times3 < 2:
                print('How many')
                c = input()
                print('Price?')
                p = input()
                print(Player.sell_aircraft(c, p))
            else:
                print('You can only do this action once')
        elif user_choice == 'Finish':
            sucses = True
            Player.finish()
            Player.pay()
            if Player.finish_transactions() == 'You lose':
                print('You lose')
                break
            while sucses:
                counter_end += 1
                if not Player.finish_turn():
                    if counter_end == 1:
                        print('Waiting for players')
                else:
                    times = 0
                    times1 = 0
                    times2 = 0
                    times3 = 0
                    Player.finish_transactions()
                    sucses = False
            if Player.end_game() != 'New turn':
                print(Player.end_game())
                break
            else:
                print(Player.end_game())
        else:
            print('Write correct command')


user1()
