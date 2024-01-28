import json
import pandas as pd
import numpy as np
from tabulate import tabulate


class Player:
    work_place = 2
    materials = 4
    fighters = 2
    money = 10000
    name: str


class Game:
    players: int
    month: int
    current_month = 1
    current_market = 3
    buyers_names = []
    count_of_materials = []
    payed_money = []
    sell_names = []
    count_of_planes = []
    give_money = []
    angar_buyers = []
    month_end = []
    names_cat = []
    count_cat = []
    money_cat = []
    plane_name_cat = []
    count_p_cat = []
    money_p_cat = []

    def __init__(self, players, names, month=48):
        self.players = players
        self.month = month
        self.players_in = names

    def make_json_info(self):
        columns = []
        data = []
        for player in self.players_in:
            columns += 'Fighters' + ' ' + player.name, 'Money' + ' ' + player.name, 'Materials' + ' ' + player.name, 'Work_place' + ' ' + player.name
            data += player.fighters, player.money, player.materials, player.work_place
        jsn = pd.DataFrame([data], columns=columns)
        result_info = tabulate(jsn, headers='keys', tablefmt='psql', showindex=False)
        return result_info

    def info(self):
        market_data = self.level_market()
        columns = 'Month', 'Market', 'Volume', 'Min_price', 'Fighters_want', 'Max_price'
        data = self.current_month, self.current_market, market_data[0], market_data[1], market_data[2], market_data[3]
        jsn = pd.DataFrame([data], columns=columns)
        result_info = tabulate(jsn, headers='keys', tablefmt='psql', showindex=False)
        return result_info

    def buy_info(self):
        columns = 'Name'
        jsn1 = pd.DataFrame(self.names_cat, columns=[columns])
        jsn1['Bought materials'] = self.count_cat
        jsn1['Money payed'] = self.money_cat
        result_info = tabulate(jsn1, headers='keys', tablefmt='psql', showindex=False)
        return result_info

    def buy_info_p(self):
        columns = 'Name'
        jsn1 = pd.DataFrame(self.plane_name_cat, columns=[columns])
        jsn1['Sold planes'] = self.count_p_cat
        jsn1['Money payed'] = self.money_p_cat
        result_info = tabulate(jsn1, headers='keys', tablefmt='psql', showindex=False)
        return result_info

    def pay_taxes(self, player: Player):
        tax = (300 * player.materials + 500 * player.fighters + 1000 * player.work_place)
        player.money -= (300 * player.materials + 500 * player.fighters + 1000 * player.work_place)
        return tax

    def level_market(self):
        data_market = [[1 * self.players, 800, 3 * self.players, 6500],
                       [int(1.5 * self.players), 650, int(2.5 * self.players), 6000],
                       [2 * self.players, 500, 2 * self.players, 5500],
                       [int(2.5 * self.players), 400, int(1.5 * self.players), 5000],
                       [3 * self.players, 300, 1 * self.players, 4500]]
        index_market = ['1', '2', '3', '4', '5']
        columns_market = ['Volume', 'Min_price', 'Fighters_want', 'Max_price']
        market = pd.DataFrame(data_market, index=index_market, columns=columns_market)
        return list(market.iloc[self.current_market - 1].to_numpy())

    def change_market_level(self):
        levels = [[0.33, 0.66, 0.82, 0.92, 1.0],
                  [0.25, 0.58, 0.83, 0.93, 1.0],
                  [0.1, 0.35, 0.68, 0.93, 1.0],
                  [0.1, 0.2, 0.45, 0.78, 1.0],
                  [0.1, 0.2, 0.36, 0.69, 0.1]]
        current_level = levels[self.current_market - 1]
        percent = float(np.random.rand(1).round(2))
        for i in range(len(current_level)):
            if percent <= current_level[i]:
                if i == 0:
                    self.current_market = 1
                elif i == 4:
                    self.current_market = 5
                else:
                    self.current_market = i + 1
                break

    def make_plane(self, player: Player, count):
        gamer = [x.name for x in self.players_in].index(player.name)
        gamer_wants = self.players_in[gamer]
        if gamer_wants.money >= 2000 * count and gamer_wants.materials >= 2 * count and gamer_wants.fighters + count <= gamer_wants.work_place:
            gamer_wants.money -= 2000 * count
            gamer_wants.materials -= 2 * count
            return True
        else:
            return False

    def make_angar(self, player: Player):
        if player.money > 2500 and player.work_place < 6:
            player.money -= 2500
            return True
        else:
            return False

    def buy_materials(self):
        chek_market = self.level_market().copy()
        chek_market = int(chek_market[0])
        while True:
            players_response = []
            for i in range(len(self.buyers_names)):
                players_response.append(self.count_of_materials[i] * self.payed_money[i])
            if chek_market == 0 or len(self.buyers_names) == 0:
                break
            first_winner = [self.buyers_names[players_response.index(max(players_response))],
                            self.count_of_materials[players_response.index(max(players_response))],
                            self.payed_money[players_response.index(max(players_response))]]
            for gamer in self.players_in:
                if gamer.name == first_winner[0]:
                    self.names_cat.append(first_winner[0])
                    gamer.money -= first_winner[2] * first_winner[1]
                    self.money_cat.append(first_winner[2] * first_winner[1])
                    gamer.materials += first_winner[1]
                    self.count_cat.append(first_winner[1])
                    chek_market -= first_winner[1]
                    self.buyers_names.pop(players_response.index(max(players_response)))
                    self.count_of_materials.pop(players_response.index(max(players_response)))
                    self.payed_money.pop(players_response.index(max(players_response)))
                if chek_market - first_winner[1] < 0:
                    first_winner[1] -= first_winner[1] - chek_market

    def sell_planes(self):
        chek_market = self.level_market().copy()
        chek_market = int(chek_market[2])
        while True:
            players_response1 = []
            for i in range(len(self.sell_names)):
                players_response1.append(self.count_of_planes[i] * self.give_money[i])
            if chek_market == 0 or len(self.sell_names) == 0:
                break
            first_winner = [self.sell_names[players_response1.index(min(players_response1))],
                            self.count_of_planes[players_response1.index(min(players_response1))],
                            self.give_money[players_response1.index(min(players_response1))]]
            print(first_winner[0])
            for gamer in self.players_in:
                if chek_market - first_winner[1] < 0:
                    first_winner[1] -= first_winner[1] - chek_market
                if gamer.name == first_winner[0]:
                    gamer.money += first_winner[2] * first_winner[1]
                    self.plane_name_cat.append(gamer.name)
                    self.money_p_cat.append(first_winner[2] * first_winner[1])
                    gamer.fighters -= first_winner[1]
                    self.count_p_cat.append(first_winner[1])
                    chek_market -= first_winner[1]
                    self.sell_names.pop(players_response1.index(min(players_response1)))
                    self.count_of_planes.pop(players_response1.index(min(players_response1)))
                    self.give_money.pop(players_response1.index(min(players_response1)))

    def is_valid(self, count, money, player: Player):
        market_for_now = self.level_market()
        if money < int(market_for_now[1]) or money == 0 or count == 0 or player.money < money * count or count > int(
                market_for_now[0]):
            return False
        else:
            self.buyers_names.append(player.name)
            self.payed_money.append(money)
            self.count_of_materials.append(count)
            return True

    def is_sell(self, count, money, player: Player):
        market_for_now = self.level_market()
        if money > int(market_for_now[3]) or count == 0 or count > int(market_for_now[2]) or player.fighters < count:
            return False
        else:
            self.sell_names.append(player.name)
            self.give_money.append(money)
            self.count_of_planes.append(count)
            return True

    def end_build(self):
        current_month = self.current_month
        if current_month in self.month_end:
            for player in self.players_in:
                if player.name in self.angar_buyers and self.month_end[
                    self.angar_buyers.index(player.name)] == current_month:
                    player.money -= 2500
                    self.month_end.pop(self.angar_buyers.index(player.name))
                    self.angar_buyers.pop(self.angar_buyers.index(player.name))
                    player.work_place += 1

    def player_capital(self, player):
        r = self.level_market()[1]
        f = self.level_market()[-1]
        cap = 0
        for i in self.players_in:
            if player == i:
                cap = player.money + (player.work_place * 5000) + (player.fighters * f) + (player.materials * r)
        return cap

    def winner(self):
        data = []
        data_n = []
        for player in self.players_in:
            data.append(self.player_capital(player))
            data_n.append(player.name)
        jsn = pd.DataFrame([data], columns=data_n)
        result_info = tabulate(jsn, headers='keys', tablefmt='psql', showindex=False)
        return result_info
