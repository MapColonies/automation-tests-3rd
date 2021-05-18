# pylint: disable=line-too-long, raise-missing-from, trailing-comma-tuple
"""This module provide generation of several request json files for testing purpose"""
import json
import enum
from server_automation.configuration import config


# class BoxSize(enum.Enum):
#     """ Size of bbox """
#     Sanity = 1,
#     Small = 10,
#     Medium = 50,
#     Big = 150


# class ZoomLevels(enum.Enum):
#     """
#     Types of zoom levels
#     """
#     default = 18
#     med = 15

class RequestsPool(enum.Enum):
    sanity = 1,


_sanity_request = {
    "modelPath": "/home/libotadmin/NewYorkCity3d",
    "metadata": {
        "identifier": "1234",
        "typename": "string",
        "schema": "string",
        "mdSource": "string",
        "xml": "string",
        "anytext": "string",
        "insertDate": "2021-04-29T10:04:58.830Z",
        "creationDate": "2021-04-29T10:04:58.830Z",
        "validationDate": "2021-04-29T10:04:58.830Z",
        "wktGeometry": "POLYGON((34.8076891807199 31.9042863434239,34.816135996859 31.9042863434239,34.816135996859 31.9118071956932,34.8076891807199 31.9118071956932,34.8076891807199 31.9042863434239))",
        "title": "string",
        "producerName": "IDFMU",
        "description": "string",
        "type": "string",
        "classification": "string",
        "srs": "string",
        "projectName": "string",
        "version": "string",
        "centroid": "string",
        "footprint": "string",
        "timeBegin": "2021-04-29T10:04:58.830Z",
        "timeEnd": "2021-04-29T10:04:58.830Z",
        "sensorType": "string",
        "region": "string",
        "nominalResolution": "string",
        "accuracyLE90": "string",
        "horizontalAccuracyCE90": "string",
        "relativeAccuracyLE90": "string",
        "estimatedPrecision": "string",
        "measuredPrecision": "string",
        "links": [
            {
                "name": "string",
                "description": "string",
                "protocol": "string",
                "url": "string"
            }
        ]
    }
}


def get_request(name):
    """
  This method provide 3rd valid json request by passing request name
  """
    if name == RequestsPool.sanity.name:
        return _sanity_request
