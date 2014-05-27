from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from scripts import auth
from scripts import sfdc
import urllib
from pyramid.renderers import render_to_response
import json
import logging
from .models import (
    DBSession,
    MyModel,
    )

log = logging.getLogger(__name__)
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
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
user_id = 'mudit@mammoth.io'
consumer_id = '3MVG9Y6d_Btp4xp6OwOuiNQWWJpbLZjerzlwDJNUIg4NXa59xlmeoQdLw1KaUVGED5Hu_DuMUCbsEVKLKDjhl'
consumer_secret = '8334446631108857716'
redirect_uri = 'https://localhost/sObjects'
@view_config(route_name='sObjects', renderer='templates/sObjects.pt')
def sObject_view(request):
    code = request.GET['code']
    data = {
        'grant_type': 'api',
        'redirect_uri': redirect_uri,
        'code':code
    }
    sfoAuth = auth.SalesforceOAuth2(consumer_id,consumer_secret,redirect_uri)
    token_response = sfoAuth.get_token(code)
    user_id = urllib.urlopen(token_response['id'])
    log.debug("access_token : %s, instance_url : %s",token_response['access_token'],token_response['instance_url'])
    sf = sfdc.sfdcdatafetch(token_response['access_token'],token_response['instance_url'])
    object = sf.returnsObject()
    if(MyModel.get_by_id(user_id)):
        MyModel.get_by_id(user_id).delete_obj()
        new_row = MyModel(id = user_id, access_token = token_response['access_token'], refresh_token = token_response['refresh_token'], instance_url =  token_response['instance_url'])
        new_row.save_obj()
    else :
        new_row = MyModel(id = user_id,access_token = token_response['access_token'],refresh_token=token_response['refresh_token'], instance_url = token_response['instance_url'])
        new_row.save_obj()
    #log.debug(object)
    return {'objects':object}
@view_config(route_name='getTable', renderer='templates/getTable.pt')
def getTable(request):
    selected = request.params.getall("selectedcategories")
    log.debug(selected)
    auth_data = MyModel.get_by_id(user_id)
    log.debug(auth_data.access_token)
    log.debug(auth_data.refresh_token)
    sfoAuth = auth.SalesforceOAuth2(consumer_id,consumer_secret,redirect_uri)
    rf_token = sfoAuth.refresh_token(auth_data.refresh_token)
    sf = sfdc.sfdcdatafetch(rf_token,auth_data.instance_url)
    field_types=[]
    for x in selected:
        field_types.append(sf.getFieldType(x))
    log.debug(field_types)
    return {}