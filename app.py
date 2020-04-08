import random

import sqlalchemy as sa
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = 'game'

    id = sa.Column(sa.Integer, primary_key=True)
    card_count = sa.Column(sa.Integer, nullable=False)
    cards = relationship('Card', backref="game")
    teams = relationship('Team', backref="game")

    def serialize(self, *keys):
        if not keys:
            keys = ['id', 'teams', 'card_count']
        data = {}
        for key in keys:
            if key == 'id':
                data[key] = self.id
            if key == 'teams':
                data[key] = [t.serialize() for t in self.teams]
            if key == 'cards':
                data[key] = [c.serialize() for c in self.cards]
            if key == 'card_count':
                data[key] = self.card_count
        return data


class Team(db.Model):
    __tablename__ = 'team'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    game_id = sa.Column(sa.Integer, sa.ForeignKey('game.id'), nullable=False)
    players = relationship('Player', backref="team")

    def serialize(self, *keys):
        if not keys:
            keys = ["id", "name", "players"]
        data = {}
        for key in keys:
            if key == "id":
                data[key] = self.id
            if key == "name":
                data[key] = self.name
            if key == "players":
                data[key] = [p.serialize() for p in self.players]
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
            keys = ['id', 'name']
        data = {}
        for key in keys:
            if key == 'id':
                data[key] = self.id
            if key == 'name':
                data[key] = self.name
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
            keys = ["id", "text", "guessed_by"]
        data = {}
        for key in keys:
            if key == "id":
                data[key] = self.id
            if key == "text":
                data[key] = self.text
            if key == "guessed_by":
                data[key] = self.guesser and self.guesser.serialize()
        return data


@app.route("/games", methods=["PUT"])
def new_game():
    data = request.json
    game = Game(card_count=data['card_count'])
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


@app.route("/games/<string:game_id>", methods=['GET'])
def game(game_id):
    return Game.query.get_or_404(game_id).serialize()


@app.route("/games/<string:game_id>/cards", methods=['POST'])
def add_cards(game_id):
    data = request.json
    Card.query.filter_by(game_id=game_id, player_id=data['player_id']).delete()
    cards = []
    for card_data in data['cards']:
        card = Card(game_id=game_id, text=card_data['text'], player_id=data['player_id'])
        cards.append(card)
        db.session.add(card)
    db.session.commit()
    return {"cards": [c.serialize() for c in cards]}


@app.route("/games/<string:game_id>/draw", methods=['GET'])
def draw_card(game_id):
    card = random_card(game_id)
    return {"card": card and card.serialize()}


@app.route("/games/<string:game_id>/guess", methods=['POST'])
def guess(game_id):
    content = request.json
    card = Card.query.get_or_404(content['card_id'])
    card.guessed_by = content['player_id']
    next_card = random_card(game_id)
    db.session.commit()
    return {"card": next_card and next_card.serialize()}


@app.route("/games/<string:game_id>/reset", methods=['GET'])
def reset(game_id):
    game = Game.query.get_or_404(game_id)
    results = []
    for team in game.teams:
        guessed = Card.query.join(Card.guesser).filter(Player.team_id == team.id)
        results.append({"team": team.serialize("id", "name"), "guessed": [c.serialize() for c in guessed]})
    Card.query.filter_by(game_id=game_id).update({'guessed_by': None})
    db.session.commit()
    return {"results": results}


def random_card(game_id):
    cards = Card.query.filter_by(game_id=game_id, guessed_by=None).all()
    if not cards:
        return None
    return random.choice(cards)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
