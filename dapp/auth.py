import os
from datetime import datetime
import pytz
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client
from keystoneauth1.exceptions.http import NotFound


def __check_creds(token):
    if os.environ.get('ET_AAA_ESM_KEYSTONE_AUTH_URL', '') == '':
        print('No auth set.')
        return True

    keystone = __keystone_client()
    try:
        resp = keystone.tokens.validate(token, include_catalog=False)
    except NotFound:
        print('no token found!')
        return False

    # note that the IDs of the roles assigned to the user are also included
    # this can allow for finer grain access policies.

    print('---------------------------------------------------')
    print('response from keystone:\n{kresp}'.format(kresp=resp))
    print('---------------------------------------------------')

    utc = pytz.UTC
    tt = resp.expires.replace(tzinfo=utc)
    lt = datetime.now()
    lt = lt.replace(tzinfo=utc)
    return lt < tt


def __keystone_client():
    auth_url = os.environ.get('ET_AAA_ESM_KEYSTONE_AUTH_URL', 'http://keystone:5000/v3')
    username = os.environ.get('ET_AAA_ESM_KEYSTONE_USERNAME', 'admin')
    passwd = os.environ.get('ET_AAA_ESM_KEYSTONE_PASSWD', 'admin')
    tenant = os.environ.get('ET_AAA_ESM_KEYSTONE_TENANT', 'admin')

    # XXX note that the domain is assumed to be default
    auth = v3.Password(auth_url=auth_url, username=username, password=passwd, project_name=tenant,
                       user_domain_id="default", project_domain_id="default")
    # TODO Cache this client
    keystone = client.Client(session=session.Session(auth=auth))
    return keystone