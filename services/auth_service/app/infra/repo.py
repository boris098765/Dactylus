from typing import Optional
from .models import CredentialsORM, TokenORM


class AuthRepository:
    def __init__(self, session):
        self.session = session

    def save_credentials(self, user_id: int, password_hash: str):
        creds = CredentialsORM(user_id=user_id, password_hash=password_hash)
        self.session.add(creds)
        self.session.commit()

    def get_credentials(self, user_id: int) -> Optional[dict]:
        creds = self.session.query(CredentialsORM).filter_by(user_id=user_id).first()
        if creds:
            return {"user_id": creds.user_id, "password_hash": creds.password_hash}
        return None

    def update_password(self, user_id: int, password_hash: str):
        creds = self.session.query(CredentialsORM).filter_by(user_id=user_id).first()
        if creds:
            creds.password_hash = password_hash
            self.session.commit()

    def save_token(self, jti: str, user_id: int, token_type: str, expires_at):
        token = TokenORM(jti=jti, user_id=user_id, token_type=token_type, expires_at=expires_at)
        self.session.add(token)
        self.session.commit()

    def get_token(self, jti: str) -> Optional[dict]:
        token = self.session.query(TokenORM).filter_by(jti=jti).first()
        if token:
            return {"jti": token.jti, "user_id": token.user_id, "revoked": token.revoked}
        return None

    def revoke_token(self, jti: str):
        token = self.session.query(TokenORM).filter_by(jti=jti).first()
        if token:
            token.revoked = True
            self.session.commit()

    def revoke_all_user_tokens(self, user_id: int):
        from sqlalchemy import and_
        self.session.query(TokenORM).filter(
            and_(TokenORM.user_id == user_id, TokenORM.revoked == False)
        ).update({"revoked": True})
        self.session.commit()