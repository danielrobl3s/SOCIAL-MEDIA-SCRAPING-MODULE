import requests

url = "https://www.instagram.com/graphql/query"

payload = 'av=17841449375330360&__d=www&__user=0&__a=1&__req=6&__hs=20005.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=2&__ccg=GOOD&__rev=1017196109&__s=k616pf%3Acsuhmx%3A4pljhb&__hsi=7423904862231244833&__dyn=7xe5WwlEnwn8K2Wmm1twpUnwgU7S6EdF8aUco38w5ux60p-0LVE4W0om782Cw8G11w6zx61vwoEcE2ygao1aU2swc20EUjwGzEaE2iwNwmE2ewnE3fw5rwSyES1Twoob82ZwrUdUbGw4mwr86C1mwrd6goK10xKi2K7E5yqcxK2K0PUy&__csr=&__comet_req=7&fb_dtsg=NAcPLETcAakF7Ac8IRHWPw9rNoyAKj3t9SnHaiZNiyHgcjUdAW3zfSw%3A17843729647189359%3A1728506540&jazoest=26326&lsd=3DlQbzuDt6hcu6VZC4OXAy&__spin_r=1017196109&__spin_b=trunk&__spin_t=1728512547&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfilePostsQuery&variables=%7B%22data%22%3A%7B%22count%22%3A12%2C%22include_relationship_info%22%3Atrue%2C%22latest_besties_reel_media%22%3Atrue%2C%22latest_reel_media%22%3Atrue%7D%2C%22username%22%3A%22nodal%22%2C%22__relay_internal__pv__PolarisIsLoggedInrelayprovider%22%3Atrue%2C%22__relay_internal__pv__PolarisFeedShareMenurelayprovider%22%3Atrue%7D&server_timestamps=true&doc_id=8343115342433006'
headers = {
  'accept': '*/*',
  'accept-language': 'es-419,es;q=0.9',
  'content-type': 'application/x-www-form-urlencoded',
  'cookie': 'mid=ZwRUWQAEAAEkOkvuteNAO2TdW--K; datr=WVQEZ9otxSdrW3lboj2lt3LI; ig_did=B52CEFC3-E13F-469D-AAAD-5C5C929934B3; ps_l=1; ps_n=1; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; ig_direct_region_hint="VLL\05449282885844\0541760048280:01f7399b20e704d7f6a48609d1a2bc4e1e11f0fc10052998f01ec225c4d823c141fb4d30"; csrftoken=UP5Srl1PbIGo2LlwHCRVBIsDYvxD2rSQ; ds_user_id=65086222838; sessionid=65086222838%3AnnvTf7pX8fywZD%3A25%3AAYevzOvpApPVcciUH5FeI0OimQs4ncAuzYKXoXgJBA; wd=663x812; rur="RVA\05465086222838\0541760063670:01f7245ede3164691e90aef6ca55c804772d791ef0dd5636e35b7737b8a47928c04c8d85"',
  'origin': 'https://www.instagram.com',
  'priority': 'u=1, i',
  'referer': 'https://www.instagram.com/nodal/',
  'sec-ch-prefers-color-scheme': 'dark',
  'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
  'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.100", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.100"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-model': '""',
  'sec-ch-ua-platform': '"macOS"',
  'sec-ch-ua-platform-version': '"14.6.1"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
  'x-asbd-id': '129477',
  'x-bloks-version-id': '8bb50762167c4432c174a01a25b916bfc9b78985507f03558e2f04754cf7cb10',
  'x-csrftoken': 'S1PkLaB9tIrf9ck70K6ICl8UiMx29HRx',
  'x-fb-friendly-name': 'PolarisProfilePostsQuery',
  'x-fb-lsd': '3DlQbzuDt6hcu6VZC4OXAy',
  'x-ig-app-id': '936619743392459'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
