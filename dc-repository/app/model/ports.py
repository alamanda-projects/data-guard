# # # =======================
# # # Project : Data Contract Repository 2.0
# # # Author  : Hani Perkasa
# # # File    : app/model/ports.py
# # # Function: baseModel pelengkap all.py
# # # =======================

from pydantic import BaseModel
from typing import List, Optional, Union

# # # ----------------------- Model Hierarchy
# # # Ports
# # #  |- PortsProperties
# # # ----------------------- Model Hierarchy

class PortsProperties(BaseModel):
    property: str
    value: Union[str, int]

class Ports(BaseModel):
    object: str
    properties: List[PortsProperties] # -> merujuk ke class PortsProperties