# Messaging App Backend



## Features 
---
* Users can create accounts and login in the system.

* One users can send a message to other with username.

* Users can access their past messages.

* One user can block/ublock the other with username.

* User login activity are kept on database.

* All errors are kept on database and critical details are hidden from users.

## Requirements 
---
###### Download & Install Docker Dashboard Application
> https://docs.docker.com/desktop/
###### Install Docker Compose
```
pip install docker-compose
```
## Start Using
---
###### Install Messaging App
```
git clone https://github.com/aykutyrdm/messaging-backend.git
```
###### Change Directory
```
cd messaging-backend
``` 
###### Build 
```
docker-compose build
```
###### Test & Run 
```
docker-compose up
```
###

# API Documentation

## Authentication
---
### Register 
```
POST /api/auth/register HTTP/1.1
```
###### Request
```
POST http://localhost:8000/api/auth/register
Content-Type: application/json
Accept: application/json

{
    "username" : "foo",
    "email" : "foo@messaging.com",
    "password" : "123"
}
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "user": {
        "id": 3,
        "username": "foo",
        "email": "foo@messaging.com"
    },
    "token": "0b62672c8575053a9c9a1b0fc5d2e10f383308213e41f6948dc75d9571cdc765"
}
```
###### Failed Response
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "username": [
        "A user with that username already exists."
    ]
}
```


### Login 
```
POST /api/auth/login HTTP/1.1
```
###### Request
```
POST http://localhost:8000/api/auth/login
Content-Type: application/json
Accept: application/json

{
	"username" : "foo",
	"password" : "123"	
}
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "user": {
        "id": 3,
        "username": "foo",
        "email": "foo@messaging.com"
    },
    "token": "ba25f4eecb64fb7a1e0a924c83a92f2223cc55e1b2a71144fc6e5b3fb2683330"
}
```
###### Failed Response
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "non_field_errors": [
        "Invalid Credentials"
    ]
}
```
## User
---
This API uses token-based HTTP Authentication scheme. All requests should include an `Authorization` header that contains authorized user token in form of `Token <TOKEN_VALUE>`. 

### Get Authenticated User
```
GET /api/auth/user HTTP/1.1
```
###### Request
```
GET http://localhost:8000/api/auth/user
Accept: application/json
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 2,
    "username": "test",
    "email": ""
}
```
###### Failed Response
```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "detail": "Invalid token."
}
```

### Logout User 
```
POST /api/auth/logout HTTP/1.1
```
###### Request
```
POST http://localhost:8000/api/auth/logout
```
###### Successful Response
```
HTTP/1.1 204 No Content
```
## Message
---
This API uses token-based HTTP Authentication scheme. All requests should include an `Authorization` header that contains authorized user token in form of `Token <TOKEN_VALUE>`. 

### Get Message List of Authenticated User 
```
GET /api/message HTTP/1.1
```
###### Request
```
GET http://localhost:8000/api/message
Accept: application/json
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "sent": [
        {
            "target": {
                "id": 3,
                "username": "john",
                "email": "john@gmail.com"
            },
            "content": "please contact me!",
            "timestamp": "2020-09-28T02:25:50.958294Z"
        },
        {
            "target": {
                "id": 5,
                "username": "sam",
                "email": "sam@messaging.com"
            },
            "content": "Hi there!",
            "timestamp": "2020-09-28T02:38:38.979874Z"
        }
    ],
    "received": [
        {
            "author": {
                "id": 2,
                "username": "spam",
                "email": "spam@gmail.com"
            },
            "content": "This is a spam!",
            "timestamp": "2020-09-28T02:29:18.222684Z"
        }
    ]
}
```

