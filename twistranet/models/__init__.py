# Importing all models from submodules

# Low-level stuff
from content import Content, StatusUpdate, ContentRegistry
from account import Account, UserAccount, SystemAccount
from community import Community, GlobalCommunity, AdminCommunity
from relation import Relation

# Do the mandatory database checkup and initial buiding
import dbsetup 
dbsetup.load_initial_data()
dbsetup.check_consistancy()

