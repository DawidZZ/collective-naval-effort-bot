from sqlalchemy.orm import Session
from app.model import Player, Resource, Deposit, AllowedRole
from sqlalchemy import func, desc


def get_leaderboard(session: Session, resource_name: str, limit: int = 10):
    result = (
        session.query(
            Player.nickname,
            func.sum(Deposit.amount).label('total_deposit')
        )
        .join(Deposit, Player.id == Deposit.player_id)
        .join(Resource, Deposit.resource_id == Resource.id)
        .filter(Resource.name == resource_name)
        .group_by(Player.id, Player.nickname)
        .order_by(desc('total_deposit'))
        .limit(limit)
        .all()
    )

    return result


def get_amount_of_player_deposit(session: Session, nickname: str, resource_name: str):
    result = (
        session.query(
            func.sum(Deposit.amount).label('total_deposit')
        )
        .join(Player, Player.id == Deposit.player_id)
        .join(Resource, Resource.id == Deposit.resource_id)
        .filter(Player.nickname == nickname)
        .filter(Resource.name == resource_name)
        .group_by(Player.id)
        .first()
    )

    return result


def get_griefers(session: Session):
    result = (
        session.query(
            Player.nickname,
            Resource.name,
            func.sum(Deposit.amount).label('total_amount')
        )
        .join(Player, Player.id == Deposit.player_id)
        .join(Resource, Resource.id == Deposit.resource_id)
        .group_by(Player.id, Player.nickname, Resource.id, Resource.name)
        .having(func.sum(Deposit.amount) < 0)
        .all()
    )

    return result


def find_player_by_nickname(session: Session, nickname: str):
    return session.query(Player).filter(Player.nickname == nickname).first()


def find_resource_by_name(session: Session, name: str):
    return session.query(Resource).filter(Resource.name == name).first()


def get_all_resources(session: Session):
    return session.query(Resource).all()
