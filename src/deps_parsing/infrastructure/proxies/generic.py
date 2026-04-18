from deps_parsing.extras.rest_client import AbstractRESTClient
from deps_parsing.extras.rest_client.deps_token_auth import DEPSTokenAuth
from deps_parsing.infrastructure.access_management import user

__all__ = ["GenericProxy"]


class GenericProxy(AbstractRESTClient):
    def _set_authentication(self) -> None:
        self._session.auth = DEPSTokenAuth(user)
