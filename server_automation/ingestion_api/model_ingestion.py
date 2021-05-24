"""This module provide wrapping class dealing with ingestion process of 3rd models"""

import json
import logging
from server_automation.configuration import config
from mc_automation_tools import common as common
from mc_automation_tools import base_requests as br

_log = logging.getLogger("server_automation.ingestion_api.model_ingestion")


class IngestionModel:
    """
    This class wrapping ingestion process API's and provide direct bas functionality
    """

    def __init__(self):
        self._ingestion_stack_url = config.INGESTION_STACK_URL
        self._ingestion_catalog_url = config.INGESTION_CATALOG_URL
        self._ingestion_job_service_url = config.INGESTION_JOB_SERVICE_URL

    def post_model_ingestion_job(self, request):
        """This method start and trigger new ingestion process of 3rd model"""
        if not isinstance(request, dict):
            _log.error(f'Request should be provided as valid json format:\n{request} => {type(request)}')
            raise TypeError('Request should be provided as valid json format')
        full_model_ingestion_url = common.combine_url(self._ingestion_stack_url, config.INGESTION_3RD_MODEL)
        resp = br.send_post_request(full_model_ingestion_url, body=request)
        return resp

    def get_single_job_status(self, job_id):
        """This method return specific ingestion job status"""
        if not isinstance(job_id, str):
            _log.error(f'should be provided job id string expressed as uuid:\n{job_id} => {type(job_id)}')
            raise TypeError('Request should be provided as valid json format')
        job_model_ingestion_url = common.combine_url(self._ingestion_job_service_url, config.INGESTION_3RD_JOB_STATUS, job_id)

        try:
            resp = br.send_get_request(job_model_ingestion_url)
            return resp
        except Exception as e:
            _log.error(f'Error on get response from ingestion job progress service with error {str(e)}')

    def is_model_on_catalog(self, identifier):
        """
        This method validate if model exists on catalog based on provided identifier
        :param identifier: string represented ingested 3rd model
        """
        resp = self.get_single_3rd_metadata(identifier)
        return True if resp.status_code == config.ResponseCode.Ok.value else False

    def get_single_3rd_metadata(self, identifier):
        """This method return specific exists metadata from catalog db"""
        if not isinstance(identifier, str):
            _log.error(f'should be provided identifier expressed as string:\n{identifier} => {type(identifier)}')
            raise TypeError('identifier should be provided as valid json format')
        model_metadata_on_catalog_url = common.combine_url(self._ingestion_catalog_url, config.INGESTION_CATALOG_MODEL_DATA, identifier)

        try:
            resp = br.send_get_request(model_metadata_on_catalog_url)
            return resp
        except Exception as e:
            _log.error(f'Error on get response from catalog db service with error {str(e)}')
            raise e

