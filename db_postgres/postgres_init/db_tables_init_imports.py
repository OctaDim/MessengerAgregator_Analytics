# ######################################################################
# ###### VERY IMPORTANT IMPORTS TO INITIALIZE POSTGRES DB TABLES #######
# ######################################################################

# PACT AGGREGATOR
from db_postgres.postgres_models._pact_pgs_models.webhook_auth_model import WebhookAuthModel
from db_postgres.postgres_models._pact_pgs_models.webhook_conversation_model import WebhookConversationModel
from db_postgres.postgres_models._pact_pgs_models.webhook_message_model import WebhookMessageModel
from db_postgres.postgres_models._pact_pgs_models.message_attachments_model import MessageAttachmentsModel
from db_postgres.postgres_models._pact_pgs_models.message_details_model import MessageDetailsModel
from db_postgres.postgres_models._pact_pgs_models.message_reactions_model import MessageReactionsModel
from db_postgres.postgres_models._pact_pgs_models.audio_msg_transcription_model import AudioMsgTranscriptionModel
from db_postgres.postgres_models._pact_pgs_models.keywords_plus_model import PlusKeywordsModel
from db_postgres.postgres_models._pact_pgs_models.keywords_minus_model import MinusKeywordsModel
from db_postgres.postgres_models._pact_pgs_models.keywords_subjects_model import PlusKeywordsSubjectModel
from db_postgres.postgres_models._pact_pgs_models.keywords_subjects_model import MinusKeywordsSubjectModel
from db_postgres.postgres_models._pact_pgs_models.chats_subjects_model import ChatsSubjectModel

# OWN AGGREGATOR
from db_postgres.postgres_models.auth_role_model import AuthRoleModel
from db_postgres.postgres_models.auth_role_model import AuthRoleModel
from db_postgres.postgres_models.customer_model import CustomerModel
from db_postgres.postgres_models.webhook_global_api_model import GlobalWebhookMsgModel

# ######################################################################
# ############ DON'T AUTO FORMAT, COMMIT OR REMOVE IMPORTS #############
# ######################################################################
