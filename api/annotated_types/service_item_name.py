from typing import Annotated

from fastapi import Path
from pydantic import UUID4

__all__ = ["ItemNameID"]

ItemNameID = Annotated[
    UUID4,
    Path(
        title="Service Item Name ID",
        description="<p>ServiceItemNameID unique identifier</p>",
        alias="id",
    ),
]
