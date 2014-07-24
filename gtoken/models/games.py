import pytz, uuid

from gtoken.utils.gtoken_time import _utcnow

from . import stormSchema
from models.accounts import CustomerAccount

@stormSchema.versioned
class Studio(object):
    __storm_table__ = 'studio'
    __version__ = 'knn_1'

    id = Int(primary=True)
    name = Unicode()

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    updated_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)

    def __storm_pre_flush__(self):
        self.updated_at = _utcnow()


@stormSchema.versioned
class game(object):
    __storm_table__ = 'game'
    __version__ = 'knn_1'

    id = Int(primary=True)
    guid = Unicode()

    studio_id = Int()
    studio = Reference(studio_id, Studio.id)

    name = Unicode()
    description = Unicode()

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    updated_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)

    def __storm_pre_flush__(self):
        self.updated_at = _utcnow()


@stormSchema.versioned
class CreditType(object):
    _storm_table__ = 'credit_type'
    __version__ = 'knn_1'

    id = Int(primary=True)

    game_id = Int()
    game = Reference(game_id, Game.id)

    name = Unicode()
    exchange_rate = Int()
    icon_filename = RawStr()

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    updated_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)

    def __storm_pre_flush__(self):
        self.updated_at = _utcnow()


@stormSchema.versioned
class Package(object):
    __storm_table__ = 'package'
    __version__ = 'knn_1'

    id = Int(primary=True)

    game_id = Int()
    game = Reference(game_id, Game.id)
  
    credit_type_id = Int()
    credit_type = Reference(credit_type_id, CreditType.id)

    name = Unicode()
    credit_value = Int()
    gcoin_value = Float()
    icon_filename = RawStr()

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    updated_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)

    def __storm_pre_flush__(self):
        self.updated_at = _utcnow()


@stormSchema.versioned
class CreditBalance(object):
    __storm_table__ = 'credit_balance'
    __version__ = 'knn_1'

    id = Int(primary=True)

    credit_type_id = Int()
    credit_type = Reference(credit_type_id, CreditType.id)

    customer_account_id = Int()
    customerAccount = Reference(customer_account_id, CustomerAccount.id)

    balance = Int()
