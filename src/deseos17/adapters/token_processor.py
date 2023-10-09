from datetime import timedelta, datetime
from typing import Literal

from jose import jwt, JWTError

from deseos17.domain.exceptions.access import AuthenticationError
from deseos17.domain.models.user_id import UserId

Algorithm = Literal[
    "HS256", "HS384", "HS512",
    "RS256", "RS384", "RS512",
]


class JwtTokenProcessor:
    def __init__(
            self,
            secret: str,
            expires: timedelta,
            algorithm: Algorithm,
    ):
        self.secret = secret
        self.expires = expires
        self.algorithm = algorithm

    def create_access_token(
            self,
            user_id: UserId,
    ) -> str:
        to_encode = {"sub": str(user_id)}
        expire = datetime.utcnow() + self.expires
        to_encode["exp"] = expire
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm,
        )

    def validate_token(self, token: str) -> UserId:
        try:
            payload = jwt.decode(
                token, self.secret, algorithms=[self.algorithm],
            )
        except JWTError:
            raise AuthenticationError

        try:
            return UserId(int(payload["sub"]))
        except ValueError:
            raise AuthenticationError
