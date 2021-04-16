"""
	@author: HarHar (https://github.com/HarHar)
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.
	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.

    py3 conversion by RathHunt (https://github.com/RathHunt)
"""
import socket
try:
    import ujson as json
except:
    import json
import time


class vndbException(Exception):
    pass


class VNDB(object):
    """ Python interface for vndb's api (vndb.org), featuring cache """
    protocol = 1

    def __init__(self, clientname, clientver, username=None, password=None, debug=False):
        self.sock = socket.socket()

        if debug:
            print('Connecting to api.vndb.org')
        self.sock.connect(('api.vndb.org', 19534))
        if debug:
            print('Connected')

        if debug:
            print('Authenticating')
        if (username == None) or (password == None):
            self.sendCommand('login', {'protocol': self.protocol, 'client': clientname,
                                       'clientver': float(clientver)})
        else:
            self.sendCommand('login', {'protocol': self.protocol, 'client': clientname,
                                       'clientver': float(clientver), 'username': username, 'password': password})
        res = self.getRawResponse()
        if res.find('error ') == 0:
            raise vndbException(json.loads(
                ' '.join(res.split(' ')[1:]))['msg'])
        if debug:
            print('Authenticated')

        self.cache = {'get': []}
        self.cachetime = 720  # cache stuff for 12 minutes

    def close(self):
        self.sock.close()

    def get(self, type, flags, filters, options):
        """ Gets a VN/producer

        Example:
        >>> results = vndb.get('vn', 'basic', '(title="Clannad")', '')
        >>> results['items'][0]['image']
        u'http://s.vndb.org/cv/99/4599.jpg'
        """
        args = '{0} {1} {2} {3}'.format(type, flags, filters, options)
        for item in self.cache['get']:
            if (item['query'] == args) and (time.time() < (item['time'] + self.cachetime)):
                return item['results']

        self.sendCommand('get', args)
        res = self.getResponse()[1]
        self.cache['get'].append(
            {'time': time.time(), 'query': args, 'results': res})
        return res

    def sendCommand(self, command, args=None):
        """ Sends a command

        Example
        >>> self.sendCommand('test', {'this is an': 'argument'})
        """
        whole = ''
        whole += command.lower()
        if isinstance(args, str):
            whole += ' ' + args
        elif isinstance(args, dict):
            whole += ' ' + json.dumps(args)

        self.sock.send(('{0}\x04'.format(whole)).encode('utf-8'))

    def getResponse(self):
        """ Returns a tuple of the response to a command that was previously sent

        Example
        >>> self.sendCommand('test')
        >>> self.getResponse()
        ('ok', {'test': 0})
        """
        res = self.getRawResponse()
        cmdname = res.split(' ')[0]
        if len(res.split(' ')) > 1:
            args = json.loads(' '.join(res.split(' ')[1:]))

        if cmdname == 'error':
            if args['id'] == 'throttled':
                raise vndbException(
                    'Throttled, limit of 100 commands per 10 minutes')
            else:
                raise vndbException(args['msg'])
        return (cmdname, args)

    def getRawResponse(self):
        """ Returns a raw response to a command that was previously sent 

        Example:
        >>> self.sendCommand('test')
        >>> self.getRawResponse()
        'ok {"test": 0}'
        """
        finished = False
        whole = ''
        while not finished:
            whole += (self.sock.recv(4096)).decode('utf-8')
            if '\x04' in whole:
                finished = True
        return whole.replace('\x04', '').strip()


if __name__ == '__main__':
    vn = VNDB('darkness', '0.1', debug=True)
    print(vn.get('vn', 'basic,details', '(title="Clannad")', ''))
