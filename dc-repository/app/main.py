# # # =======================
# # # Project : Data Contract Repository 2.0
# # # Author  : Hani Perkasa
# # # File    : app/main.py
# # # Function: main script
# # # =======================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from typing import Dict
from app.model.users import UserCreate
from app.core.connection import database, col_usr, col_dcr
from app.core.display import *
from app.core.hasher import Hasher
from app.core.generator import (
    cn_generator,
    create_jwt_token,
    create_private_key,
    tkn_exp,
    sa_exp,
)
from datetime import datetime, timedelta
from app.core.verificator import (
    user_verification,
    access_verification,
    access_verification_filter,
    token_verification,
    grplvlroot,
    grplvladmin,
    grplvlall,
)
from app.info.app_info import *

current_dateTime = datetime.now()

# Database declaration
usrcollection = database[col_usr]
dccollection = database[col_dcr]

# Error response
usrnotallowed = usr_403
dcnotfound = dc_404
dcnotvalid = dc_412  # # persiapan untuk validasi YAML / JSON
dc_404_notfound = HTTPException(status_code=404, detail=dcnotfound)

app = FastAPI(
    title=app_title,
    description=app_description,
    summary=app_summary,
    version=app_version,
    # terms_of_service=terms_of_service,
    contact={
        "name": app_contact_name,
        "url": app_contact_url,
        "email": app_contact_email,
    },
    license_info={
        "name": app_license_info_name,
        "url": app_license_info_url,
    },
    docs_url=None,
    redoc_url=None,
)


@app.get("/", response_class=RedirectResponse, status_code=302)
async def default_page():
    return "/welcome"


@app.get("/welcome")
async def welcome():
    content = """
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Contract Repository 2.0</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 20px;
        }

        h1 {
            color: #3366cc;
            font-size: 32px;
        }

        h2 {
            color: #009688;
            font-size: 24px;
        }

        h3 {
            color: #009688;
            font-size: 20px;
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            margin-bottom: 8px;
        }

        hr {
            border: 1px solid #ccc;
            margin: 20px 0;
        }

        a {
            color: #3366cc;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>

<body>
    <h1>Data Contract Repository 2.0</h1>
    <h2>Versi: 0.3.0 (Alpha) <br> <a href="https://gitlab.com/dto-moh/data/dto-dcr/-/blob/master/README.md?ref_type=heads&plain=0&blame=1" target="_blank">Readme.md (Panduan Penggunaan)</a></h2>
    <h3>Fitur :</h3>
    <ul>
        <li>- Manajemen User</li>
        <li>- Manajemen Data Contract</li>
    </ul>
    <h3>Pengembang :</h3>
    <p>Tim Data dari DTO Kemenkes RI</p>
    <h3>Lisensi :</h3>
    <p><a href="https://www.apache.org/licenses/LICENSE-2.0.html" target="_blank">Apache 2.0 License</a></p>
    <hr>

    <h2>Apa itu Data Contract ? ==> <a href="https://gitlab.com/dto-moh/data/dto-odcs/-/tree/master" target="_blank">Readme.md</a></h2>
    <h2>Contoh Data Contract ==> <a href="https://gitlab.com/dto-moh/data/dto-odcs/-/blob/master/examples/data-contract-example.yaml" target="_blank">data-contract.yaml</a></h2>
</body>

</html>

    """
    return HTMLResponse(content=content)


# Generate Token
@app.post("/login")
async def login_for_access_token(
    user_in_db: Dict[str, str] = Depends(user_verification)
):
    # # checking access level
    user_uname = user_in_db["username"]
    user_level = user_in_db["level"]
    user_status = user_in_db["is_active"]
    user_team = user_in_db["data_domain"]
    user_type = user_in_db["type"]
    await access_verification(user_level, user_status, grplvlall)
    # # checking access level

    user_data = {
        "usr": user_uname,
        "typ": user_type,
        "lvl": user_level,
        "sts": user_status,
        "tim": user_team,
    }

    token = create_jwt_token(user_data, tkn_exp)
    return {"access_token": token, "token_type": "Bearer"}


@app.post("/logout")
async def logout_user(current_user: dict = Depends(token_verification)):
    response = JSONResponse(content={"message": "Logout successful"})
    # response = raise HTTPException(status_code=412, detail=usr_412_uname)
    response.delete_cookie("Authorization")
    return response


