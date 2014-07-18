Database Schema
===============

The schema listing given here is not intended to be comprehensive. It is intended to give a general structure and address some specific decisions, but other tables may be added and those given here may be expanded.

Tables used purely by the OAuth2 provider (e.g. ``oauth2_grant``, ``oauth2_token``) are also omitted. See the documentation for `OAuth2 Servers`_.

.. _`OAuth2 Servers`: https://flask-oauthlib.readthedocs.org/en/latest/oauth2.html

.. contents::

Accounts
--------

``customer_account``
````````````````````

============================= ============= ====================================
Column                        Type          Notes
============================= ============= ====================================
``id``                        serial        Primary Key
``nickname``                  varchar(40)   Display name
``email``                     varchar(64)   Unique
``gender``                    varchar(8)    ``male``, ``female``, ``other``
``avatar_filename``           text
``vip``                       varchar(16)   ``standard``, ``gold``, or ``NULL``
``coins``                     decimal(8, 2) GCoin balance
``referral_code``             varchar(64)   Unique
``inviter_referral_code``     varchar(64)   References ``customer_account(referral_code)``
``created_at``                timestamp
``updated_at``                timestamp
``last_login_at``             timestamp
``is_active``                 boolean       Default False
``is_archived``               boolean       Default False
============================= ============= ====================================


``customer_login_password``
```````````````````````````

======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``customer_account_id`` int          References ``customer_account(id)``. Unique (only one password login per account)
``username``            varchar(32)  Unique
``email``               varchar(64)  Unique
``password``            varchar(40)  BCrypt hash of password
======================= ============ ====================================


``customer_login_oauth``
````````````````````````
======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``customer_account_id`` int          References ``customer_account(id)``
``service``             varchar(32)  Third-party OAuth service used
``identity``            text         Identity in service
======================= ============ ====================================

**Constraint**: Unique on (``customer_account_id``, ``service``).


``admin_account``
`````````````````

======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``username``            varchar(32)  Unique
``password``            varchar(40)  BCrypt hash of password
``email``               varchar(64)
``role``                varchar(16)  ``admin``, ``support``, ``accounting``, ``studio``
``studio_id``           integer      References ``studio(id)``. Nullable.
``created_at``          timestamp
``updated_at``          timestamp
``last_login_at``       timestamp
``is_active``           boolean
``is_archived``         boolean
======================= ============ ====================================


``partner_account``
```````````````````

======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``name``                varchar(32)
``client_id``           varchar(40)  OAuth2 Client ID
``client_secret``       varchar(55)  OAuth2 Client Secret
``redirect_uris``       text         OAuth2 redirect URLs
``default_scopes``      text         OAuth2 default scopes
======================= ============ ====================================


Games
-----

``studio``
``````````

======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``name``                varchar(32)
======================= ============ ====================================

``game``
````````
======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``studio_id``           integer      References ``studio(id)``
``guid``                uuid         Used as game_id in APIs. Secret.
``name``                varchar(128)
``description``         text
======================= ============ ====================================

``credit_type``
``````````
======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial       Primary Key
``game_id``             integer      References ``game(id)``
``name``                varchar(32)
``label``               varchar(32)  Display name of credit
``exchange_rate``       integer      Exchange rate from coins to credits
``icon_filename``       text
======================= ============ ====================================

``package``
```````````
======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial       Primary Key
``game_id``             integer      References ``game(id)``
``credit_type_id``      integer      References ``credit_type(id)``
``name``                varchar(32)
``label``               varchar(32)  Display name of package
``credit_value``        integer
``gcoin_value``         decimal(8,2)               
``icon_filename``       text
======================= ============ ====================================


Credits
-------

``credit_balance``
``````````````````
======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``credit_type_id``      integer      References ``credit_type(id)``
``customer_account_id`` integer      References ``customer_account(id)``
``balance``             integer      Balance in game credits
======================= ============ ====================================

**Constraint**: Unique on (``credit_type_id``, ``customer_account_id``)


Transactions
------------

``coin_transaction``
````````````````````

Records all coin-related transactions, with associated metadata. A user's coin balance can be completely reconstructed by a ``SUM(amount)`` query over this table.

======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``customer_account_id`` integer      References ``customer_account(id)``
``reciever_account_id`` integer      References ``customer_account(id)``. Nullable
``amount``              decimal(8,2) Change in coin balance
``partner_account_id``  integer      References ``partner_account(id)``. Nullable
``game_id``             integer      References ``game(id)``. Nullable
``credit_type_id``      integer      References ``credit_type(id)``. Nullable
``package_id``          integer      References ``package(id)``. Nullable
``created_at``          timestamp
``description``         text         Extra human-readable information
======================= ============ ====================================


``credit_transaction``
``````````````````````
Records all credit-related transactions, with associated metadata. A user's credit balance for any game can be completely reconstructed by a ``SUM(amount)`` query over this table.

Note that a credit purchase will have a corresponding entry in ``coin_transaction``.

======================= ============ ====================================
Column                  Type         Notes
======================= ============ ====================================
``id``                  serial
``customer_account_id`` integer      References ``customer_account(id)``
``coin_transaction_id`` integer      References ``coin_transaction(id)``. Nullable.
``amount``              decimal(8,2) Change in credit balance
``game_id``             integer      References ``game(id)``
``credit_type_id``      integer      References ``credit_type(id)``     
``package_id``          integer      References ``package(id)``
``created_at``          timestamp
``description``         text         Extra human-readable information
======================= ============ ====================================
