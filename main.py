import requests
import json
import mail
import time
import os
import logging
import dnspod
import conf


def send_mail(ip_str):
    _mail = mail.get_default_user_mail('.mail_user_info.json')
    _mail.send_mail(conf.RECEIVER_EMAIL_ADDRESS, 'new ip:{}'.format(ip_str), ip_str)


def get_ip():
    url = 'https://v4.myip.la'
    ret = requests.get(url)
    return ret.text


def load_last_ip():
    if not os.path.exists('.last_ip'):
        return ''

    with open('.last_ip') as fr:
        return fr.read()


def save_ip(ip_str):
    with open('.last_ip', 'w') as fw:
        fw.write(ip_str)


def run():
    while 1:
        try:
            _last_ip = load_last_ip()
            _ip = get_ip().strip()
            logging.info('new ip:{}, old ip:{}'.format(_ip, _last_ip))
            if _ip != _last_ip:
                send_mail(_ip)

                dh = dnspod.DnspodHelper()
                dh.update_ddns(_ip)
            save_ip(_ip)

        except Exception as e:
            logging.error(e)
        time.sleep(10 * 60)


def main():
    run()


if __name__ == '__main__':
    logging.basicConfig(filename='ddns.log', level = getattr(logging, 'DEBUG'), format='%(levelname)s %(asctime)s %(message)s')
    main()