### Send a New Message 
```
POST /api/message HTTP/1.1
```
###### Request
```
POST http://localhost:8000/api/message
Content-Type: application/json
Accept: application/json

{
	"target" : "john",
	"content" : "please contact me!"
}
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "author": {
        "id": 4,
        "username": "foo",
        "email": "foo@gmail.com"
    },
    "target": {
        "id": 3,
        "username": "john",
        "email": "john@gmail.com"
    },
    "content": "please contact me!",
    "timestamp": "2020-09-28T02:25:50.958294Z"
}
```
###### Blocked Case Failed Response
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "detail": [
        "Operation is not allowed."
    ]
}
```


### Get Sent Message List of Authenticated User 
```
GET /api/message/sent HTTP/1.1
```
###### Request
```
GET http://localhost:8000/api/message/sent
Accept: application/json
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "target": {
            "id": 3,
            "username": "john",
            "email": "john@gmail.com"
        },
        "content": "please contact me!",
        "timestamp": "2020-09-28T02:25:50.958294Z"
    },
    {
        "target": {
            "id": 5,
            "username": "sam",
            "email": "sam@messaging.com"
        },
        "content": "Hi there!",
        "timestamp": "2020-09-28T02:38:38.979874Z"
    }
]
```

### Get Received Message List of Authenticated User 
```
GET /api/message/received HTTP/1.1
```
###### Request
```
GET http://localhost:8000/api/message/received
Accept: application/json
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "author": {
            "id": 2,
            "username": "spam",
            "email": "spam@gmail.com"
        },
        "content": "This is a spam!",
        "timestamp": "2020-09-28T02:29:18.222684Z"
    }
]
```
### Get Chat Messages of Authenticated User with Another User 
```
GET /api/message/chat HTTP/1.1
```
###### Request
```
GET http://localhost:8000/api/message/chat?target=john
Accept: application/json
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "sent": [
        {
            "content": "please contact me!",
            "timestamp": "2020-09-28T02:25:50.958294Z"
        }
    ],
    "received": [
        {
            "content": "Hi there.",
            "timestamp": "2020-09-28T05:19:20.644062Z"
        }
    ]
}
```
###### Failed Response
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "non_field_errors": [
        "Invalid Username"
    ]
}
```
### Get Daily Message List of Authenticated User
```
GET /api/message/daily HTTP/1.1
```
###### Request
```
GET http://localhost:8000/api/message/daily?date=2020-09-28
Accept: application/json
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "sent": [
        {
            "target": {
                "id": 3,
                "username": "john",
                "email": "john@gmail.com"
            },
            "content": "please contact me!",
            "timestamp": "2020-09-28T02:25:50.958294Z"
        },
        {
            "target": {
                "id": 5,
                "username": "sam",
                "email": "sam@messaging.com"
            },
            "content": "Hi there!",
            "timestamp": "2020-09-28T02:38:38.979874Z"
        }
    ],
    "received": [
        {
            "author": {
                "id": 2,
                "username": "spam",
                "email": "spam@gmail.com"
            },
            "content": "This is a spam!",
            "timestamp": "2020-09-28T02:29:18.222684Z"
        },
        {
            "author": {
                "id": 3,
                "username": "john",
                "email": "john@gmail.com"
            },
            "content": "Hi there.",
            "timestamp": "2020-09-28T05:19:20.644062Z"
        }
    ]
}
```
###### Failed Response
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "detail": [
        "Invalid Date String"
    ]
}
```
## Block
---
This API uses token-based HTTP Authentication scheme. All requests should include an `Authorization` header that contains authorized user token in form of `Token <TOKEN_VALUE>`. 
### Get Blocked User List of Authenticated User 
```
GET /api/block HTTP/1.1
```
###### Request
```
GET http://localhost:8000/api/block
Accept: application/json
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "blocked": {
            "id": 2,
            "username": "spam",
            "email": "spam@gmail.com"
        },
        "timestamp": "2020-09-28T05:46:12.445131Z"
    }
]
```

### Block a User

```
POST /api/block HTTP/1.1
```
###### Request
```
POST http://localhost:8000/api/block
Content-Type: application/json
Accept: application/json

{
	"blocked" : "spam"
}
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "prevented": {
        "id": 4,
        "username": "foo",
        "email": "foo@gmail.com"
    },
    "blocked": {
        "id": 2,
        "username": "spam",
        "email": "spam@gmail.com"
    },
    "timestamp": "2020-09-28T05:46:12.445131Z"
}
```
###### Failed Response
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "non_field_errors": [
        "Invalid Username"
    ]
}
```
### Unblock a User

```
DELETE /api/block HTTP/1.1
```
###### Request
```
DELETE http://localhost:8000/api/block
Content-Type: application/json
Accept: application/json

{
	"blocked" : "spam"
}
```
###### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

[]
```
###### Not Blocked Before Case Failed Response
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "detail": [
        "Operation is not allowed."
    ]
}
```

## Login Activities
---
This API must be called by admin users. All requests should include an `Authorization` header that contains authorized **SUPER** user token in form of `Token <TOKEN_VALUE>`.

*The credentials of initial super user created at compile time can be authenticated for token object.* 

