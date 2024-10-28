import requests
import csv
import json
from middleware_tk import get_user_cookies, read_json, delete_file, get_queryString, get_user_cookies_values
import time
from datetime import datetime
import pytz

lolazo = None

def get_tiktok_user(username):

   url = f'https://www.tiktok.com/api/search/user/full/?WebIdLastTime=1728178612&aid=1988&app_language=es&app_name=tiktok_web&browser_language=es-419&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F129.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&cursor=0&data_collection_enabled=true&device_id=7422470536956364294&device_platform=web_pc&focus_state=true&from_page=search&history_len=12&is_fullscreen=true&is_page_visible=true&keyword={username}&odinId=7398293910891021318&os=mac&priority_region=MX&referer=https%3A%2F%2Fwww.google.com%2F&region=MX&root_referer=https%3A%2F%2Fwww.google.com%2F&screen_height=900&screen_width=1440&tz_name=America%2FMonterrey&user_is_login=true&web_search_code=%7B%22tiktok%22%3A%7B%22client_params_x%22%3A%7B%22search_engine%22%3A%7B%22ies_mt_user_live_video_card_use_libra%22%3A1%2C%22mt_search_general_user_live_card%22%3A1%7D%7D%2C%22search_server%22%3A%7B%7D%7D%7D&webcast_language=es&msToken=waT6Sy4qpnVSMMaBGJtrKp5RgrMg6fGVlxZCYkdhSZ9v4vHc8lLwVZBTza4mY-mKTfmZVGi2oO3SXGnBS6ZB86Jeao5gArO3h1gEF4iDh66HM02QxfIni0nBFOc4dfCxVekhqRALDNT_bDGcyuw21Lm8&X-Bogus=DFSzswVY070ANj1qtB7oSOIm4L7G&_signature=_02B4Z6wo00001Sm41iAAAIDAyXMd8lWEF1EpuNKAAC1l87'

   payload = {}
   headers = {
   'accept': '*/*',
   'accept-language': 'es-419,es;q=0.9',
   'cookie': 'tt_chain_token=a3rp+Clgceg1A6CA6HL62Q==; delay_guest_mode_vid=5; passport_csrf_token=4075af0f2aa93479a593d1a1c92a84d7; passport_csrf_token_default=4075af0f2aa93479a593d1a1c92a84d7; store-country-code-src=uid; last_login_method=google; _ttp=2n839FwqLfjSWs2zyIBIT3hxxSo; multi_sids=7398293910891021318%3Ae461d7662cbc557a2a5fc427002fed6d; cmpl_token=AgQQAPNGF-RO0raS67q-qp0__WBwkzCJf4TNYNQ4GA; passport_auth_status=3ce19fa6bc422fcf294e9258341d037b%2Cd9e0ab5047ff4e90798cac7a3b0f86e2; passport_auth_status_ss=3ce19fa6bc422fcf294e9258341d037b%2Cd9e0ab5047ff4e90798cac7a3b0f86e2; sid_guard=e461d7662cbc557a2a5fc427002fed6d%7C1728690056%7C15552000%7CWed%2C+09-Apr-2025+23%3A40%3A56+GMT; uid_tt=5d23e1a12d3b8698a987773cf6b6483eda5bf3807fd7f8f87a92f21fadb85a77; uid_tt_ss=5d23e1a12d3b8698a987773cf6b6483eda5bf3807fd7f8f87a92f21fadb85a77; sid_tt=e461d7662cbc557a2a5fc427002fed6d; sessionid=e461d7662cbc557a2a5fc427002fed6d; sessionid_ss=e461d7662cbc557a2a5fc427002fed6d; sid_ucp_v1=1.0.0-KDI4YjEzZTdmYTljZTc1ODllYTQ1MDU3NmM0ODdiMTZmMjg2ZmFhYTgKIQiGiOG006OB1mYQiO-muAYYswsgDDC_irC1BjgIQBJIBBADGgZtYWxpdmEiIGU0NjFkNzY2MmNiYzU1N2EyYTVmYzQyNzAwMmZlZDZk; ssid_ucp_v1=1.0.0-KDI4YjEzZTdmYTljZTc1ODllYTQ1MDU3NmM0ODdiMTZmMjg2ZmFhYTgKIQiGiOG006OB1mYQiO-muAYYswsgDDC_irC1BjgIQBJIBBADGgZtYWxpdmEiIGU0NjFkNzY2MmNiYzU1N2EyYTVmYzQyNzAwMmZlZDZk; store-idc=maliva; store-country-code=mx; tt-target-idc=useast1a; tt-target-idc-sign=ujGv8pPvS_SF7Z1oczLJ6bVFS3y--5ZfVQhdEgf2SQZ8bE3S82U_YYHyX6wD8u6gay5ZCT40EcAFnQt9YK8s0jl8qlAJzRFC6-k5Jo5_v-bO9o3kE6DQSgdExYrDJ6B3AsYYvhMb-HJO6VxufPNh-Gw81pvNioEQZObtwo_yCzf6ofOtqvxsNL2cFdJ7ev8ChdJx4nN-jRMJbyzqaksYNzAN65rgtCcUdR25W4FH4hSwWRydf4g4Ak5IupdmA0cL4yY3kZmvI6gdP7AmE72L301EyfR8oXfbUH2ISDyq3emgptW9czyAQ0I3gVUHT-0-v8Kmb1WfAvR6ebhPf37Gim49ZFDVvjRQCr4HEafpfaeXvxMI15j8eC9rh_pABxK57JWQ3d8Iz6JCYgH5k9xsA81Y13se_1nreF3sMSay6y36MqXLb-CA7swK4nOZjBm8G5WMgk02OclpO7wNqTVDzgUWo59gF43BSRDVaHqiwwUykaGKOc6Z_0aQ6UB5PPCe; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; tt_csrf_token=pydkJoK0-NeS5XrgJ0rxRvrlbHBpIRQ3koXU; ak_bmsc=F0E152A76767A3604D1DEF8FB3CA8900~000000000000000000000000000000~YAAQlygcuGX0pYGSAQAAnAJGiBkEhSDISpiuBuqIZfc5AoFyXZXpmFhgHGVpg1a3udbw2FjKXnBfpBVO4zKVpdZ2P5rHsq4o7e4qYRbo7amiq8ERSHnchbUfimYwPJNkDqzuR7NJ1/yGfRY90vFjiB+eHQICb2zPgozq2MO7a67iQ+hkNCgBNlE6rti4m+I46MVsGMeUtIbA6RGksHduhgnjDa6ueKJTE9Y+rhl1b6xCkmDlWXMA9tWZGR6tnnaXsOFb0xNlopmD8kAKK1W+uYudpSNIJdybYO2eNg0nbGhtV5ShiUQhRSdzO6E3MUZ9U8YYFM3x0XFY2oz44O6LRzYduIUWD5OLlqs6hkvj21fGi5OlpEtq3/Ij2CG2viHrIzy1MXeQwGcibw==; bm_sv=967C1838A93A64C255A79C092B65F080~YAAQkSgcuKprSnySAQAA83NhiBlv2d7A/8nmbyrI2hQH7eUo8yHKWzI4aGJTNZI+hnbKIaRON3w+Dp2QCdyNstuXLj7qldgr+njBkNE6OXVLCZKGqH1GYV/ypv4wgZkuu+6u6RhaTqo/OjwxouWj3fRZcuIlQnf0X7UHn3OGrZ3jXyRu8vjz73WgzUGjZt+hjXWqqkq+oiXGfsL9lrPh2eK8iFaJB0DaDwg/9mRu8/6UOcMfWDsqTRQvKUrPZWS0~1; passport_fe_beating_status=true; ttwid=1%7CCfpB8i4ul6kmCIOwyorYXVEM-NSETzbrhXBxm_CFeew%7C1728864942%7C10f53ac7c38a1bb3d97725d2a15f310c9436b6a92f2d756e2a8c3b45ca1e9615; odin_tt=11ac96136739eb7913e3416eeefd1d48435c07fe70008ee5c7268e7e23221b0a5c9d299e7a940dc675aafcede075e552b8a7c275c29bc72c8f99fb0a9ca6f47f0b6fa9f36039450b4b986a99ec0fc5cb; perf_feed_cache={%22expireTimestamp%22:1729036800000%2C%22itemIds%22:[%227400876178501799174%22%2C%227422647948070210821%22%2C%227423180872578239750%22]}; msToken=FDn4jKMojRhboxzARe9_gmUm7bBsZwp__Gj0Es8FR4NpHW90_Baj4nNWfqzODV7CAaWeXPo53fvrEDgar8ilLYs0SssTCBeS7tVfJAWzEdQTw7n9XjLdqyOaCAtuwxqRq3m8CX686muQD0GTypvOemWi; msToken=waT6Sy4qpnVSMMaBGJtrKp5RgrMg6fGVlxZCYkdhSZ9v4vHc8lLwVZBTza4mY-mKTfmZVGi2oO3SXGnBS6ZB86Jeao5gArO3h1gEF4iDh66HM02QxfIni0nBFOc4dfCxVekhqRALDNT_bDGcyuw21Lm8; msToken=wO6FLrwZ95f4iKQxqrJ2ELS9Pif_gWL3BjfgN8RBES7A__qdNqY1zvp8AM0QMe3ylu3p42IWRekWT5C16pdzOltoHqwGhzdbqHnajqIX1TXCMaiJjqbnEbjeAs6BYwakPvxQkKpQOGublGhXrlPK2JRd; odin_tt=23fd3b29c150ff1a2f48c8717ace2bfe8ac320eb8e2e447e766dbbeb852339c4217e09829913d7396f34fcb9c062ce4f78c36ec633286ef6a418cb705a69e2279577e944aa7132914c67a5f6ecf06593; store-country-code=mx; store-country-code-src=uid; store-idc=maliva; tt-target-idc=useast1a',
   'priority': 'u=1, i',
   'referer': f'https://www.tiktok.com/search/user?q={username}&t=1728864923259',
   'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"macOS"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
   }

   response = requests.request("GET", url, headers=headers, data=payload)
   r = response.json()

   users_found = r['user_list']

   unique_id = None

   for user in users_found:

      if username == user['user_info']['unique_id']:

         unique_id = user['user_info']['unique_id']
         follower_count = user['user_info']['follower_count']
         profile_link = f'https://www.tiktok.com/@{username}'

   
   if unique_id is not None:
      
      return username, follower_count, profile_link
   else:
      print('Sorry!, user not found :C')
   
   
