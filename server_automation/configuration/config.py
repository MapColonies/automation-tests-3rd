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

