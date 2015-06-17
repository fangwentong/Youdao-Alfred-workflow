#!/usr/bin/env python
#coding=utf-8

from workflow import Workflow, web
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

errorInfo = {
    '20': u'要翻译的文本过长',
    '30': u'无法进行有效的翻译',
    '40': u'不支持的语言类型',
    '50': u'无效的key',
    '60': u'无词典结果，仅在获取词典结果生效'
}

def translate(wf):

    url = 'http://fanyi.youdao.com/openapi.do'
    params = dict(
        keyfrom = 'Wentong',
        key = '1394860876',
        type = 'data',
        doctype = 'json',
        version = '1.1',
        q = wf.args[0]
    )

    res = web.get(url, params).json()

    error_code = res.get('errorCode', '')
    if error_code == 0:
        wf.add_item(res['translation'][0], res.get('query'))
        for item in res['basic']['explains']:
            wf.add_item(item, res['query'])
        for item in res['web']:
            wf.add_item(', '.join(item['value']), item['key'])
    else:
        wf.add_item(errorInfo[str(error_code)], wf.args[0])

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(translate))
