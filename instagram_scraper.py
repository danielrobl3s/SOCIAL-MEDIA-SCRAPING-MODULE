import requests

def get_user_posts(username):

  url = "https://www.instagram.com/graphql/query"

  payload = f'av=17841465245145777&hl=es&__d=www&__user=0&__a=1&__req=6&__hs=20006.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=2&__ccg=UNKNOWN&__rev=1017226246&__s=qj0nq9%3A24xszg%3A0acc7x&__hsi=7424179546107152794&__dyn=7xe5WwlEnwn8K2Wmm1twpUnwgU7S6EdF8aUco38w5ux60p-0LVE4W0om782Cw8G11w6zx61vwoEcE2ygao1aU2swc20EUjwGzEaE2iwNwmE2ewnE3fw5rwSyES1Twoob82ZwrUdUbGw4mwr86C1mwrd6goK10xKi2K7E5yqcxK2K0PUy&__csr=&__comet_req=7&fb_dtsg=NAcP6H2QkkOxEhrlBsRWSdzd4VpTHE_6gobXFTI4JOO_l4kKle2eQyg%3A17843676607167008%3A1728527552&jazoest=26312&lsd=T_FkSMEN_zVrruSDga-ofO&__spin_r=1017226246&__spin_b=trunk&__spin_t=1728576502&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfilePostsQuery&variables=%7B%22data%22%3A%7B%22count%22%3A12%2C%22include_relationship_info%22%3Atrue%2C%22latest_besties_reel_media%22%3Atrue%2C%22latest_reel_media%22%3Atrue%7D%2C%22username%22%3A%22{username}%22%2C%22__relay_internal__pv__PolarisIsLoggedInrelayprovider%22%3Atrue%2C%22__relay_internal__pv__PolarisFeedShareMenurelayprovider%22%3Atrue%7D&server_timestamps=true&doc_id=8343115342433006'
  headers = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'mid=ZwRUWQAEAAEkOkvuteNAO2TdW--K; datr=WVQEZ9otxSdrW3lboj2lt3LI; ig_did=B52CEFC3-E13F-469D-AAAD-5C5C929934B3; ps_l=1; ps_n=1; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; ig_direct_region_hint="VLL\\05449282885844\\0541760048280:01f7399b20e704d7f6a48609d1a2bc4e1e11f0fc10052998f01ec225c4d823c141fb4d30"; csrftoken=UP5Srl1PbIGo2LlwHCRVBIsDYvxD2rSQ; ds_user_id=65086222838; sessionid=65086222838%3AnnvTf7pX8fywZD%3A25%3AAYet1p9NeZxM9sGc8ATtlMOl7FAoj2R1SenzjT51JQ; rur="EAG\\05465086222838\\0541760112498:01f74c9c245f8b2c46b511438af78c9d685b188288141d49da49e1d58fc720f2f9d5f7d6"; wd=827x812; csrftoken=kFP5Pxdr4yd7Jpzd0Be9XJMxAVDWoehc; ds_user_id=65086222838; rur="EAG\\05465086222838\\0541760112614:01f7edc1e8b8ee0f6d99b15cb2d551f4f0917d2aea715f277b481929040f2111f8c2d315"',
    'origin': 'https://www.instagram.com',
    'priority': 'u=1, i',
    'referer': f'https://www.instagram.com/{username}/?hl=es',
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
    'x-csrftoken': 'UP5Srl1PbIGo2LlwHCRVBIsDYvxD2rSQ',
    'x-fb-friendly-name': 'PolarisProfilePostsQuery',
    'x-fb-lsd': 'T_FkSMEN_zVrruSDga-ofO',
    'x-ig-app-id': '936619743392459'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  r = response.json()

  posts = r['data']['xdt_api__v1__feed__user_timeline_graphql_connection']['edges']
  data = []

  user_id = posts[0]['node']['user']['pk']

  for post in posts:
    
    code = post['node']['code']

    media_id = post['node']['pk']

    title = post['node']['caption']['text']

    like_count = post['node']['like_count']

    comment_count = post['node']['comment_count']

    comment = get_post_comments(code, media_id)

    if post['node']['video_versions'] == None:
      is_video = "False"

    else:
      is_video = "True"

    taken_at = post['node']['taken_at']

    data.append({"code": code, "media_id": media_id, "title": title, "likes_count": like_count, "comment_count": comment_count, "comments": comment, "is_video?": is_video, "taken_at": taken_at})

  return data, user_id




