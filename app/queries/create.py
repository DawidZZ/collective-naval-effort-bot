from sqlalchemy.orm import Session
from app.model import Player, Resource, Deposit, AllowedRole
from sqlalchemy import func, desc


def add_player(session: Session, nickname: str):
    player = Player(nickname=nickname)
    session.add(player)
    session.commit()
    return player


def add_resource(session: Session, name: str):
    resource = Resource(name=name)
    session.add(resource)
    session.commit()
    return resource


def add_deposit(session: Session, player_id: int, resource_id: int, amount: int):
    deposit = Deposit(player_id=player_id,
                      resource_id=resource_id, amount=amount)
    session.add(deposit)
    session.commit()
    return deposit


def find_or_add_player(session: Session, nickname: str):
    player = session.query(Player).filter(Player.nickname == nickname).first()
    if player is None:
        player = add_player(session, nickname)
    return player
