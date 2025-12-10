# ######################################################################
# ###### VERY IMPORTANT IMPORTS TO INITIALIZE POSTGRES DB TABLES #######
# ######################################################################

from db_postgres.postgres_models.auth_role_model import AuthRoleModel
from db_postgres.postgres_models.webhook_auth_model import WebhookAuthModel
from db_postgres.postgres_models.webhook_conversation_model import WebhookConversationModel
from db_postgres.postgres_models.webhook_message_model import WebhookMessageModel
from db_postgres.postgres_models.message_attachments_model import MessageAttachmentsModel
from db_postgres.postgres_models.message_details_model import MessageDetailsModel
from db_postgres.postgres_models.message_reactions_model import MessageReactionsModel

# ######################################################################
# ############ DON'T AUTO FORMAT, COMMIT OR REMOVE IMPORTS #############
# ######################################################################
