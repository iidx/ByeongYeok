"""
병역명문가란게있길래 궁금해서 소팅해본거...
지역코드가 왜인지 2~16밖에없음 1어디감?
"""
import json
import requests

year = 2018
base_url = 'https://open.mma.go.kr/caisGGGS/hall/mmg/listAllCall.json?yr={year}&jbc_cd={num}&callback'
dutydata_url = 'https://open.mma.go.kr/caisGGGS/hall/mmg/memberCall.json?yr={year}&grno={grno}&callback'

def remove_brackets_json(requests_object):
    return json.loads(requests_object.text[1:-1])

gamuns = []
for n in range(2, 16):
    url = base_url.format(year=year, num='%02d'%n)
    req = remove_brackets_json(requests.get(url))
    for x in req['mmgList']:
        url = dutydata_url.format(year=year, grno=x['bymyeongmunga_grno'])
        x_req = remove_brackets_json(requests.get(url))
        x_req = x_req['jwgt_BYMYEONGMUNGAVO']
        loc, sign = x_req['bymyeongmunga_grno'].split('-')
        gamuns.append({ 'name': x_req['daepyoja_fnm'],
                        'sign': sign,
                        'loc': loc,
                        'serv_t': int(x_req['bokmu_mcnt_sum']),
                        'serv_n': int(x_req['ihaengja_cnt'])})
    print(n, 'done.')
gamuns = sorted(gamuns, key=lambda k: k['serv_n']) 
for x in gamuns:
    print('{} - {} 소재 {} 가문 총 {}명 {}개월 복무'.format(x['sign'], x['loc'], x['name'], x['serv_n'], x['serv_t']))
