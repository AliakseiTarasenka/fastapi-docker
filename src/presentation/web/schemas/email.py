from typing import List

from pydantic import BaseModel
from pydantic.networks import NameEmail


class EmailModel(BaseModel):
    addresses: List[NameEmail]