# # # ======================= Users
# # # ======================= Bagian ini untuk kebutuhan manajemen user
@app.post("/user/create", tags=["user"])
async def create_user(
    user_form: UserCreate, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    await access_verification(user_level, user_status, grplvladmin)
    # # checking access level

    if not user_form.username:
        raise HTTPException(status_code=412, detail=usr_412_uname)
    if not user_form.password:
        raise HTTPException(status_code=412, detail=usr_412_pwd)
    if not user_form.name:
        raise HTTPException(status_code=412, detail=usr_412_name)
    if not user_form.group_access:
        raise HTTPException(status_code=412, detail=usr_412_level)
    if not user_form.data_domain:
        raise HTTPException(status_code=412, detail=usr_412_team)
    # if not user_form.is_active:
    #     raise HTTPException(status_code=412, detail="Status active is required")

    user_info = await usrcollection.find_one({"username": user_form.username})

    # Cek apakah user yang digunakan adalah root
    # karena hanya root yang boleh menambahkan user root lainya
    if user_level not in grplvlroot or user_status == False:
        raise HTTPException(status_code=403, detail=usrnotallowed)

    # Cek apakah sudah ada user root active
    # itupun dalam kondisi root yang ditambahkan harus mode is_active = False
    if user_form.group_access in grplvlroot and user_form.is_active == True:
        raise HTTPException(status_code=409, detail=usr_409_root)

    # Cek apakah username sudah ada
    if user_info:
        raise HTTPException(status_code=409, detail=usr_409_taken)

    # Cek apakah password terdiri dari minimal 8 char
    if len(user_form.password) < 8:
        raise HTTPException(status_code=422, detail=pwd_422_long)

    # Cek apakah password terdiri dari huruf besar, kecil, angka serta char khusus
    valid_chars = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+={}[]<>,./?;:'\""
    )
    if not any(c in valid_chars for c in user_form.password):
        raise HTTPException(status_code=422, detail=pwd_422_all)

    # Cek apakah password mengandung setidaknya satu huruf besar, satu huruf kecil, satu angka, dan satu karakter khusus
    if not any(c.isupper() for c in user_form.password):
        raise HTTPException(status_code=422, detail=pwd_422_upcase)

    if not any(c.islower() for c in user_form.password):
        raise HTTPException(status_code=422, detail=pwd_422_locase)

    if not any(c.isdigit() for c in user_form.password):
        raise HTTPException(status_code=422, detail=pwd_422_num)

    if not any(c in valid_chars for c in user_form.password if not c.isalnum()):
        raise HTTPException(status_code=422, detail=pwd_422_spc)

    # hashing password
    hashed_password = Hasher.get_password_hash(user_form.password)

    # populate user data
    user_data = {
        "username": user_form.username,
        "password": hashed_password,
        "name": user_form.name,
        "group_access": user_form.group_access,
        "data_domain": user_form.data_domain,
        "is_active": user_form.is_active,
        "type": "user",
        "created_at": current_dateTime,
    }

    # insert user
    await usrcollection.insert_one(user_data)

    return {"message": "User created successfully"}


@app.get("/sakey/create", tags=["user"])
async def create_sakey(current_user: dict = Depends(token_verification)):
    # # checking access level
    user_uname = current_user["usr"]
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    user_team = current_user["tim"]
    await access_verification(user_level, user_status, grplvlall)
    # # checking access level

    if user_level not in grplvlall or user_status == False:
        raise HTTPException(status_code=403, detail=usrnotallowed)

    clientid = cn_generator()

    user_data = {
        "cln": clientid,
        "usr": user_uname,
        "typ": "sa",
        "lvl": user_level,
        "sts": user_status,
        "tim": user_team,
    }

    privatekey = create_private_key(user_data, sa_exp)
    hashed_privatekey = Hasher.get_password_hash(privatekey)
    expire_at = datetime.utcnow() + timedelta(days=sa_exp)

    sa_data = {
        "client_id": clientid,
        "private_key": hashed_privatekey,
        "type": "sa",
        "generated_by": user_uname,
        "generated_at": current_dateTime,
        "group_access": user_level,
        "data_domain": user_team,
        "is_active": True,
        "expire_at": expire_at,
        "created_at": current_dateTime,
    }

    # insert user
    await usrcollection.insert_one(sa_data)

    return {
        "client_id": clientid,
        "private_key": privatekey,
        "generated_by": user_uname,
        "generated_at": current_dateTime,
    }


# Example route to get user data
@app.get("/user/me", response_model=dict, tags=["user"])
async def who_am_i(current_user: dict = Depends(token_verification)):
    user_uname = current_user["usr"]
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    user_team = current_user["tim"]
    await access_verification(user_level, user_status, grplvlall)
    return current_user


# Example route to get user data
@app.get("/sakey/me", response_model=dict, tags=["user"])
async def who_am_i(current_user: dict = Depends(token_verification)):
    user_uname = current_user["usr"]
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    user_team = current_user["tim"]
    await access_verification(user_level, user_status, grplvlall)
    return current_user


# # # ======================= Data Contract
# # # ======================= Bagian ini untuk kebutuhan menampilkan Data Contract tanpa filter
@app.get("/datacontract/gencn", tags=["datacontract"])
async def generate_contract_number(current_user: dict = Depends(token_verification)):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    user_uname = current_user["usr"]
    await access_verification(user_level, user_status, grplvlall)
    # # checking access level

    code = cn_generator()

    return {
        "contract_number": code,
        "generated_by": user_uname,
        "generated_at": current_dateTime,
    }


