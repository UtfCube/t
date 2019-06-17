from app.models import RevokedTokenModel
from flask_jwt_extended import create_access_token, create_refresh_token

class TokenService:
    def revoke_token(self, jti):
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.save_to_db()
    
    def create_access_token(self, identity):
        return create_access_token(identity=identity)

    def create_refresh_token(self, identity):
        return create_refresh_token(identity=identity)
