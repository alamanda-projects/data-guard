# # # =======================
# # # Project : Data Contract Repository 2.0
# # # Author  : Hani Perkasa
# # # File    : app/model/users.py
# # # Function: baseModel pelengkap utils.py
# # # =======================

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union
import datetime
from email_validator import validate_email, EmailNotValidError

# # # ----------------------- Model Hierarchy
# # # CreateUser
# # # ----------------------- Model Hierarchy

# Model untuk data user lengkap
class UserCreate(BaseModel):
    username: str
    name: str
    password: str
    group_access: str
    data_domain: str
    is_active: bool
