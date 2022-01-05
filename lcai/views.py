import logging

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseNotFound

from arches.app.utils.response import JSONResponse
from arches.app.models.resource import Resource
from arches.app.utils.exceptions import InvalidNodeNameException, MultipleNodesFoundException
from arches.app.models.system_settings import settings

logger = logging.getLogger(__name__)


def get_node_values(request):
    resourceid = request.GET.get('resourceid')
    node_name = request.GET.get('node_name')

    resource = Resource.objects.get(pk=resourceid)
    value = ''

    try:
        value = resource.get_node_values(node_name)
    except InvalidNodeNameException as e:
        logger.exception(e)
        return HttpResponseNotFound("Node not found")
    except MultipleNodesFoundException as e:
        logger.exception(e)
        return HttpResponseBadRequest("Multiple nodes with name '{}' found".format(node_name))
    return JSONResponse(value)

def rockart(request) :
	return render(request, 'rockart.htm', {
        'main_script': 'index',
        'app_title': settings.APP_TITLE,
        'copyright_year': settings.COPYRIGHT_YEAR
    })