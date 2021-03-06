import pytz

from storm.locals import *

from ..utils.gtoken_time import _utcnow

from . import stormSchema

@stormSchema.versioned
class CoinTransaction(Storm):
    __storm_table__ = 'coin_transaction'
    __version__ = 'knn_1'

    id = Int(primary=True)
    
    customer_account_id = Int()
    customerAccount = Reference(customer_account_id, "CustomerAccount.id")

    reciever_account_id = Int()
    receiverAccount = Reference(reciever_account_id, "CustomerAccount.id")

    amount = Float()

    partner_account_id = Int()
    partnerAccount = Reference(partner_account_id, "PartnerAccount.id")

    game_id = Int()
    game = Reference(game_id, "Game.id")

    credit_type_id = Int()
    creditType = Reference(credit_type_id, "CreditType.id")

    package_id = Int()
    package = Reference(package_id, "Package.id")

    description = Unicode()

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=_utcnow)


@stormSchema.versioned
class CreditTransaction(Storm):
    __storm_table__ = 'credit_transaction'
    __version__ = 'knn_1'

    id = Int(primary=True)
    
    customer_account_id = Int()
    customerAccount = Reference(customer_account_id, "CustomerAccount.id")

    coin_transaction_id = Int()
    coinTransaction = Reference(coin_transaction_id, "CoinTransaction.id")

    amount = Float()

    game_id = Int()
    game = Reference(game_id, "Game.id")

    credit_type_id = Int()
    creditType = Reference(credit_type_id, "CreditType.id")

    package_id = Int()
    package = Reference(package_id, "Package.id")

    description = Unicode()

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=_utcnow)
