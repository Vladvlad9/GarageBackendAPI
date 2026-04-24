from typing import Annotated

from fastapi import Path
from pydantic import UUID4

__all__ = ["CarID"]

CarID = Annotated[
    UUID4,
    Path(
        title="CarID ID",
        description="<p>CarID unique identifier</p>",
        alias="id",
    ),
]
