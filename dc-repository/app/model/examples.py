# # # =======================
# # # Project : Data Contract Repository 2.0
# # # Author  : Hani Perkasa
# # # File    : app/model/exmaples.py
# # # Function: baseModel pelengkap all.py
# # # =======================

from pydantic import BaseModel
from typing import List, Optional, Union

# # # ----------------------- Model Hierarchy
# # # Examples
# # # ----------------------- Model Hierarchy


class Examples(BaseModel):
    type: Optional[str]
    data: Optional[str]
