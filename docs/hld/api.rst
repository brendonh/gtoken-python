Mobile API
==========

The API listing given here is not intended to be comprehensive. It is intended to give a general structure and address some specific decisions, but other API calls may be added and those given here may be expanded.

.. contents::



Versioning
----------

Every API will include a version number in its URL, e.g.:

* ``/api/1/login``
* ``/api/2/login``

These multiple versions will have separate implementations in the application, and old versions will be kept available for as long as possible. 

An API call can be *extended* without increasing its version number. This usually means adding new optional fields, and modifying the API implementation to use them only if available. The call must still work as expected if the new fields are not present.

If an API call must be changed in a way that breaks existing clients, it should be given a new version.

Each API call may have its own version numbers. The "current" API document for app developers should use the latest version of each call, and these must always be compatible with each other. So, if a new version of one API breaks existing versions of other APIs, those APIs should be given new, compatible versions at the same time (and this should be noted in the documentation).


Common Data Structures
----------------------

Profile
```````

A JSON object representing a customer's account information, with the following keys:

================= ====== =====================================
Key               Type   Notes
================= ====== =====================================
``nickname``      string
``email``         string
``gender``        string
``vip``           string "standard", "gold", or null
``coins``         float  Available GCoin balance
================= ====== =====================================

API Calls
---------

``POST /account/register``
``````````````````````````

Used to *explicitly* register a customer account from a mobile app, meaning that the user has indicated they have no existing account, and filled out a registration form in-app.

**Endpoint**: ``/api/1/account/register``

**Request**:

================= ====== ==============================
Parameter         Type   Notes
================= ====== ==============================
``username``      string Must be unique
``password``      string 
``email``         string
``nickname``      string
``gender``        string "male", "female", or "other"
``game_id``       guid  
``referral_code`` string
================= ====== ==============================

**Response (JSON)**:

================= ====== ==============================
Key               Type   Notes
================= ====== ==============================
``success``       bool
``message``       string Human-readable error message
================= ====== ==============================


``POST /account/login-password``
````````````````````````````````

Logs a user in via their GToken username and password. The account must already exist.

**Endpoint**: ``/api/1/account/login-password``

**Request**:

================= ====== ==============================
Parameter         Type   Notes
================= ====== ==============================
``username``      string
``password``      string
``game_id``       guid
================= ====== ==============================

**Response (JSON)**:

================= ======= ================================
Key               Type    Notes
================= ======= ================================
``success``       bool
``message``       string  Human-readable error message
``session``       string  Access token for later requests
``profile``       profile See ``profile`` definition above
================= ======= ================================


``POST /account/login-oauth``
`````````````````````````````

Log in via a third-party OAuth provider, e.g. Facebook. Note that this API will **implicitly register** the user if an account does not already exist, using user information retrieved from the third-party provider.

**Endpoint**: ``/api/1/account/login-oauth``

**Request**:

================= ====== ==========================================
Parameter         Type   Notes
================= ====== ==========================================
``service``       string Identifies the third-party service used
``token``         string Access token returned by third party
``game_id``       guid
================= ====== ==========================================

**Response (JSON)**

================= ======= ================================
Key               Type    Notes
================= ======= ================================
``success``       bool
``message``       string  Human-readable error message
``session``       string  Access token for later requests
``profile``       profile See ``profile`` definition above
================= ======= ================================


``POST /account/connect-password``
``````````````````````````````````

Adds a password-based login to an existing account, which must not have one already (i.e. it has only OAuth login).

**Endpoint**: ``/api/1/account/connect-password``

**Request**:

================= ====== ==========================================
Parameter         Type   Notes
================= ====== ==========================================
``session``       string Access token returned by previous login
``game_id``       guid
``username``      string
``password``      string
================= ====== ==========================================

**Response (JSON)**

================= ======= ================================
Key               Type    Notes
================= ======= ================================
``success``       bool
``message``       string  Human-readable error message
================= ======= ================================


``POST /account/connect-oauth``
```````````````````````````````

Adds an OAuth login to an existing account. One account may have multiple OAuth logins.

**Endpoint**: ``/api/1/account/connect-oauth``

**Request**:

================= ====== ==========================================
Parameter         Type   Notes
================= ====== ==========================================
``session``       string Access token returned by previous login
``game_id``       guid
``service``       string Identifies the third-party service used
``token``         string Access token returned by third party
================= ====== ==========================================

**Response (JSON)**

================= ======= ================================
Key               Type    Notes
================= ======= ================================
``success``       bool
``message``       string  Human-readable error message
================= ======= ================================

``GET /account/profile``
````````````````````````

Returns profile of logged-in user. May be used to check whether a session token is still valid.

**Endpoint**: ``/api/1/account/profile``

**Request**

================= ====== ==========================================
Parameter         Type   Notes
================= ====== ==========================================
``session``       string Access token returned by previous login
================= ====== ==========================================

**Response (JSON)**

================= ======= ================================
Key               Type    Notes
================= ======= ================================
``success``       bool
``message``       string  Human-readable error message
``profile``       profile See ``profile`` definition above
================= ======= ================================


``POST /account/profile``
`````````````````````````

Updates profile of logged-in user. Parameters may be omitted, and those fields will be unchanged.

**Endpoint**: ``/api/1/account/profile``

**Request**

================= ====== ==========================================
Parameter         Type   Notes
================= ====== ==========================================
``session``       string Access token returned by previous login
``email``         string
``nickname``      string
``gender``        string "male", "female", or "other"
================= ====== ==========================================

**Response (JSON)**

================= ======= ================================
Key               Type    Notes
================= ======= ================================
``success``       bool
``message``       string  Human-readable error message
================= ======= ================================


``GET /balance``
````````````````

Gets a user's credit balance for a given game.

**Endpoint**: ``/api/1/balance``

**Request**

================= ====== ==========================================
Parameter         Type   Notes
================= ====== ==========================================
``session``       string Access token returned by previous login
``game_id``       guid
================= ====== ==========================================

**Response (JSON)**

================= ======= ================================
Key               Type    Notes
================= ======= ================================
``success``       bool
``message``       string  Human-readable error message
``balance``       int    
================= ======= ================================


``POST /spend``
```````````````

Deducts credits from a user's balance for a given game.

**Endpoint**: ``/api/1/account/profile``

**Request**

================= ====== ==========================================
Parameter         Type   Notes
================= ====== ==========================================
``session``       string Access token returned by previous login
``game_id``       guid
``quantity``      int    Number of tokens to deduct
================= ====== ==========================================

**Response (JSON)**

================= ======= =================================
Key               Type    Notes
================= ======= =================================
``success``       bool
``message``       string  Human-readable error message
``balance``       int     Remaining balance after deduction
================= ======= =================================
