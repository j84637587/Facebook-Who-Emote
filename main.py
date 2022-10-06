import requests
import time # prevent dos attack detection
import json
import re
from typing import Optional

__COOKIE = f"sb=AAwZYkxTgYeKf7OC4sElnUI1; m_pixel_ratio=1; c_user=100001118268433; datr=iI_0YmeRozoCy0xhKTmoklmj; m_page_voice=100001118268433; dpr=0.8999999761581421; wd=1218x784; x-referer=eyJyIjoiLzEwMDA2Nzc2OTc4NjQzNi9wb3N0cy9wY2IuNDMzMjcwODA4OTQxOTA4Lz9waG90b19pZD00MzMyNzA2OTU2MDg1ODYmbWRzPSUyRnBob3RvcyUyRnZpZXdlciUyRiUzRnBob3Rvc2V0X3Rva2VuJTNEcGNiLjQzMzI3MDgwODk0MTkwOCUyNnBob3RvJTNENDMzMjcwNjk1NjA4NTg2JTI2cHJvZmlsZWlkJTNEMTAwMDAxMTE4MjY4NDMzJTI2ZWF2JTNEQWZZT0NWRy1ieTZ6eFREaW0zbVVKeDk0RXlzYktXdHViYW9ibEJqZ3JyV0FsOENZU3Zod0QyMFNRT0g4T1BKUnlMTSUyNnBhaXB2JTNEMCUyNnNvdXJjZSUzRDQ4JTI2cmVmaWQlM0Q1MiUyNl9fdG5fXyUzREVILVIlMjZjYWNoZWRfZGF0YSUzRGZhbHNlJTI2ZnRpZCUzRCZtZHA9MSZtZGY9MSIsImgiOiIvMTAwMDY3NzY5Nzg2NDM2L3Bvc3RzL3BjYi40MzMyNzA4MDg5NDE5MDgvP3Bob3RvX2lkPTQzMzI3MDY5NTYwODU4NiZtZHM9JTJGcGhvdG9zJTJGdmlld2VyJTJGJTNGcGhvdG9zZXRfdG9rZW4lM0RwY2IuNDMzMjcwODA4OTQxOTA4JTI2cGhvdG8lM0Q0MzMyNzA2OTU2MDg1ODYlMjZwcm9maWxlaWQlM0QxMDAwMDExMTgyNjg0MzMlMjZlYXYlM0RBZllPQ1ZHLWJ5Nnp4VERpbTNtVUp4OTRFeXNiS1d0dWJhb2JsQmpncnJXQWw4Q1lTdmh3RDIwU1FPSDhPUEpSeUxNJTI2cGFpcHYlM0QwJTI2c291cmNlJTNENDglMjZyZWZpZCUzRDUyJTI2X190bl9fJTNERUgtUiUyNmNhY2hlZF9kYXRhJTNEZmFsc2UlMjZmdGlkJTNEJm1kcD0xJm1kZj0xIiwicyI6Im0ifQ%3D%3D; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1664913485360%2C%22v%22%3A1%7D; xs=36%3AC2rd8vycJ4a-BA%3A2%3A1660194695%3A-1%3A11299%3A%3AAcXxqnCetfCeT2mVxkzz4iVm_N1uBA1UziqYyoPMkSXJ; fr=0ohzYKYOALumA9KfD.AWWYM8t-f1n9tP7JlNc0WK98g88.BjPJMd.1w.AAA.0.0.BjPJMd.AWVUTvGWCrk" # COOKIE
__USER = re.search(r"c_user\=(\d*)\;", __COOKIE, re.MULTILINE).group(1) # cookie.c_user

API_URL = f"https://www.facebook.com/api/graphql/" # api url

# 用於GET html
html_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-TW,zh;q=0.8",
    "cache-control": "no-cache",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": __COOKIE,
  }

# 用於POST API
api_headers = {
    "accept": "*/*",
    "accept-language": "zh-TW,zh;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": __COOKIE,
  }

session = requests.Session() # session

