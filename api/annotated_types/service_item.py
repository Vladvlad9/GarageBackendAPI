from typing import Annotated

from fastapi import Path
from pydantic import UUID4

__all__ = ["ServiceItemID"]

ServiceItemID = Annotated[
    UUID4,
    Path(
        title="ServiceItemID ID",
        description="<p>ServiceItemID unique identifier</p>",
        alias="id",
    ),
]
