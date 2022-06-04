import requests
import json
import conf
import logging

URI_BASE = 'https://dnsapi.cn'


class DnspodHelper(object):
    def get_record(self):
        url = '{}/{}'.format(URI_BASE, 'Record.List')
        data = {
            'login_token': conf.LOGIN_TOKEN,
            'domain': conf.DOMAIN,
        }

        ret = requests.post(url, data=data)
        return ret.text

    def save(self, filename, content):
        with open(filename, 'w') as fw:
            fw.write(content)

    def load(self, filename):
        with open(filename) as fr:
            return fr.read()

    def parse_record(self, content):
        ret_data = json.loads(content)

        for rec in ret_data['records']:
            print(rec)

    def update_ddns(self, ip_str):
        url = '{}/{}'.format(URI_BASE, 'Record.Ddns')
        data = {
            'login_token': conf.LOGIN_TOKEN,
            'domain': conf.DOMAIN,
            'record_id': conf.RECORD_ID,
            'record_line': '默认',
            'record_line_id': 0,
            'value': ip_str
        }
        logging.info('update ddns:{}'.format(data))
        ret = requests.post(url, data=data)
        logging.info('result:{}'.format(ret.text))


if __name__ == '__main__':
    dh = DnspodHelper()
    #ret = dh.get_record()
    #dh.save('.record', ret)
    ret = dh.load('.record')
    dh.parse_record(ret)
