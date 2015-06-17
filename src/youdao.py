#!/usr/bin/env python
#coding=utf-8

from workflow import Workflow, web
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def translate(wf):

    url = 'http://fanyi.youdao.com/openapi.do'
    params = dict(
        keyfrom = 'Wentong',
        key = '1394860876',
        type = 'data',
        doctype = 'json',
        version = '1.1',
        # q = wf.args[0]
        q = 'hello'
    )

    res = web.get(url, params).json()

    if res.get('errorCode', '') == 0:
        wf.add_item(res['translation'][0], res.get('query'))
        for item in res['basic']['explains']:
            wf.add_item(item, res['query'])
        for item in res['web']:
            wf.add_item(', '.join(item['value']), item['key'])
    else:
        wf.add_item(u'没有找到', u'并没有找到你要的单词')

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(translate))
