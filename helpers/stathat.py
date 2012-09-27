import urllib
import urllib2

class StatHat:

    def http_post(self, path, data):
        try:
            pdata = urllib.urlencode(data)
            req = urllib2.Request('http://api.stathat.com' + path, pdata)
            resp = urllib2.urlopen(req)
            return resp.read()
        except urllib2.HTTPError, e:
            # StatHat error
            return None

    def post_value(self, user_key, stat_key, value):
        data = {'key': stat_key, 'ukey': user_key, 'value': value}
        return self.http_post('/v', data)

    def post_count(self, user_key, stat_key, count):
        data = {'key': stat_key, 'ukey': user_key, 'count': count}
        return self.http_post('/c', data)

    def ez_post_value(self, ezkey, stat_name, value):
        data = {'ezkey': ezkey, 'stat': stat_name, 'value': value}
        return self.http_post('/ez', data)

    def ez_post_count(self, ezkey, stat_name, count):
        data = {'ezkey': ezkey, 'stat': stat_name, 'count': count}
        return self.http_post('/ez', data)