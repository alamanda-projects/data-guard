# Documentation

## Login

Default user :
| Username | Password | Keterangan |
| -------- | -------- | -------- |
| root | DCr00t!! | Superuser |
| admin | admiN!23 | Admin User |
| user | useR!234 | User ASIK |
| user2 | useR!234 | User SSM |

Pada saat login postman mengirimkan username dan password melalui parameter `username` dan `password` pada header menggunakan method POST.

Output :
```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ99eyJ1c3IiOiJ1c2VyIiwidHlwIjoidXNlciIsImx2bCI6InVzZXIiLCJzdHMiOnRydWUsInRpbSI6ImFzaWsiLCJleHAiOjE3MDg5NDY3NzJ9.GnFcL6COpySWvHBetW7luenOeU4yIwp44eTl9GCYTok",
    "token_type": "Bearer"
}
```

## Add User
Dengan menggunakan user `root` silahkan buat sebuah user untuk data domain tertentu dengan menggunakan `body` messages sbb :
```
{
  "username": "fulan",
  "password": "R4H4s!@",
  "name": "Fulan bin Fulan",
  "group_access": "user",
  "data_domain": "Domain X",
  "is_active": true
}
```
menggunakan method POST ke `http://localhost:8888/user/create`

Jika berhasil maka akan mendapat response sbb : 
```
{
    "message": "User created successfully"
}
```

## Add Data Contract