def get_video_comments(username, id):

   url = f"https://www.tiktok.com/api/comment/list/?WebIdLastTime=1728178612&aid=1988&app_language=ja-JP&app_name=tiktok_web&aweme_id={id}&browser_language=es-419&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F130.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&current_region=JP&cursor=0&data_collection_enabled=true&device_id=7422470536956364294&device_platform=web_pc&enter_from=tiktok_web&focus_state=true&fromWeb=1&from_page=video&history_len=9&is_fullscreen=true&is_non_personalized=false&is_page_visible=true&odinId=7398293910891021318&os=mac&priority_region=MX&referer=&region=MX&screen_height=900&screen_width=1440&tz_name=America%2FMonterrey&user_is_login=true&webcast_language=es&msToken=Zx5X79YzD6_GOmBSYaFjWHPiIgCuEpTXTBcC2EccfCz6xD7-6fZnqp2BJkCtJXGlyZyz34qnjwp50tatKNYNwP_4JRmhUnehpN9tSLhjItqJRd0-YvwuEZpJUwpnTvZs_wI2nka8caRNPLCyxcnlccRu&X-Bogus=DFSzswVYH7GANjrztQNM2ELNKBT-&_signature=_02B4Z6wo00001R8MZ2AAAIDCTfNHeYrfqaEfDGPAACDh5b"

   payload = {}
   headers = {
   'accept': '*/*',
   'accept-language': 'es-419,es;q=0.9',
   'cookie': 'tt_chain_token=a3rp+Clgceg1A6CA6HL62Q==; delay_guest_mode_vid=5; passport_csrf_token=4075af0f2aa93479a593d1a1c92a84d7; passport_csrf_token_default=4075af0f2aa93479a593d1a1c92a84d7; store-country-code-src=uid; last_login_method=google; _ttp=2n839FwqLfjSWs2zyIBIT3hxxSo; multi_sids=7398293910891021318%3A5803ccf7963c0aa6bcba8da2929ec88f; cmpl_token=AgQQAPNGF-RO0raS67q-qp0__WBwkzCJf4TNYNQuuw; passport_auth_status=bfd1cfabe87a783e79b1fa45d72987bd%2C3ce19fa6bc422fcf294e9258341d037b; passport_auth_status_ss=bfd1cfabe87a783e79b1fa45d72987bd%2C3ce19fa6bc422fcf294e9258341d037b; sid_guard=5803ccf7963c0aa6bcba8da2929ec88f%7C1729018505%7C15552000%7CSun%2C+13-Apr-2025+18%3A55%3A05+GMT; uid_tt=0adc6b2a2da3a84728542b6b93a105a7d273bde0eb06493c1eb45020b8adb6c2; uid_tt_ss=0adc6b2a2da3a84728542b6b93a105a7d273bde0eb06493c1eb45020b8adb6c2; sid_tt=5803ccf7963c0aa6bcba8da2929ec88f; sessionid=5803ccf7963c0aa6bcba8da2929ec88f; sessionid_ss=5803ccf7963c0aa6bcba8da2929ec88f; sid_ucp_v1=1.0.0-KDM5Nzc3ODBkOTZlMmVlZjEzNmMzY2FhZTY0ZThhNDk2ZTU4Nzg1NDUKIQiGiOG006OB1mYQifW6uAYYswsgDDC_irC1BjgIQBJIBBADGgZtYWxpdmEiIDU4MDNjY2Y3OTYzYzBhYTZiY2JhOGRhMjkyOWVjODhm; ssid_ucp_v1=1.0.0-KDM5Nzc3ODBkOTZlMmVlZjEzNmMzY2FhZTY0ZThhNDk2ZTU4Nzg1NDUKIQiGiOG006OB1mYQifW6uAYYswsgDDC_irC1BjgIQBJIBBADGgZtYWxpdmEiIDU4MDNjY2Y3OTYzYzBhYTZiY2JhOGRhMjkyOWVjODhm; store-idc=maliva; store-country-code=mx; tt-target-idc=useast1a; tt-target-idc-sign=T5P0nLa__cUlAufJC-yvMveX0L1dMaeNfMAiRRqG4RTQd9dru_mtnje89EAiyFGd_xtaW6_Cbj8XiHNTB2DQYULlJL-73fMRO5KxdZ30RoTAp-oUkHm0hPeYDLrCDHeWvllu9SW0wmE3oDfn_D9ZmuZUwdeNY1X72jecdQM7NpNkqZWMH1s7D1NX1__LMcDRvRsXaWE0swEBYHOCGeStm_S0tAiPOKX8qHqG_s9vtuEg8_YMHptjpPy9FQx3FpN4gRLazaQjvGcqInGkqFsM7oYfRwPk4q-7u1XazKB1y9mVTjXTvN3pyj409FV2zPFnaQe4RK87abIdwXgfiWfN5trAYbzdc_fboghqtKBN3fc1RmQ-QjCpe_zzeGETJpXdVpT9k3W8b3JAvnYRD-423V0vtsJvjCnp3drT9K-mx5xgF_YxMT0SYgLYEtFs1pXwr1VAmIiWgaHgY6Gi-KB5o_vBZhaBF1LTWW1HFo86ihTeW0BPxJlwJO253m62nHsy; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; tt_csrf_token=nvwQUkrJ-VqeJ0f6LwdX6_vC9z9KKiUEZL7U; ak_bmsc=09703F4E56E4C26B9681BB6A1A8F3E51~000000000000000000000000000000~YAAQZXlAFzMVN8GSAQAAXb08xRnDoyFr0+TP/0sjI3Q8kNbXVg2sPJkf3zyMN9Te6D5EpVUxfiOUnCwO2zvd5ZiDG2xWzsjSJcf+esyfulh7bBaH7BKP/ae3F0UBhpMzfX1GIIJCW/Y1SnOsdgCFVl039IWqdZ0xa/EmSNQiHXDa5o6QTM6XIVRy3pB7D98miYBNNyXF/S8P7/9qHSAGN5HTBjeP4I/Wwy58M0lzGAdIGU8mtYyNQtQkAtQB3F36HAYMITZzVCtTRP8AA1d7+Ji4IR8b4sBx1A3MmedNl2bYBZnNBXbhtVPUJrVxyKvyIYPWAH6uAgHCROBl2X0EgnGLcrVXwCX86sFALh08FFkjIHh3QhOEJRyaaxDkXSuG60nnEBo/KEcXuA==; passport_fe_beating_status=true; odin_tt=33a4abb9d6d5c1af7d460e1b2a893bdd95fb17b19d89cbb79d091f6b10fa1b7d7001ab3ecd4d33e4ff1584c4dd55e30ca1b30e3a9b36f7b971cb2127d4b020eaa7292074ab4b5e0b27af590b0b051b42; bm_sv=AB9A9F8A5DD3742D65DC78FE20C045D8~YAAQV3lAFyTfbcCSAQAAFYCJxRngkea33wZrmHUiaatQzF3dOeeDXgFiwFDvUqlOeskOSBYtVfi23fcyYtlTO8Fopb0NCST63WJPn+G/Gad8RnrMILBRtA22xAouoAeMooXhz/U+HkKTYjHygVpctSLgb3P/TQMWD1diYVG45R86MVMyAYuQUf/OYxgSra0FsJ5x93xOPBxKrUCPHTCxXez1Jw2jdEq+QjWQSVjFjAvUttj0voPR9tzinpnAX6AE~1; ttwid=1%7CCfpB8i4ul6kmCIOwyorYXVEM-NSETzbrhXBxm_CFeew%7C1729890977%7Cd09382771fea37fa2c0617068bfcb5f7866edea8162aba8e15b23890570ecaca; msToken=-ff5irTSHB6OL4moCx2E_-F4GRA2Bl7hNh7Wk5vVRvKWexTloqw5gNNtzSRV9DBQo_85iCbjtkXg6kMn9XlT2C3i8RMKP8LXJ-bEEKiEqPXPfJ349OHZk-xr5HIfqirDuglEtPQ2VZuPmNMpRzIT3s22; msToken=Zx5X79YzD6_GOmBSYaFjWHPiIgCuEpTXTBcC2EccfCz6xD7-6fZnqp2BJkCtJXGlyZyz34qnjwp50tatKNYNwP_4JRmhUnehpN9tSLhjItqJRd0-YvwuEZpJUwpnTvZs_wI2nka8caRNPLCyxcnlccRu; msToken=6vItUDRj3uA8wEo0lo4echjMic_rUxSH-At8QIMOqw3J9CoA5q1KzA1-Jsqj9J6eccwyZlGwD8jxYJ3Yeh1fm2RP32j2OGQEFuBzMlYfVr9F7jq-U6WppmP6oBnJAvF5Qtknzj3Df8ibW_PX8kOSjcsc; odin_tt=1f5f17f3994b3d8b4f2c2bb696eedcb08dd3c1c4b63231e18c4106c8c7885b686206b1405fbf59fc0e8b3500425e1d2c7250b1044efa76514ccafc24ac66c55884836b8467e43c1e856013ac5a9d0753; store-country-code=mx; store-country-code-src=uid; store-idc=maliva; tt-target-idc=useast1a',
   'priority': 'u=1, i',
   'referer': f'https://www.tiktok.com/@{username}/video/{id}',
   'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"macOS"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
   }

   response = requests.request("GET", url, headers=headers, data=payload)

   r = response.json()

   cments = r['comments']
   comments = []

   for comment in cments:
      text = comment['text']
      user = comment['user']['nickname']

      comments.append({'user_that_commented': user, 'text': text})
   
   return comments


