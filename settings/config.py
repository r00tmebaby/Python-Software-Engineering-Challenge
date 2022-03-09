# Database Configuration
# SQL alchemy database type. Current setup is with sqlite3db.

DATABASE_URL = "postgresql://postgres:r00tme123@localhost:5432/bidnamic"

# Where the FastAPI will run
HOST = "0.0.0.0"
PORT = 80

# Swagger Documentation
API = {"title": "Bidamic 🚀"}

# General
ROOT_PATH = "/api/v1"
LANGUAGE = "EN"
DEFAULT_DATE_FORMAT = "%b %d %Y %H:%M:%S"

# Token Generator
SECRET_KEY = "0F8C3BAD9497C008840623F91D0CE16F5AA6E54A8B868448E80C7D9702455D2CDB463D38A8B47675490FC8E0713C11141F18CFA0DA8D4CDDC028807AD7A57186"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

# Error codes
BAD_REQUEST = 400000  # 400 -> Actual HTTP Error Code | 000 -> Our API Ref.
INVALID_CREDENTIALS = 400001
INVALID_EMAIL = 400002
INVALID_REFRESH_TOKEN = 400003
MISSING_USER_ID = 400004
INVALID_USER_ID = 400005
USER_ALREADY_VERIFIED = 400006
INVALID_USER_TOKEN = 400007
DUPLICATE_EMAIL = 400008
USERNAME_TOO_SHORT = 400009
USERNAME_TOO_LONG = 4000010
USERNAME_INVALID_CHARACTERS = 400011
PASSWORD_TOO_SHORT = 400012
PASSWORD_INVALID = 400013
USER_ALREADY_LOGGED = 400014

CONTACT_ADMINISTRATOR = 405000

UNAUTHORIZED = 401000
INVALID_CLIENT = 401001

FORBIDDEN = 403000
NOT_FOUND = 404000

# Languages in JSON Format
ERROR_DESCRIPTIONS_EN = {

    BAD_REQUEST: "Bad request",
    UNAUTHORIZED: "User not logged in",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Resource does not exist",

    MISSING_USER_ID: "Missing user ID",

    DUPLICATE_EMAIL: "Email already registered",

    USERNAME_TOO_SHORT: "Username needs a minimum of 3 characters",
    USERNAME_TOO_LONG: "Username cannot exceed 15 characters",
    USERNAME_INVALID_CHARACTERS: "Username can only have letters and numbers",
    USER_ALREADY_VERIFIED: "User already verified",

    PASSWORD_TOO_SHORT: "Password needs a minimum of 8 characters",
    PASSWORD_INVALID: "Password must contain at least 1 letter, 1 number, and 1 special character",

    INVALID_USER_TOKEN: "Invalid user or token",
    INVALID_CLIENT: "Invalid OAuth application client",
    INVALID_USER_ID: "Invalid user ID",
    INVALID_CREDENTIALS: "Invalid username and/or password",
    INVALID_REFRESH_TOKEN: "Invalid refresh token",
}


"""
    "title": "Bidnamic - API Documentation 🚀",
    "license": {
        "name": "Uvicorn",
        "url": "https://www.uvicorn.org/",
    },
    "description": "Maximise revenue and profitability from Google Shopping with Bidnamic’s advanced machine 
    learning and deep human expertise."

<hr>

## 🔒 Authentication
You will be able to:

* **Login** - login using a valid email and password
* **Logout** - to logout from the system 

## 🙋 Users
Only for registered users:
* **View and edit** personal information

<hr>
"""
