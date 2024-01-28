from flask import Flask, request, jsonify
from game import Player, Game

names = []
names_local = []
plane_buyers = []
count_planes = []
count_of_players = []
app = Flask(__name__)
print('Please, print count of players')
pl = int(input())
print('Please, pick count of month')
mo = int(input())
game = Game(pl, names, mo)


@app.route('/main/connect', methods=['POST'])
def connect_user():
    if request.method == 'POST':
        user_name = request.get_data()
        user_name = bytes.decode(user_name, encoding='utf-8')
        user = Player()
        user.name = user_name
        names_local.append(user_name)
        if names_local.count(user.name) == 1:
            names.append(user)
            return "1"
        else:
            return '0'


@app.route('/main/end_game', methods=['POST', 'GET'])
def end_game():
    if game.month + 1 == game.current_month or (len(game.players_in) == 1 and game.players != 1):
        return game.winner()
    elif len(game.players_in) == 0:
        return f"All players without money now, game over"
    else:
        return "New turn"


@app.route('/main/get', methods=['GET'])
def load_info():
    return game.make_json_info()


@app.route('/main/info', methods=['GET'])
def info():
    return game.info()


@app.get('/main/buy_info')
def buy_info():
    if len(game.names_cat) != 0:
        return game.buy_info()
    else:
        return 'Not raw deals yet'


@app.get('/main/buy_plane')
def buy_p_info():
    if len(game.plane_name_cat) != 0:
        return game.buy_info_p()
    else:
        return "Not plane deals yet"


@app.route('/main/produce', methods=['POST'])
def produce_plane():
    who_wants = request.json['Name']
    count = request.json['Count']
    for player in names:
        if player.name == who_wants and game.make_plane(player, count):
            plane_buyers.append(who_wants)
            count_planes.append(count)
            return jsonify('Ok we do this aircrafts for you')
    else:
        return jsonify('You need more money or materials')


@app.route('/main/build', methods=['POST', 'GET'])
def make_angar():
    current_month = game.current_month
    who_wants = request.json['Name']
    for player in names:
        if player.name == who_wants and game.make_angar(player):
            game.angar_buyers.append(who_wants)
            game.month_end.append(current_month + 3)
            print(game.month_end)
            print(game.angar_buyers)
            return jsonify('Ok, we make this angar for you')
    else:
        return jsonify("You need more money")


@app.route('/main/start', methods=['GET'])
def start_game():
    if len(names) == game.players:
        return '1'
    else:
        return '0'


@app.route('/main/finish', methods=['GET', 'POST'])
def finish_transactions():
    for player in names:
        if player.money < 0:
            names.remove(player)
            game.players -= 1
            return jsonify("You lose")
        else:
            return jsonify('OK')


@app.route('/main/finish_turn', methods=['GET', 'POST'])
def finish_one():
    who_wants = request.json['Name']
    count_of_players.append(who_wants)
    if len(count_of_players) % len(names) == 0:
        game.buy_materials()
        game.buyers_names.clear()
        game.count_of_materials.clear()
        game.payed_money.clear()
        game.sell_planes()
        game.sell_names.clear()
        game.count_of_planes.clear()
        game.give_money.clear()
        game.end_build()
        game.current_month += 1
        game.change_market_level()
        for player in names:
            if player.name in plane_buyers:
                player.fighters += count_planes[plane_buyers.index(player.name)]
                count_planes.pop(plane_buyers.index(player.name))
                plane_buyers.remove(player.name)
    return jsonify('All transactions finished')


@app.route('/main/pay', methods=['GET', 'POST'])
def pay():
    who_wants = request.json['Name']
    for player in names:
        if player.name == who_wants:
            return jsonify(f"At this month you payed {game.pay_taxes(player)} evil tax")


@app.route('/main/finish_all', methods=['GET', 'POST'])
def finish():
    if len(count_of_players) % len(names) == 0:
        return '1'
    else:
        return '0'


@app.route('/main/buy_raw', methods=['POST', 'GET'])
def buy_raw():
    who_wants = request.json['Name']
    count = request.json['Count']
    money_payed = request.json['Money']
    count = int(count)
    money_payed = int(money_payed)
    for player in names:
        if player.name == who_wants and game.is_valid(count, money_payed, player):
            return jsonify("You application is accepted")
    else:
        return jsonify("Please send the valid application")


@app.route('/main/sell_plane', methods=['POST', 'GET'])
def sell_plane():
    who_wants = request.json['Name']
    count = request.json['Count']
    money_payed = request.json['Money']
    count = int(count)
    money_payed = int(money_payed)
    for player in names:
        if player.name == who_wants and game.is_sell(count, money_payed, player):
            return jsonify("You application is accepted")
    else:
        return jsonify("Please send the valid application")


@app.route('/main')
def main_page():
    return "main page"


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
