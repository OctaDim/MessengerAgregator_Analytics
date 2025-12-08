# ######################################################################
# ###### VERY IMPORTANT IMPORTS TO INITIALIZE POSTGRES DB TABLES #######
# ######################################################################

from db_postgres.postgres_models.auth_role_model import AuthRoleModel
from db_postgres.postgres_models.webhook_connection_model import WebhookConnectionModel
from db_postgres.postgres_models.webhook_conversation_model import WebhookConversationModel
from db_postgres.postgres_models.webhook_message_model import WebhookMessageModel

# ######################################################################
# ############ DON'T AUTO FORMAT, COMMIT OR REMOVE IMPORTS #############
# ######################################################################