def get_post_comments(code, media_id):

  url = f"https://www.instagram.com/api/v1/media/{media_id}/comments/?can_support_threading=true&permalink_enabled=false&hl=es"

  payload = {}
  headers = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.9',
    'cookie': 'mid=ZwRUWQAEAAEkOkvuteNAO2TdW--K; datr=WVQEZ9otxSdrW3lboj2lt3LI; ig_did=B52CEFC3-E13F-469D-AAAD-5C5C929934B3; ps_l=1; ps_n=1; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; ig_direct_region_hint="VLL\\05449282885844\\0541760048280:01f7399b20e704d7f6a48609d1a2bc4e1e11f0fc10052998f01ec225c4d823c141fb4d30"; csrftoken=UP5Srl1PbIGo2LlwHCRVBIsDYvxD2rSQ; ds_user_id=65086222838; sessionid=65086222838%3AnnvTf7pX8fywZD%3A25%3AAYefYpfnHjeVINjfMowufGCC1f5fEQskylMhV5PLmA; wd=827x812; rur="CCO\\05465086222838\\0541760111534:01f7831ebb2b9d64f00a47af48cc2b6ee322bb36e28df2bfbeaaedd15e0108d2abaa72ad"; csrftoken=kFP5Pxdr4yd7Jpzd0Be9XJMxAVDWoehc; ds_user_id=65086222838; rur="EAG\\05465086222838\\0541760111816:01f7b6f9026d872ddbf7b2de8dff6e97b320c70180bdd00e82d17b957b7537088d71a624"',
    'priority': 'u=1, i',
    'referer': f'https://www.instagram.com/p/{code}/?hl=es&img_index=1',
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
    'x-csrftoken': 'UP5Srl1PbIGo2LlwHCRVBIsDYvxD2rSQ',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR2RG47XxdXMhIam1qJFqgw-V6mdxVIlnsL-3H1ziOQJARRC',
    'x-requested-with': 'XMLHttpRequest'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  r = response.json()

  users = []
  texts = []
  commentos = r['comments']


  for comment in commentos:
    users.append(comment['user']['username'])
    texts.append(comment['text'])
  
  return {'users_that_commented': users, "comments": texts}


def get_similar_users(username, user_id):

  url = "https://www.instagram.com/graphql/query"

  payload = f'av=17841465245145777&hl=es&__d=www&__user=0&__a=1&__req=5&__hs=20006.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=2&__ccg=UNKNOWN&__rev=1017234147&__s=he40q2%3A24xszg%3Aksqfye&__hsi=7424259351402020069&__dyn=7xe5WwlEnwn8K2Wmm1twpUnwgU7S6EdF8aUco38w5ux60p-0LVE4W0om782Cw8G11wBw5Zx62G3i1ywOwa90Fw4Hw9O0Lbwae4UaEW2G0AEco5G0zEnwhE3fw5rwSyES1Twoob82ZwrUdUbGw4mwr86C1mwrd6goK10xKi2K7E5yqcxK2K0Pay8&__csr=gP2k45OTlhIn9-x5QQGt94XGF5QQJRXJeisxlJya8HniJCL-haaqWWKGGiUJh0kJah4QFbKdF7hEXy8BDgyle5G8ijmifz8PhbzEKmV894h93GgKFThFKql2GxyHmiVEzDBDwwUgLVUoAAw04TZo3H-7Eao0BxaGwmoyaAo11E2jw8u1eCAUdCoit2E0vvw5bxB0Ry8Gq0cex2Qi1-BkWx50Awal28Ghwui6AW8byow9wby3C23ikE6yqt2k1GQ260iObxa2yex-1m81KwnE5O1qwRwyH1c4Z0ae02Bm01k5w1sC&__comet_req=7&fb_dtsg=NAcPkzBEXcMoFLTlyQy3eNiLzax2w69zdyAwcx1lB0-qwIxPN1o_RyA%3A17843676607167008%3A1728527552&jazoest=26453&lsd=NEAOb1Z_w5XsSLR8gmCGWm&__spin_r=1017234147&__spin_b=trunk&__spin_t=1728595083&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfileSuggestedUsersWithPreloadableQuery&variables=%7B%22module%22%3A%22profile%22%2C%22target_id%22%3A%22{user_id}%22%7D&server_timestamps=true&doc_id=7871693226285927'
  headers = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'mid=ZwRUWQAEAAEkOkvuteNAO2TdW--K; datr=WVQEZ9otxSdrW3lboj2lt3LI; ig_did=B52CEFC3-E13F-469D-AAAD-5C5C929934B3; ps_l=1; ps_n=1; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; ig_direct_region_hint="VLL\\05449282885844\\0541760048280:01f7399b20e704d7f6a48609d1a2bc4e1e11f0fc10052998f01ec225c4d823c141fb4d30"; csrftoken=UP5Srl1PbIGo2LlwHCRVBIsDYvxD2rSQ; ds_user_id=65086222838; sessionid=65086222838%3AnnvTf7pX8fywZD%3A25%3AAYc6j5j5S7ps1lQTge96zwgvx5EtQx3NImLyTjxTaA; rur="CCO\\05465086222838\\0541760131076:01f7518d34ff734e78af7da82392d72540f9d8479b7afb535a3963f70f9977d95163d078"; wd=827x812; csrftoken=kFP5Pxdr4yd7Jpzd0Be9XJMxAVDWoehc; ds_user_id=65086222838; rur="CCO\\05465086222838\\0541760131450:01f7573baf7ef7d38b1ee05fea78e684c061d99ac345c5a383894933fbdf10b705ed563e"',
    'origin': 'https://www.instagram.com',
    'priority': 'u=1, i',
    'referer': f'https://www.instagram.com/{username}/?hl=es',
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
    'x-csrftoken': 'UP5Srl1PbIGo2LlwHCRVBIsDYvxD2rSQ',
    'x-fb-friendly-name': 'PolarisProfileSuggestedUsersWithPreloadableQuery',
    'x-fb-lsd': 'NEAOb1Z_w5XsSLR8gmCGWm',
    'x-ig-app-id': '936619743392459'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.json())


postes = get_user_posts('YOUR_USERNAME_HERE')

similar_users = get_similar_users('YOUR_USER_HERE', postes[1])

print(similar_users)