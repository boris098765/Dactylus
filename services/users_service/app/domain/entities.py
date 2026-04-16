from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


class RSLStatusEnum(str, Enum):
    LEARNER    = "learner"
    NATIVE     = "native"
    TRANSLATER = "translater"

@dataclass
class UserDTO:
    id: int
    username: str
    email: str

    is_verified: bool
    rsl_status: RSLStatusEnum
    created_at: datetime