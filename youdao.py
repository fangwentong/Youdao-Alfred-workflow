#!/usr/bin/env python
#coding=utf-8

from workflow import Workflow, web
import sys, urllib2

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
        key     = '1394860876',
        type    = 'data',
        doctype = 'json',
        version = '1.1',
        q       = wf.args[0]
    )

    try:
        res = web.get(url, params).json()
        error_code = res.get('errorCode', '')
        if error_code == 0:
            wf.add_item(
                title    = res['translation'][0],
                subtitle = res.get('query'),
                copytext = res['translation'][0],
                arg      = res['translation'][0],
                valid    = True,
            )
            if res.get('basic'):
                for item in res['basic']['explains']:
                    wf.add_item(
                        title    = item,
                        subtitle = res['query'],
                        copytext = item,
                        arg      = item,
                        valid    = True,
                    )
            if res.get('web'):
                for item in res['web']:
                    wf.add_item(
                        title    = ', '.join(item['value']),
                        subtitle = item['key'],
                        copytext = ', '.join(item['value']),
                        arg      = ', '.join(item['value']),
                        valid    = True,
                    )
        else:
            wf.add_item(
                title    = errorInfo[str(error_code)],
                subtitle = wf.args[0],
            )

    except urllib2.URLError:
        wf.add_item(
            title    = u'网络异常',
            subtitle = u'请检查网络设置',
        )
    except:
        wf.add_item(
            title    = u'未知错误',
            subtitle = u'未知错误',
        )
    finally:
        wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(translate))
