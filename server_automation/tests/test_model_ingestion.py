# pylint: disable=line-too-long, invalid-name, broad-except, duplicate-code
""" This module responsible of testing export tools - server side:"""
import json
import logging
import time
from datetime import datetime
from server_automation.functions import executors as exc
from server_automation.configuration import config
from mc_automation_tools import common as common
from server_automation.tests import request_sampels

# from conftest import ValueStorage

_log = logging.getLogger('server_automation.tests.3RD_ingestion_process')
Z_TIME = datetime.now().strftime('_%Y%m_%d_%H_%M_%S')


def test_upload_model():
    """
    This test validate and testing validate E2E process of ingesting new model into db via upload / ingestion api
    """
    _log.info('Start running test: %s', test_upload_model.__name__)
    request = request_sampels.get_request(request_sampels.RequestsPool.sanity.name)
    assert request, \
        f'Test: [{test_upload_model.__name__}] Failed: File not exist or failure on loading request json'
    identifier = "_".join(['test_upload_model', Z_TIME])
    request['metadata']['identifier'] = identifier

    # start ingestion
    s_code, content = exc.send_ingestion_request(request)
    assert s_code == config.ResponseCode.IngestionModelOk.value, \
        f'Test: [{test_upload_model.__name__}] Failed: Ingestion model api return status code [{s_code}]'

test_upload_model()