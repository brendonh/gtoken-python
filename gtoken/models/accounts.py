import pytz
from . import stormSchema
from utils.gtoken_time import _utcnow
from models.games import Studio

@stormSchema.versioned
class CustomerAccount(object):
    __storm_table__ = 'customer_account'
    __version__ = 'knn_1'

    id = Int(primary=True)
    nickname = Unicode()
    email = Unicode()
    gender = RawStr()
    avatar_filename = RawStr()

    vip = RawStr()
    coins = Float()
    
    referral_code = Unicode()
    inviter_id = Int()
    inviter = Reference(inviter_id, "CustomerAccount.id")

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    updated_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    last_login_at = DateTime(tzinfo=pytz.UTC)

    is_archived = Bool(default=False)

    def __storm_pre_flush__(self):
        self.updated_at = _utcnow()


@stormSchema.versioned
class CustomerLoginPassword(object):
    __storm_table__ = 'customer_login_password'
    __version__ = 'knn_1'
    id = Int(primary=True)

    customer_account_id = Int()
    customerAccount = Reference(customer_account_id, CustomerAccount.id)

    username = Unicode()
    email = Unicode()
    password = Unicode()


@stormSchema.versioned
class CustomerLoginOauth(object):
    __storm_table__ = 'customer_login_oauth'
    __version__ = 'knn_1'

    id = Int(primary=True)
    
    customer_account_id = Int()
    customerAccount = Reference(customer_account_id, CustomerAccount.id)

    service = RawStr()
    identity = RawStr()


@stormSchema.versioned
class AdminAccount(object):
    __storm_table__ = 'admin_account'
    __version__ = 'knn_1'

    id = Int(primary=True)
    
    username = Unicode()
    passsword = Unicode()
    email = Unicode()
    role = RawStr()

    studio_id = Int()
    studio = Reference(studio_id, 'Studio.id')

    created_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    updated_at = DateTime(tzinfo=pytz.UTC, default_factory=models._utcnow)
    last_login_at = DateTime(tzinfo=pytz.UTC)

    is_active = Bool(default=False)
    is_archived = Bool(default=False)

    def __storm_pre_flush__(self):
        self.updated_at = _utcnow()


@stormSchema.versioned
class PartnerAccount(object):
    __storm_table__ = 'partner_account'
    __version__ = 'knn_1'

    id = Int(primary=True)
    
    name = Unicode()

    client_id = RawStr()
    client_secret = RawStr()
    redirect_uris = RawStr()
    default_scopes = RawStr()
