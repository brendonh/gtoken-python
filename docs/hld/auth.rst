Authentication
==============

Accounts
--------

We will have three separate sets of user accounts:

 * **Customer** accounts (mobile API and customer website)
 * **Admin** accounts (admin web app)
 * **Partner** accounts (partner API)

Each set of accounts will be stored separately in the database (since they have different associated information). All passwords will be hashed using bcrypt_.

For customer accounts, no further access control is necessary. Each customer has identical access to their own data.

Admin accounts will specify a single *role* for each user. Based on the requirements document these roles are currently expected to be *Admin*, *Support*, *Accounting*, and *Studio*. The *Studio* role will further specify which studio they administer.

Access control for partner accounts, if any, is not yet defined.

.. _bcrypt: https://pypi.python.org/pypi/bcrypt/1.0.2


Logins
------

Each sub-application will have its own authentication mechanism:

 * **Mobile API**: OAuth2 against the customer accounts
 * **Customer website**: OAuth2 against customer accounts, cookie sessions
 * **Admin web app**: Password login against admin accounts, cookie sessions
 * **Partner API**: Password-based OAuth2 against the partner accounts

We will use Flask's oauthlib_ integration to act as both an OAuth2 provider (for the mobile and partner APIs) and client (for customer login via Facebook, etc).

.. _oauthlib: https://flask-oauthlib.readthedocs.org/en/latest/


Customer Registration
---------------------

Customer account registration can happen in two ways:

* **Explicit** registration, by filling out the registration form on either the customer website or mobile app.
* **Implicit** registration, by logging in via a third-party OAuth2 provider (e.g. Facebook) as a user who does not already have an account.

A customer may also **connect** a new login method to an existing account. This is discussed further in the API section.


Admin and Partner Account Management
------------------------------------

The admin and partner accounts cannot be directly registered. They must be created via the admin web app.