def getTabApiBody(targetId:str, cursor: str) -> str:
    """取得用於 Tab API 的資料.

    Args:
        targetId (str): 文章 targetId 資料.
        cursor (str): cursor 資料.

    Returns:
        str: 用於 Tab API 的資料.
    """
    body = f"av={__USER}" \
    f"&__user={__USER}" \
    "&__a=1" \
    "&__dyn=7AzHJ16U9ob8ng5K8G6EjBWo2nDwAxu13wsongS3q2ibwyzE2qwJyEiwsobo6u3y4o2Gwn82nwb-q7oc81xoswMwto88422y11xmfz83WwgEcHzoaEnxO0Bo7O2l2Utwwwi831wiEjwZwlo5qfK6E7e58jwGzEaE5e7oqBwJK2W5olwUwOzEjUlDw-wQ-261eBx_y88E3VBwJCwLyES0Io88cA0z8c84qifxe3u362-2B0" \
    "&__csr=gkMuhAJgYwZ96gGIQn5PNklfFsiLtayeYziYTr8pVlluWFGGrDGIzRiF4VehK_AV7ldkigxeiaVCFA-tqgDQKlpqoECjK8xquqqUOiF8OaBBCXxyEkCyVGAyFFHBjjx-dzUlF6XG6rCxem4qyVpUO4Q5onx2cxq-aG1fyUS6UjwEwIxiuiu3q9wPwRxO2q6EC6E-u9wjUboC8yEmwg8Ze4oe8nws8owWDwJz8do6C6oiwFxa4Egzodawmo5u13wmU4S0vq0gR02eU0Du046o0Fq1Tg1PE0bgU0cOE0dsU0aso3Cw11W0m206IQ09Mw1lm04BU42i4u6o4O9zE0tpwa-i1Kw1xm0e_w1Cx0h80DK4obE2pwbq08tw" \
    "&__req=5w" \
    "&__hs=19269.HYP%3Acomet_pkg.2.1.0.2.1" \
    "&dpr=1" \
    "&__ccg=GOOD" \
    "&__rev=1006321469" \
    "&__s=a6wsfx%3Axw1jo4%3A6q8jll" \
    "&__hsi=7150748944671857447" \
    "&__comet_req=15" \
    "&fb_dtsg=NAcNeDVwCftLvh29GPczMmdMePi5_jQdBnjZYqKv7dRpH0UJFodQL8Q%3A36%3A1660194695" \
    "&jazoest=25558" \
    "&lsd=dIvBwYcHZAnhq9irz2mtil" \
    "&__spin_r=1006321469" \
    "&__spin_b=trunk" \
    "&__spin_t=1664913479" \
    "&fb_api_caller_class=RelayModern" \
    "&fb_api_req_friendly_name=CometUFIReactionsDialogTabContentRefetchQueryStable" \
    f"&variables=%7B%22count%22%3A10%2C%22cursor%22%3A%22{cursor}%22%2C%22feedbackTargetID%22%3A%22{targetId}%22%2C%22reactionID%22%3Anull%2C%22scale%22%3A1%2C%22id%22%3A%22{targetId}%22%7D" \
    "&server_timestamps=true" \
    "&doc_id=8694153690610820"
    return body

def getPageApiBody(targetId:str) -> str:
    """取得用於 Page API 的資料.

    Args:
        targetId (str): 文章 targetId 資料.

    Returns:
        str: 用於 Page API 的資料.
    """
    body = f"av={__USER}" \
    f"&__user={__USER}" \
    "&__a=1" \
    "&__dyn=7AzHJ16U9ob8ng5K8G6EjBWo2nDwAxu13wsongS3q2ibwyzE2qwJyEiwsobo6u3y4o2Gwn82nwb-q7oc81xoswMwto88422y11xmfz83WwgEcHzoaEnxO0Bo7O2l2Utwwwi831wiEjwZwlo5qfK6E7e58jwGzEaE5e7oqBwJK2W5olwUwgojUlDw-wUwxwjFovUy2a0-pobpEbUGdwb6223908O3216AzUjwTwNwLwFg" \
    "&__csr=gT2A64p4lEBR4OEalnN5lmyMyyunW6isD9FimX4RO95tAcAXF4WylmF6rhEJBbIFKmF9oV5pF5DQF5AKi9yqgy9oGCUF3XBgEwCFUycKu5EeGXyGwLDy9o8Ukxq58aEbXxCbG6ogxq3Kdxa7UcU6q3m22dwFyU5W1Mxy589oaF87G5obo2iwhEdo8oa89E5K1axObwywUzoK1Lw961lw1Ki0aWw3_83jwfW00UCA0-81nU091U2Bo093E0nTw2oE08980Yi045o2izU1pE" \
    "&__req=13" \
    "&__hs=19270.HYP%3Acomet_pkg.2.1.0.2.1" \
    "&dpr=1" \
    "&__ccg=GOOD" \
    "&__rev=1006322236" \
    "&__s=7nxpbq%3Ab2cipy%3Aitiraf" \
    "&__hsi=7150870177793773204" \
    "&__comet_req=15" \
    "&fb_dtsg=NAcNJ_LNmi9f6VwL2utggsQI-LLgmbX2cY4QVVof5LXLHSTm20N74wQ%3A36%3A1660194695" \
    "&jazoest=25332" \
    "&lsd=O24Uu0QqracrFPKSktog9r" \
    "&__spin_r=1006322236" \
    "&__spin_b=trunk" \
    "&__spin_t=1664941706" \
    "&fb_api_caller_class=RelayModern" \
    "&fb_api_req_friendly_name=CometUFIReactionsDialogQuery" \
    f"&variables=%7B%22feedbackTargetID%22%3A%22{targetId}%22%2C%22scale%22%3A1%7D" \
    "&server_timestamps=true" \
    "&doc_id=5635592226502296"
    return body

