from .app import get_application
from routers.setup import include_routers

__all__ = ["get_application", "include_routers"]