> username: '**admin**'
>password: '**123**' 
### List All Login Activities 
```
GET /api/auth/loginactivity HTTP/1.1
```
##### Request
```
GET http://localhost:8000/api/auth/loginactivity
Accept: application/json
```
##### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 3,
        "login_IP": "172.24.0.1",
        "login_username": "foo",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "status": "F",
        "timestamp": "2020-09-28T02:23:59.559514Z"
    },
    {
        "id": 4,
        "login_IP": "172.24.0.1",
        "login_username": "spam",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "status": "S",
        "timestamp": "2020-09-28T02:28:28.816243Z"
    }
]
```
##### Failed Response
```
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
    "detail": "You do not have permission to perform this action."
}
```

## Errors
---
This API must be called by admin users. All requests should include an `Authorization` header that contains authorized **SUPER** user token in form of `Token <TOKEN_VALUE>`.

*The credentials of initial super user created at compile time can be authenticated for token object.* 

> username: '**admin**'
>password: '**123**' 
### List All Errors
```
GET /api/exception HTTP/1.1
```
##### Request
```
GET http://localhost:8000/api/exception
Accept: application/json
```
##### Successful Response
```
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 1,
        "username": "<unknown>",
        "user_IP": "172.24.0.1",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "request_method": "POST",
        "request_path": "/api/auth/user",
        "status_code": "401",
        "error_code": null,
        "error_codes": "authentication_failed",
        "timestamp": "2020-09-28T02:23:27.032159Z"
    },
    {
        "id": 8,
        "username": "foo",
        "user_IP": "172.24.0.1",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "request_method": "GET",
        "request_path": "/api/message/chat/sadsa",
        "status_code": "400",
        "error_code": null,
        "error_codes": {
            "non_field_errors": [
                "invalid"
            ]
        },
        "timestamp": "2020-09-28T04:27:38.971283Z"
]
```
##### Failed Response
```
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
    "detail": "You do not have permission to perform this action."
}
```
# Test Cases
---
## Account
> messaging-backend/messaging_app/accounts/test.py


###### Register Tests


```
Successful Registration Test
```






```
Registration Tests with Invalid Duplicated Data
```









```
Registration Test with Missing Data 
```








###### Login Tests       


```
Successful Login Tests
```







```
Login Tests with Invalid Credential
```








```
Login Tests with Missing Data
```






###### Block Tests


```
Create user objects for Blocking tests
```





```
Successful GET Block List Test
```




```
Successful POST Block Test
```






```
POST Block Test with client Blocked Field
```








```
POST Block Test with Invalid Blocked Field
```








```
POST Block Test with dublicated Blocked Field
```









```
POST Block Test with Missing Blocked Field
```








```
Successful Delete Block Test
```







```
Delete Not existing Block Test
```






```
Delete Block Test with client Blocked Field
```






```
Delete Block Test with Invalid Blocked Field
```






```
Delete Block Test with Missing Blocked Field
```






###### User Tests


```
Create user objects for User tests
```




```
Successful GET Authenticated User Test
```





###### Permission Tests


```
GET Not Authenticated User Test
```




```
Forbidden GET Login Activities List Test (only admin users)
```

## Message
> messaging-backend/messaging_app/message/test.py



###### Message Tests


```
Create user object for Sent Messages tests
```





```
Successful GET Messages Test
```




```
Successful POST Message Response Test
```




```
POST Message Test with Blank Data
```








```
POST Message Test with Invalid Data
```








```
POST Message Test with Client Data
```








```
POST Message Test with Missing Data 
```








###### SentMessages Tests


```
Create user object for Sent Messages tests
```




```
Successful GET Sent Message List Test
```



###### ReceivedMessages Tests


```
Create user object for Received Messages tests
```




```
Successful GET Received Message List Test
```



###### Chat Tests


```
Create user objects for Chat Messages Tests
```





```
Successful GET Chat Messages
```




```
GET Chat Messages with Invalid Query String
```






```
GET Chat Messages with Missing Query String
```





###### DailyMessages Tests


```
Create user objects for Daily Messages Tests
```




```
Successful GET Daily Messages
``` 




```
GET Daily Messages with Invalid Query Date String
```






```
GET Daily Messages with Missing Query Date String
```





###### Permission Tests


```
GET Not Authenticated User Messages Test
```






```
GET Not Authenticated User received Messages Test
``` 






```
GET Not Authenticated User Sent Messages Test
``` 






```
GET Not Authenticated User chat Messages Test
``` 






```
GET Not Authenticated User daily Messages Test
``` 
## Message
> messaging-backend/messaging_app/message/test.py



###### Permission Tests

```
Forbidden GET Expception List Test (only admin users)
```