def get_user_posts(username, url):

   payload = {}
   headers = {
  'Accept': '*/*',
  'Accept-Language': 'es-419,es;q=0.9',
  'Connection': 'keep-alive',
  'Cookie': 'tt_chain_token=a3rp+Clgceg1A6CA6HL62Q==; delay_guest_mode_vid=5; passport_csrf_token=4075af0f2aa93479a593d1a1c92a84d7; passport_csrf_token_default=4075af0f2aa93479a593d1a1c92a84d7; store-country-code-src=uid; last_login_method=google; _ttp=2n839FwqLfjSWs2zyIBIT3hxxSo; multi_sids=7398293910891021318%3A5803ccf7963c0aa6bcba8da2929ec88f; cmpl_token=AgQQAPNGF-RO0raS67q-qp0__WBwkzCJf4TNYNQuuw; passport_auth_status=bfd1cfabe87a783e79b1fa45d72987bd%2C3ce19fa6bc422fcf294e9258341d037b; passport_auth_status_ss=bfd1cfabe87a783e79b1fa45d72987bd%2C3ce19fa6bc422fcf294e9258341d037b; sid_guard=5803ccf7963c0aa6bcba8da2929ec88f%7C1729018505%7C15552000%7CSun%2C+13-Apr-2025+18%3A55%3A05+GMT; uid_tt=0adc6b2a2da3a84728542b6b93a105a7d273bde0eb06493c1eb45020b8adb6c2; uid_tt_ss=0adc6b2a2da3a84728542b6b93a105a7d273bde0eb06493c1eb45020b8adb6c2; sid_tt=5803ccf7963c0aa6bcba8da2929ec88f; sessionid=5803ccf7963c0aa6bcba8da2929ec88f; sessionid_ss=5803ccf7963c0aa6bcba8da2929ec88f; sid_ucp_v1=1.0.0-KDM5Nzc3ODBkOTZlMmVlZjEzNmMzY2FhZTY0ZThhNDk2ZTU4Nzg1NDUKIQiGiOG006OB1mYQifW6uAYYswsgDDC_irC1BjgIQBJIBBADGgZtYWxpdmEiIDU4MDNjY2Y3OTYzYzBhYTZiY2JhOGRhMjkyOWVjODhm; ssid_ucp_v1=1.0.0-KDM5Nzc3ODBkOTZlMmVlZjEzNmMzY2FhZTY0ZThhNDk2ZTU4Nzg1NDUKIQiGiOG006OB1mYQifW6uAYYswsgDDC_irC1BjgIQBJIBBADGgZtYWxpdmEiIDU4MDNjY2Y3OTYzYzBhYTZiY2JhOGRhMjkyOWVjODhm; store-idc=maliva; store-country-code=mx; tt-target-idc=useast1a; tt-target-idc-sign=T5P0nLa__cUlAufJC-yvMveX0L1dMaeNfMAiRRqG4RTQd9dru_mtnje89EAiyFGd_xtaW6_Cbj8XiHNTB2DQYULlJL-73fMRO5KxdZ30RoTAp-oUkHm0hPeYDLrCDHeWvllu9SW0wmE3oDfn_D9ZmuZUwdeNY1X72jecdQM7NpNkqZWMH1s7D1NX1__LMcDRvRsXaWE0swEBYHOCGeStm_S0tAiPOKX8qHqG_s9vtuEg8_YMHptjpPy9FQx3FpN4gRLazaQjvGcqInGkqFsM7oYfRwPk4q-7u1XazKB1y9mVTjXTvN3pyj409FV2zPFnaQe4RK87abIdwXgfiWfN5trAYbzdc_fboghqtKBN3fc1RmQ-QjCpe_zzeGETJpXdVpT9k3W8b3JAvnYRD-423V0vtsJvjCnp3drT9K-mx5xgF_YxMT0SYgLYEtFs1pXwr1VAmIiWgaHgY6Gi-KB5o_vBZhaBF1LTWW1HFo86ihTeW0BPxJlwJO253m62nHsy; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; tt_csrf_token=ef08ZCen-W-f1qOBRLt80l9UocyCLiqYKD20; ak_bmsc=782E47B3EF8654E8DA7E684714D24C4F~000000000000000000000000000000~YAAQ0wzGFyUkbrWSAQAAlwnjvBnwhoy63CnL4HmoiW0GE7941iEe2ylaokYGhFTMpXb5Gf54yLhIOyyOCQVftwYFULDrxEutQc2jrh/pBWV3Jiwfj+SEuSyqN1Y6P9Q9nJ2AHy6P4x560wjf6qcwqQpL3jG2tf6b+YoMR1FNx3azVRTDwPBHi0UeUZeDP5APWIicjPyhc+DzZJzGcjDs6MOZWhkgVajAtQNZd2NOJgdl9fS7Xk+doJRDyE0smLCOm6aLs6k/MXgvi5fm1bHgC//hWmIyi0pPOBMYN0fJkbARRJEZpSx5utexCGH7a2PKZ+XiRIANK4E/ThTvZruHTSFhKV34zQR6y5/bQCnGIXJLgwnoQD8vvBqowQFyk1/p; msToken=EYBy2DYwNKGeJCJrjd2WBhoN7lc8W0DFm566IOPizuSwXZwstVMrKUBuzPP490C3yGAYmOrZByNa1Xh4FJ4zIqY8-5srqpjn0oUEBaTpgfT5X3VE6ZV3sH5KnZKJGKz9qdJ6jZdXyaEYBxo=; msToken=lzEsyVTi106IYEEsA02pVurfQpE8naa9vCI9h81uyjuLAQ05sFz8siqr1KtMN5oSAtXJ6uTyT9Z2JBEH5aTfQLFtl7467V6NBywRxDZJIk_HhXzN9IFaWgUjH44pW43jTXJhtfm5N8Dbdp0=; bm_sv=8EAC532582BDB9977CBD96F1FBEAEE1B~YAAQzwzGFyPcarWSAQAAl9/rvBnzS74glf9uBiZjPw2UcH6bK5vIiJdLmQqE/Cj16xM9eX1dsyVb+Uw2klpk4Q5HxQF49V3uaoe1i2HHCwgJZFRH4QL2mJXMbKqWKioDaAEyYc/sfu6V48dTCAS13QffydCHDvMwI98kcLxyZzL12tDGyinh3kAivKACeO2gx4Lz1MCE63zvHAnPh/hC4ksBS+LbT9qk/bEDwwbJ0Rq+zPq0AQO2N28aW98Bp7Uo~1; passport_fe_beating_status=true; ttwid=1%7CCfpB8i4ul6kmCIOwyorYXVEM-NSETzbrhXBxm_CFeew%7C1729746428%7C3ce798e739dd3c53d088b1a87baa6ddf68137f03f09e810766aef14d336cd2ad; odin_tt=6c67c245393123afedbea2de794a1044743065b83da260353d7500cde0e55fecdc6528186ccfbea530a061bb7127eabf224e92a4e18649133d15058d7b681dfd; msToken=fvH0Yi6f8EJkuY-5Xt1b5vpWT_r8StNj8MrIV6EUWJlbdJXxHlBdo5bti6dJHzThX0Rai1XYRup1Z6o5Q-7GfB273ncsdnwI9hlkAkFSDNUK66zukeiuDYUN2emngkFRn7IewgcJTRrXJrEtIw==; odin_tt=1f5f17f3994b3d8b4f2c2bb696eedcb08dd3c1c4b63231e18c4106c8c7885b686206b1405fbf59fc0e8b3500425e1d2c7250b1044efa76514ccafc24ac66c55884836b8467e43c1e856013ac5a9d0753; store-country-code=mx; store-country-code-src=uid; store-idc=maliva; tt-target-idc=useast1a',
  'Referer': f'https://www.tiktok.com/@{username}',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"'
}

   response = requests.request("GET", url, headers=headers, data=payload)

   try:
      r = response.json()
   except:
      return "No data retrieved"

   return r


