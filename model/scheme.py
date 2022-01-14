import decimal
from dataclasses import dataclass
from typing import Literal


@dataclass
class Merchant:
	login: str
	password: Literal['PASSWORD', 'PASSWORD2']


@dataclass
class Order:
	number: int
	description: str
	cost: decimal
