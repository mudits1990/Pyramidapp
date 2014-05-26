from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from scripts import auth
from scripts import sfdc
from pyramid.renderers import render_to_response
import logging
from .models import (
    DBSession,
    MyModel,
    )

log = logging.getLogger(__name__)
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_sfdcdatafetch_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
@view_config(route_name='sObjects', renderer='templates/sObjects.pt')
def sObject_view(request):
    consumer_id = '3MVG9Y6d_Btp4xp6OwOuiNQWWJpbLZjerzlwDJNUIg4NXa59xlmeoQdLw1KaUVGED5Hu_DuMUCbsEVKLKDjhl'
    consumer_secret = '8334446631108857716'
    redirect_uri = 'https://localhost/sObjects'
    code = request.GET['code']
    data = {
        'grant_type': 'api',
        'redirect_uri': redirect_uri,
        'code':code
    }
    sfoAuth = auth.SalesforceOAuth2(consumer_id,consumer_secret,redirect_uri)
    token_response = sfoAuth.get_token(code)
    log.debug("access_token : %s, instance_url : %s",token_response['access_token'],token_response['instance_url'])
    sf = sfdc.sfdcdatafetch(token_response['access_token'],token_response['instance_url'])
    object = sf.returnsObject()
    #log.debug(object)
    return {'objects':object}
@view_config(route_name='getTable', renderer='templates/getTable.pt')
def getTable(request):
    selected = request.params.getall("selectedcategories")
    log.debug(selected)
    return {}