def read_logs(username):
   i = range(1,10)

   for x in i:

      try:
         with open(f'{username}_output_link_{x}.json', 'r') as f:

            filename = (f'{username}_output_link_{x}.json')

            print(filename) 
            time.sleep(3)

            content = f.read()
                
            # Check if the content is not 'No data retrieved'
            if content.strip('"') != 'No data retrieved':
               
               lolazo = str(content)

               return lolazo

            else:
               print('no return in here')

      
            
      except FileNotFoundError:
            print(f'File {username}_link_{x}.json does not exist')
      except json.JSONDecodeError:
            print(f'Error decoding JSON from file {username}_link_{x}.json')
      except Exception as e:
            print(f'An error occurred: {e}')


def get_tiktok_stats(username):

   data = []

   links = get_queryString(username)

   i = 1
   for link in links:
      file = get_user_posts(username, url=link)

      with open(f'{username}_output_link_{i}.json', 'w') as f:
         json.dump(file, f)
      i += 1

      time.sleep(3)

   lolazo = read_logs(username)

   json_file = json.loads(lolazo)
   
   items = json_file['itemList']

   for item in items:
      caption = item['desc']

      id = item['id']
      print(id)
      print(caption)

      like_count = item['statsV2']['diggCount']
      print(like_count)

      comment_count = item['statsV2']['commentCount']
      print(comment_count)

      comments = any
      comments = get_video_comments(username, id)

      print(comments)

      created_at_num = item['createTime']
      created_at = datetime.fromtimestamp(created_at_num, tz=pytz.UTC)
      print(created_at)

      data.append({
         "post_id": id,
         "caption": caption,
         "like_count": like_count,
         "comments_count": comment_count,
         "comments": json.dumps(comments) if isinstance(comments, (dict, list)) else comments,
         "created_at": created_at})

   return data


def main():
   #user = input('introduce yout tiktok account: ')
   #get_tiktok_stats(user)
   pass


# Entry point ------------>

if __name__ == '__main__':
   main()