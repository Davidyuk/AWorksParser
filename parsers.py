import re
from lxml import html


def groups_parser(text):
    tree = html.fromstring(text)
    res = []
    for option in tree.xpath('//*[@id="group"]/option'):
        if not option.get('value').isdigit():
            continue
        res.append({'id': int(option.get('value')), 'name': option.text})
    return res


def student_list_parser(text):
    tree = html.fromstring(text)
    res = []
    for a in tree.xpath('//table[@class="works"]/tr/td/a'):
        uid = int(re.match('marks_student\?id=(\d+)', a.get('href')).group(1))
        res.append({'id': uid, 'name': a.text})
    return res


def student_parser(text):
    tree = html.fromstring(text)
    res = []
    for tr in tree.xpath('//table[@class="bordered marks"]/tr'):
        tds = tr.xpath('td')
        if tr.get('class') == 'worktype':
            res.append({'name': tds[0].text, 'tasks': []})
        elif len(tds) == 4:
            a = tds[1].xpath('a')[0]
            tid = int(re.match('marks_view\?tid=(\d+);sid=(\d+)', a.get('href')).group(1))
            [max_rate, rate_weight] = map(int, re.match('1\.\.(\d+), (\d+)%', tds[2].text).groups())
            res[-1]['tasks'].append({'date': tds[0].text, 'id': tid, 'name': a.text or '', 'maxRate': max_rate,
                                     'rateWeight': rate_weight, 'marks': []})
            for tr in tds[3].xpath('table/tr'):
                tds = tr.xpath('td')
                if len(tds) != 3:
                    continue
                rate2 = float(tds[2].text) if tds[2].text else None
                res[-1]['tasks'][-1]['marks'].append({'date': tds[0].text, 'rate1': float(tds[1].text), 'rate2': rate2})
    return res
