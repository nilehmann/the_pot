import os
import random

import sqlalchemy as sa
from flask import Flask, request, safe_join, send_file, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = 'game'

    id = sa.Column(sa.Integer, primary_key=True)
    max_cards = sa.Column(sa.Integer, nullable=False)
    cards = relationship('Card', backref="game")
    teams = relationship('Team', backref="game")

    def serialize(self, *keys):
        if not keys:
            keys = ['id', 'teams', 'maxCards']
        data = {}
        for key in keys:
            if key == 'id':
                data[key] = self.id
            if key == 'teams':
                data[key] = [t.serialize() for t in self.teams]
            if key == 'maxCards':
                data[key] = self.max_cards
        return data


class Team(db.Model):
    __tablename__ = 'team'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    game_id = sa.Column(sa.Integer, sa.ForeignKey('game.id'), nullable=False)
    players = relationship('Player', backref="team")

    def serialize(self, *keys):
        if not keys:
            keys = ["id", "name", "players", "guessedCount"]
        data = {}
        for key in keys:
            if key == "id":
                data[key] = self.id
            if key == "name":
                data[key] = self.name
            if key == "players":
                data[key] = [p.serialize() for p in self.players]
            if key == "guessedCount":
                data[key] = Card.query.join(Card.guesser).filter(Player.team_id == self.id).count()
        return data


class Player(db.Model):
    __tablename__ = 'player'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    team_id = sa.Column(sa.Integer, sa.ForeignKey('team.id'), nullable=False)
    cards = relationship('Card', backref="player", foreign_keys='Card.player_id')
    guessed = relationship('Card', backref="guesser", foreign_keys='Card.guessed_by')

    def serialize(self, *keys):
        if not keys:
            keys = ['id', 'name', 'guessedCount', 'createdCount']
        data = {}
        for key in keys:

            if key == 'id':
                data[key] = self.id
            if key == 'name':
                data[key] = self.name
            if key == 'guessedCount':
                data[key] = Card.query.join(Player.guessed).filter(Player.id == self.id).count()
            if key == 'createdCount':
                data[key] = Card.query.join(Player.cards).filter(Player.id == self.id).count()
        return data


class Card(db.Model):
    __tablename__ = 'card'

    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.Text, nullable=False)
    game_id = sa.Column(sa.Integer, sa.ForeignKey('game.id'), nullable=False)
    guessed_by = sa.Column(sa.Integer, sa.ForeignKey('player.id'))
    player_id = sa.Column(sa.Integer, sa.ForeignKey('player.id'), nullable=False)

    def serialize(self, *keys):
        if not keys:
            keys = ["id", "text"]
        data = {}
        for key in keys:
            if key == "id":
                data[key] = self.id
            if key == "text":
                data[key] = self.text
            if key == "guessedBy":
                data[key] = self.guesser and self.guesser.serialize()
        return data


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    path = safe_join('ui/dist', path)
    if os.path.exists(path):
        return send_file(path)
    else:
        return send_from_directory('ui/dist', 'index.html')


@app.route("/api/games", methods=["PUT"])
def new_game():
    data = request.json
    game = Game(max_cards=data['maxCards'])
    db.session.add(game)
    for team_data in data['teams']:
        team = Team(name=team_data.get('name'))
        team.game = game
        db.session.add(team)
        for player_data in team_data.get('players', []):
            player = Player(name=player_data['name'])
            player.team = team
            db.session.add(player)
    db.session.commit()
    return game.serialize()


@app.route("/api/games", methods=['GET'])
def games():
    return {'games': [g.serialize() for g in Game.query.all()]}


@app.route("/api/games/<string:game_id>", methods=['GET'])
def game(game_id):
    return Game.query.get_or_404(game_id).serialize()


# TODO: only participants of the game should allow sending cards
@app.route("/api/games/<string:game_id>/cards", methods=['POST', 'GET'])
def cards(game_id):
    if request.method == 'POST':
        data = request.json
    else:
        data = request.args
    game = Game.query.get_or_404(game_id)
    cards = Card.query.filter_by(game_id=game_id, player_id=data['playerId'])
    if request.method == 'POST':
        cards.delete()
        cards = []
        for card_data in data['cards']:
            text = card_data.get('text', '').strip()
            if not text:
                continue
            card = Card(game_id=game_id, text=text, player_id=data['playerId'])
            cards.append(card)
            db.session.add(card)
        db.session.commit()
    return {"cards": [c.serialize() for c in cards], "max_cards": game.max_cards}


@app.route("/api/games/<string:game_id>/draw", methods=['GET'])
def draw_card(game_id):
    card = random_card(game_id)
    return {"card": card and card.serialize()}


@app.route("/api/games/<string:game_id>/guess", methods=['POST'])
def guess(game_id):
    data = request.json
    print(data)
    card = Card.query.get_or_404(data['cardId'])
    card.guessed_by = data['playerId']
    next_card = random_card(game_id)
    db.session.commit()
    return {"card": next_card and next_card.serialize()}


@app.route("/api/games/<string:game_id>/next_round", methods=['POST'])
def next_round(game_id):
    game = Game.query.get_or_404(game_id)
    results = []
    for team in game.teams:
        results.append({"team": team.serialize("id", "name", "guessedCount")})
    Card.query.filter_by(game_id=game_id).update({'guessed_by': None})
    db.session.commit()
    return {"results": results, "game": game.serialize()}


def random_card(game_id):
    cards = Card.query.filter_by(game_id=game_id, guessed_by=None).all()
    if not cards:
        return None
    return random.choice(cards)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
