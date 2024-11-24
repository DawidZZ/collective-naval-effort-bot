from sqlalchemy.orm import Session
from app.model import Player, Resource, Deposit, AllowedRole
from sqlalchemy import func, desc


def delete_resource(session: Session, resource_id: int):
    resource = session.query(Resource).filter(
        Resource.id == resource_id).first()
    session.delete(resource)
    session.commit()
    return resource
