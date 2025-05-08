# # # =======================
# # # Project : DataGuard Repository
# # # Author  : Alamanda Team
# # # File    : app/model/dbtschema.py
# # # Function: BaseModel DataGuard Contract to DBT Schema
# # # =======================

from pydantic import BaseModel
from typing import List, Optional, Union

# # # ----------------------- Model Hierarchy
# # # Examples
# # # ----------------------- Model Hierarchy


class Dbtschemas(BaseModel):
    type: Optional[str]
    data: Optional[str]
