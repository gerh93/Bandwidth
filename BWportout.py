"""
Port a telephone number from Bandwidth using their API.


pip install xmljson
pip install requests

"""

import argparse
import logging
import StringIO
import requests
from xmljson import badgerfish as bf
from envparse import env
from xml.etree.ElementTree import fromstring

BASE_URL = 'https://dashboard.bandwidth.com/v1.0/'

log = logging.getLogger(__name__)

class BandwidthAPI(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        

    def TN_query(self, phone_number):
        """
        Runs a TN query for the provided phone_number.

        params:
          - phone_number is the number to lookup on Bandwidth

        return:  
          - retrives status, ordertype, orderid
          
        
        """
        tags = {}
        response = self._call('tns/%s' % phone_number)
        for x in response.findall(".//"):
            tags[x.tag] = x.text
            log.debug( x.tag, x.text)
        return tags
        
    def LSR_order(self, phone_number):
        raise NotImplemented

    def port_in(self, **port_order):
        raise NotImplemented

    def _call(self, path, **kwargs):
        req = requests.get(BASE_URL, auth=(self.user, self.password)) 
        json_response = bf.data(fromstring(req.text))        

        log.debug() ('Raw response:\n' + req.text +  '\n\n')

        responseCode = req.status_code;
        log.debug('Response code: ' + str(responseCode))

        isSuccesResponse = r.status_code == requests.codes.ok;
        if not req.status_code == requests.codes.ok:
            raise FailedException(str(responseCode))
     
        root = ET.fromstring(contents.getvalue())
        return root


class FailedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(FailedException, self, *args, **kwargs)
        log.warn('Response code: ' + str(responseCode))
        log.warn(root.tag)
        log.warn(root[0][0].tag + ': ' +root[0][0].text)
        log.warn(root[0][1].tag + ': ' +root[0][1].text)
        

if __name__ == '__main__':
   logging.basicConfig()
   log.setLevel(logging.DEBUG)
   env.read_envfile()
   parser = argparse.ArgumentParser('bandwidth', description=__doc__)
   parser.add_argument('phone_number', metavar='phone_number', type=str, nargs='+')
   parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', default=False) 
   parser.add_argument('--user', '-u', dest='user', required=True,
                        help='The initial authorization.')
   parser.add_argument('--password', '-u', dest='password', required=True,
                        help='The initial authorization.')
   args = parser.parse_args()
   try:
      api = BandwidthAPI(user, password)
      api.TN_query(args.phone_number)
   except:  pass