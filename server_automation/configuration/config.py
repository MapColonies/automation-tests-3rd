# pylint: disable=line-too-long
""" configuration interface """
import enum
from mc_automation_tools import common


class ResponseCode(enum.Enum):
    """
    Types of server responses
    """
    Ok = 200  # server return ok status
    ValidationErrors = 400  # bad request
    StatusNotFound = 404  # status\es not found on db
    ServerError = 500  # problem with error
    DuplicatedError = 409  # in case of requesting package with same name already exists


#############################################      Running global environment variables     ################################################
ENVIRONMENT_NAME = common.get_environment_variable('ENVIRONMENT_NAME', 'dev')
TMP_DIR = common.get_environment_variable('TMP_DIR', '/tmp/auto_3rd')
#####################################################        Environment         ###########################################################
INGESTION_STACK_URL = common.get_environment_variable('INGESTION_STACK_URL', 'http://ingestion-stack-3d-model-ingestion-service-route-3d.apps.v0h0bdx6.eastus.aroapp.io/')
INGESTION_CATALOG_URL = common.get_environment_variable('INGESTION_CATALOG_URL', 'http://ingestion-stack-3d-ingestion-catalog-route-3d.apps.v0h0bdx6.eastus.aroapp.io/')
INGESTION_JOB_SERVICE_URL = common.get_environment_variable('INGESTION_JOB_SERVICE_URL', 'http://ingestion-stack-discrete-ingestion-db-route-3d.apps.v0h0bdx6.eastus.aroapp.io/')
##################################################  Ingestion API's sub urls & API's  ######################################################
INGESTION_3RD_MODEL = 'models'
################################################################## S3 ######################################################################
S3_DOWNLOAD_EXPIRATION_TIME = common.get_environment_variable("S3_DOWNLOAD_EXPIRED_TIME", 3600)
S3_DOWNLOAD_DIRECTORY = common.get_environment_variable('S3_DOWNLOAD_DIR', '/tmp/')
S3_BUCKET_NAME = common.get_environment_variable('S3_BUCKET_NAME', None)
S3_ACCESS_KEY = common.get_environment_variable('S3_ACCESS_KEY', None)
S3_SECRET_KEY = common.get_environment_variable('S3_SECRET_KEY', None)
S3_END_POINT = common.get_environment_variable('S3_END_POINT', None)
###################################################################### general ##############################################################
USE_JIRA = common.get_environment_variable('USE_JIRA', False)
INGESTION_MENDATORY_PARAMS = ['modelPath', ]