def getTargetID(url: str) -> str:
    """取得指定文章的TargetID.

    Args:
        url (str): 指定文章的網址.

    Returns:
        str: 如果有返回TargetID, 否則空字串.
    """
    regex = r"\"story\"\:\{\"feedback\"\:\{\"id\"\:\"([a-zA-Z0-9=]*)\"\}\,\"id\""
    r = session.get(url, headers=html_headers)
    matches = re.search(regex, r.text, re.MULTILINE)
    if matches is None:
        return ""
    return matches.group(1)

nodes = {}

def updatenNodes(reactors: dict) -> Optional[str]:
    """更新當前紀錄,
    並且檢查是否還有紀錄要更新,
    有就返回cursor反之None.

    Args:
        reactors (dict): 要更新的資料.

    Returns:
        Option[str]: 如果還有還有紀錄就返回cursor反之None.
    """
    # Update
    for edge in reactors['edges']:
        node = edge['node']
        nodes[node['id']] = {
            'name': node['name'],
            'profile_url': node['profile_url'],
        }

    # Get next cursor
    page_info = reactors['page_info']
    return page_info['end_cursor'] if page_info['has_next_page'] else None

def fetchWhoEmote(targetId: str) -> None:
    """請求與表情符號相關的資料.

    Args:
        targetId (str): 文章的targetId.

    Raises:
        ValueError: 請求出現錯誤時拋出.
    """
    cursor = ""
    round = 0
    while True:
        body = getPageApiBody(targetId) if cursor == "" else getTabApiBody(targetId, cursor)
        r = session.post(API_URL, headers=api_headers, params=body)
        if r.status_code == requests.codes.ok:
            if cursor == "": # cursor 為空字串表示是第一次取得, 且第一次使用的API不同.
                reactors = r.json()['data']['node']['comet_reactions_dialog_tab_content_renderer']['feedback']['reactors']
            else:
                reactors = r.json()['data']['node']['reactors']

            cursor = updatenNodes(reactors) # 更新紀錄
            print(f"Round: {round}")
        else:
            raise ValueError(f"Error request  url: {API_URL} body: {body}")
        time.sleep(0.5)
        round += 1
        if cursor is None:
            break


if __name__ == "__main__":
    # post_url = "https://www.facebook.com/story.php?story_fbid=pfbid02KncazrqyTJPMmrP5MPuad73s9xH8mRrsTWkvGLrtrKi43sir9BC163nNFcfUfRRVl&id=100067769786436"
    # post_url = "https://www.facebook.com/permalink.php?story_fbid=pfbid0TpqK6WM7wEGJFTV35gRN4WSRXaD779PT7EpxpSrvzEJRmmMWCkiVLqnrUvx9JLLQl&id=100067769786436"
    post_url = "https://www.facebook.com/TWCDC/posts/pfbid0tqufrb9h2BUZyPb7LwF2tBwMSt4q3UAwawmCPFUxW1mWgbsVC6DsKKhRHUSYLK5Al"

    targetId = getTargetID(post_url)
    fetchWhoEmote(targetId)
    print(f"Total: {len(nodes)}")
    json_str = json.dumps(nodes,ensure_ascii=False , indent=4)
    file = open(f"{targetId}.json", "w", encoding='utf-8')
    file.write(json_str)
    file.close()
    print(f"Done! Save to path: {targetId}")