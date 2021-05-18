# pylint: disable=line-too-long, invalid-name, fixme
"""This module provide test full functionality """
import json
import logging
import os
import time
from datetime import datetime, timedelta
from server_automation.ingestion_api import model_ingestion
from server_automation.configuration import config
from mc_automation_tools import common as common
from mc_automation_tools import base_requests as br
from mc_automation_tools import s3storage as s3

_logger = logging.getLogger("server_automation.function.executors")


def send_ingestion_request(request, request_name=None):
    """
    This method use ingestion api wrapping class to start new ingestion process
    """
    if request_name:
        request['metadata']['identifier'] = request_name

    _logger.info('Send request: %s to export ', request['metadata']['identifier'])
    # request = json.dumps(request)
    im = model_ingestion.IngestionModel()
    resp = im.post_model_ingestion_job(request)
    status_code, content = common.response_parser(resp)
    _logger.info('Response of trigger returned with status: %d', status_code)
    return status_code, content