@app.post("/datacontract/add", tags=["datacontract"])
async def insert_datacontract(
    data: All, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    await access_verification(user_level, user_status, grplvladmin)
    # # checking access level

    try:
        dccollection.insert_one(data.dict())
        return {"message": "Insert Success"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/datacontract/lists", tags=["datacontract"])
async def get_datacontract(current_user: dict = Depends(token_verification)):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    await access_verification(user_level, user_status, grplvladmin)
    # # checking access level

    dclist = await display_all()

    return dclist


@app.get("/datacontract/metadata", tags=["datacontract"])
async def get_datacontract_metadata(current_user: dict = Depends(token_verification)):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    await access_verification(user_level, user_status, grplvladmin)
    # # checking access level

    dclist = await display_metadata()

    return dclist


@app.get("/datacontract/model", tags=["datacontract"])
async def get_datacontract_model(current_user: dict = Depends(token_verification)):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    await access_verification(user_level, user_status, grplvladmin)
    # # checking access level

    dclist = await display_model()

    return dclist


@app.get("/datacontract/ports", tags=["datacontract"])
async def get_datacontract_ports(current_user: dict = Depends(token_verification)):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    await access_verification(user_level, user_status, grplvladmin)
    # # checking access level

    dclist = await display_ports()

    return dclist


@app.get("/datacontract/examples", tags=["datacontract"])
async def get_datacontract_examples(current_user: dict = Depends(token_verification)):
    # # checking access level
    user_level = current_user["lvl"]
    user_status = current_user["sts"]
    await access_verification(user_level, user_status, grplvladmin)
    # # checking access level

    dclist = await display_examples()

    return dclist


# # # ======================= Data Contract filtered
# # # ======================= Bagian ini untuk kebutuhan menampilkan Data Contract berdasarkan filter contract_number
@app.get("/datacontract/filter", tags=["datacontract_filtered"])
async def get_datacontract_filter(
    contract_number: str = None, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_client = current_user.get("cln")
    user_uname = current_user.get("usr")
    user_level = current_user.get("lvl")
    user_status = current_user.get("sts")
    user_team = current_user.get("tim")
    await access_verification_filter(
        user_uname,
        user_level,
        user_status,
        grplvlall,
        user_team,
        user_client,
        contract_number,
    )
    # # checking access level

    dcfilter = await display_all(contract_number)

    return dcfilter


@app.get("/datacontract/metadata/filter", tags=["datacontract_filtered"])
async def get_datacontract_metadata_filter(
    contract_number: str = None, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_client = current_user.get("cln")
    user_uname = current_user.get("usr")
    user_level = current_user.get("lvl")
    user_status = current_user.get("sts")
    user_team = current_user.get("tim")
    await access_verification_filter(
        user_uname,
        user_level,
        user_status,
        grplvlall,
        user_team,
        user_client,
        contract_number,
    )
    # # checking access level

    dcfilter = await display_metadata(contract_number)

    return dcfilter


@app.get("/datacontract/model/filter", tags=["datacontract_filtered"])
async def get_datacontract_model_filter(
    contract_number: str = None, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_client = current_user.get("cln")
    user_uname = current_user.get("usr")
    user_level = current_user.get("lvl")
    user_status = current_user.get("sts")
    user_team = current_user.get("tim")
    await access_verification_filter(
        user_uname,
        user_level,
        user_status,
        grplvlall,
        user_team,
        user_client,
        contract_number,
    )
    # # checking access level

    dcfilter = await display_model(contract_number)

    return dcfilter


@app.get("/datacontract/ports/filter", tags=["datacontract_filtered"])
async def get_datacontract_ports_filter(
    contract_number: str = None, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_client = current_user.get("cln")
    user_uname = current_user.get("usr")
    user_level = current_user.get("lvl")
    user_status = current_user.get("sts")
    user_team = current_user.get("tim")
    await access_verification_filter(
        user_uname,
        user_level,
        user_status,
        grplvlall,
        user_team,
        user_client,
        contract_number,
    )
    # # checking access level

    dcfilter = await display_ports(contract_number)

    return dcfilter


@app.get("/datacontract/examples/filter", tags=["datacontract_filtered"])
async def get_datacontract_examples_filter(
    contract_number: str = None, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_client = current_user.get("cln")
    user_uname = current_user.get("usr")
    user_level = current_user.get("lvl")
    user_status = current_user.get("sts")
    user_team = current_user.get("tim")
    await access_verification_filter(
        user_uname,
        user_level,
        user_status,
        grplvlall,
        user_team,
        user_client,
        contract_number,
    )
    # # checking access level

    dcfilter = await display_examples(contract_number)

    return dcfilter


@app.get("/datacontract/dbtschema/filter", tags=["datacontract_filtered"])
async def get_datacontract_dbtschema_filter(
    contract_number: str = None, current_user: dict = Depends(token_verification)
):
    # # checking access level
    user_client = current_user.get("cln")
    user_uname = current_user.get("usr")
    user_level = current_user.get("lvl")
    user_status = current_user.get("sts")
    user_team = current_user.get("tim")
    await access_verification_filter(
        user_uname,
        user_level,
        user_status,
        grplvlall,
        user_team,
        user_client,
        contract_number,
    )
    # # checking access level

    dcfilter = await display_dbtschema(contract_number)

    return dcfilter