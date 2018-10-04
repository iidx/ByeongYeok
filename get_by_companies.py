import requests
import re
byurl = 'https://work.mma.go.kr/caisBYIS/search/byjjecgeomsaek.do'
param = 'al_eopjong_gbcd=11111%2C11112&eopjong_gbcd_list=11111%2C11112&eopjong_gbcd=1&gegyumo_cd=&eopche_nm=&juso=&sido_addr=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&sigungu_addr=&chaeyongym=&bjinwonym=B&searchCondition=&searchKeyword=&pageUnit=10&pageIndex={page}&menu_id='

header = {'Content-Type': 'application/x-www-form-urlencoded'}
r = r"eopjong_gbcd_list=11111,11112\">\(?주?유?\)?(식회사)?\s?(.+)\(?주?유?\)?</a></th>"

companies = []
print("파싱 중...")
for x in range(1, 37):
    url = byurl + "?" + param.format(page=x)
    resp = requests.post(url, headers=header)
    resp = resp.text
    for x in re.findall(r, resp):
        _, x = x
        companies.append(x)
print(companies)

saramin = 'http://www.saramin.co.kr'
search_company = '/zf_user/search?searchword={comname}'
re_search_company = r"<a\shref=\"/zf_user/company-info/view\?csn=(.+)\"\stitle"

company_info = '/zf_user/company-info/view?csn={csnid}'
#re_is_recruitment = r"<span class=\"r_noti\">총 <b>(.+)건</b>의 채용을 진행하고 있습니다.</span>"
re_is_employee = r";\"\stitle=\"(.+)\"\sclass"

for company_name in companies:
    resp = requests.get(saramin+search_company.format(comname=company_name))
    resp = resp.text
    try:
        csnid = re.search(re_search_company, resp).group(1)
    except:
        print(company_name, '검색 실패')
        continue

    resp = requests.get(saramin+company_info.format(csnid=csnid))
    resp = resp.text
    
    res = re.findall(re_is_employee, resp)
    if res:
        print(company_name, '뽑 => ', saramin+company_info.format(csnid=csnid))
        for x in res:
            print(x)
        print()
        #res = re.search(re_is_recruitment, resp).group(1)
        #print(company_name, res, '건 뽑 =>', saramin+company_info.format(csnid=csnid))
    else:
        print(company_name, '안뽑\n')
        
