# # # =======================
# # # Project : DataGuard Repository
# # # Author  : Alamanda Team
# # # File    : app/model/exmaples.py
# # # Function: BaseModel DataGuard Contract - Example section
# # # =======================

from pydantic import BaseModel
from typing import List, Optional, Union

# # # ----------------------- Model Hierarchy
# # # Examples
# # # ----------------------- Model Hierarchy


class Examples(BaseModel):
    type: Optional[str]
    data: Optional[str]
