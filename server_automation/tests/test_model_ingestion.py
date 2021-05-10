# pylint: disable=line-too-long, invalid-name, broad-except, duplicate-code
""" This module responsible of testing export tools - server side:"""
import json
import logging
import time
from datetime import datetime
# from server_automation.tests import request_sampels
# from server_automation.functions import executors as exc
from server_automation.configuration import config
from mc_automation_tools import common as common

# from conftest import ValueStorage

_log = logging.getLogger('server_automation.tests.3RD_ingestion_process')
Z_TIME = datetime.now().strftime('_%Y%m_%d_%H_%M_%S')


def test_upload_model():
    """
    This test validate and testing validate E2E process of ingesting new model into db via upload\ingest api
    """
    _log.info('Start running test: %s', test_upload_model.__name__)
