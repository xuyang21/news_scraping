import requests
from bs4 import BeautifulSoup

washington_post_homepage_url = 'https://www.washingtonpost.com/'
washington_post_homepage_cookie = {
    'wp_devicetype': '0',
    'wp_ak_signinv2': '1|20230125',
    'wp_ak_om': '1|20230731',
    'wp_ak_wab': '0|1|1|1|0|1|1|1|0|20230418',
    'wp_ak_v_mab': '0|0|0|1|20231130',
    'wp_geo': 'HK||||INTL',
    'ak_bmsc': '3DF42D0A5CE61C9374C942E9EF911FB4~000000000000000000000000000000~YAAQDpZUaLGPEfWMAQAAMzZZJhaYG9rG2dc9rDg3hlwFLli4JRO9NJIQs8rywcp/ks14revjlqF7gaEgLAdDxXwQtoW0YCMxIohF6VWptZrgpSGoXrBlXqc2yCUjcinJedQjWduYdAFbJ+sDRYEVNirF69A/zd/VIbyYZg+/Nc7C8PMqrAe4c1NuxO1wLB8+ZwXtFCT5bpGPkZj3dFc32kqCmaG0lBElV0LuJm+xIC6rf69YrFVl+8m14kVG93i5xvu/kvXkQtnKv95phaY1YHRxuY4UwAQKwfdVG/KKl3f4CS72fzd56luF6x8YXW1ud84zzJU+LvR9KPjkkAXhthtbF0654FxYk+ztmj5mXuStqhFIfNKoGa1J5K17pPQKJ4W3cBTnR1Dc2C7YNvNQ9Cs=',
    'wp_ak_bt': '1|20200518',
    'wp_ak_bfd': '1|20201222',
    'wp_ak_tos': '1|20211110',
    'wp_ak_sff': '1|20220425',
    'wp_ak_lr': '0|20221020',
    'wp_ak_co': '2|20220505',
    'wp_ak_btap': '1|20211118',
    'wp_ak_pp': '1|20210310',
    'wp_usp': '1---',
    'wp_ttrid': '"417b0a08-4616-4614-9ce1-5c9a9475f63d"',
    'wp_pwapi_ar': '"H4sIAAAAAAAA/6uuBQBDv6ajAgAAAA=="',
    '_gid': 'GA1.2.585883373.1705745399',
    'akaas_wp_ak_v_nav': '1713522911~rv=60~id=5de61f9c6a3131bcadc754fc81a910a5~rn=1-variant',
    'wp_ld_assembler': 'enableArticleDescriptionsForYouCard.0|enableFullWidthForYouCard.0',
    'wp_s': 'T.1.1705745397.1705746912.1.1.0.1',
    'cto_bundle': 'mFHs619aUGtwbkpTendpUWVuUkVCbU9SbyUyRm01TnQwWVJ1TG5HQVc0dDN5azIzQ0d0T2FKNFhDTnlkblpaRHZEd3NudThOeSUyQlJmYzZ0dW8za2NoaXVYRU9WM0hWRnVGdm9NcjhMQ00xZ2IxWXlFTjdjQkR5RFF4ZE5QSTFsaHU2RWdCcDZFJTJCMUhFOUNYeXdnbVQlMkZqdDBmOUJrYU8lMkZWY0N1U1p0U0d0bW1ZRFl5a3VZJTNE',
    '_cb': 'D23HDtBQdSIKDzXNTC',
    '_chartbeat2': '.1705745398879.1705746912553.1.CRcBP6BqqLOtb0XeEBh5yUsBUx1-9.4',
    '_cb_svref': 'https%3A%2F%2Fwww.washingtonpost.com%2F',
    '_ga_WRCN68Y2LD': 'GS1.1.1705746912.1.0.1705746912.0.0.0',
    '_ga': 'GA1.1.1233712934.1705745399',
    '_t_tests': 'eyJDVEdaZWlKUDFtMkxMIjp7ImNob3NlblZhcmlhbnQiOiJDIiwic3BlY2lmaWNMb2NhdGlvbiI6WyJuVU53cCJdfSwibGlmdF9leHAiOiJtIn0=',
    'permutive-id': '829b6366-5021-4d8c-9612-fdd32160cd7d',
    'jctr_sid': '9781517057469138278350',
    '_fbp': 'fb.1.1705746913829.9076664878',
    '__gads': 'ID=5af9a184b2cf1a1b:T=1705745406:RT=1705746914:S=ALNI_MY_6tnS3D2jgRtciJ1lWH0-7nmzag',
    '__gpi': 'UID=00000cebc5863588:T=1705746914:RT=1705746914:S=ALNI_MbP2VGj-OK80cVcS6QYqslfQCaxYg',
    'jts-rw': '{"u":"58676170574540047070582"}',
    'jts-fbp': 'fb.1.1705746913829.9076664878',
    'wp_ak_pct': '0|20230131',
    'bm_sv': '67131FD38CF3F58F08A1CA2E36BD3F28~YAAQDpZUaDDiEfWMAQAAE9CHJhZ3YhL862uBpSTG2x7daOAYlbG0AJSX+LTC4if9A76LUO+fh0fJjW5iFuSrIfSvy+f0kBZK3oLVWf2QbJC2dQDn0abkKqTnqBuiZRWS9l5oj+MQuwf+vYx9YFoQRhq95MHl+wNd32mH9S3WGevCx0PPzPl1g8Z9XuviAKZaVXB/7FPoCcskkraBuwLTOm3I0cr+v1geF17y/GVPT9dHsG0cMZs3A0MXw6x/WrEabPQVBThBOTND~1',
    'RT': '"z=1&dm=www.washingtonpost.com&si=59776052-6824-4b3c-80af-30ebe3468561&ss=lrlwruvu&sl=3&tt=fjq&obo=1&rl=1&nu=3tjflmxg&cl=wdcg&ld=1n54w&r=2xpaxrjb&ul=1n559"',
}
washington_post_homepage_headers = {
    'authority': 'www.washingtonpost.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'wp_devicetype=0; wp_ak_signinv2=1|20230125; wp_ak_om=1|20230731; wp_ak_wab=0|1|1|1|0|1|1|1|0|20230418; wp_ak_v_mab=0|0|0|1|20231130; wp_geo=HK||||INTL; ak_bmsc=3DF42D0A5CE61C9374C942E9EF911FB4~000000000000000000000000000000~YAAQDpZUaLGPEfWMAQAAMzZZJhaYG9rG2dc9rDg3hlwFLli4JRO9NJIQs8rywcp/ks14revjlqF7gaEgLAdDxXwQtoW0YCMxIohF6VWptZrgpSGoXrBlXqc2yCUjcinJedQjWduYdAFbJ+sDRYEVNirF69A/zd/VIbyYZg+/Nc7C8PMqrAe4c1NuxO1wLB8+ZwXtFCT5bpGPkZj3dFc32kqCmaG0lBElV0LuJm+xIC6rf69YrFVl+8m14kVG93i5xvu/kvXkQtnKv95phaY1YHRxuY4UwAQKwfdVG/KKl3f4CS72fzd56luF6x8YXW1ud84zzJU+LvR9KPjkkAXhthtbF0654FxYk+ztmj5mXuStqhFIfNKoGa1J5K17pPQKJ4W3cBTnR1Dc2C7YNvNQ9Cs=; wp_ak_bt=1|20200518; wp_ak_bfd=1|20201222; wp_ak_tos=1|20211110; wp_ak_sff=1|20220425; wp_ak_lr=0|20221020; wp_ak_co=2|20220505; wp_ak_btap=1|20211118; wp_ak_pp=1|20210310; wp_usp=1---; wp_ttrid="417b0a08-4616-4614-9ce1-5c9a9475f63d"; wp_pwapi_ar="H4sIAAAAAAAA/6uuBQBDv6ajAgAAAA=="; _gid=GA1.2.585883373.1705745399; akaas_wp_ak_v_nav=1713522911~rv=60~id=5de61f9c6a3131bcadc754fc81a910a5~rn=1-variant; wp_ld_assembler=enableArticleDescriptionsForYouCard.0|enableFullWidthForYouCard.0; wp_s=T.1.1705745397.1705746912.1.1.0.1; cto_bundle=mFHs619aUGtwbkpTendpUWVuUkVCbU9SbyUyRm01TnQwWVJ1TG5HQVc0dDN5azIzQ0d0T2FKNFhDTnlkblpaRHZEd3NudThOeSUyQlJmYzZ0dW8za2NoaXVYRU9WM0hWRnVGdm9NcjhMQ00xZ2IxWXlFTjdjQkR5RFF4ZE5QSTFsaHU2RWdCcDZFJTJCMUhFOUNYeXdnbVQlMkZqdDBmOUJrYU8lMkZWY0N1U1p0U0d0bW1ZRFl5a3VZJTNE; _cb=D23HDtBQdSIKDzXNTC; _chartbeat2=.1705745398879.1705746912553.1.CRcBP6BqqLOtb0XeEBh5yUsBUx1-9.4; _cb_svref=https%3A%2F%2Fwww.washingtonpost.com%2F; _ga_WRCN68Y2LD=GS1.1.1705746912.1.0.1705746912.0.0.0; _ga=GA1.1.1233712934.1705745399; _t_tests=eyJDVEdaZWlKUDFtMkxMIjp7ImNob3NlblZhcmlhbnQiOiJDIiwic3BlY2lmaWNMb2NhdGlvbiI6WyJuVU53cCJdfSwibGlmdF9leHAiOiJtIn0=; permutive-id=829b6366-5021-4d8c-9612-fdd32160cd7d; jctr_sid=9781517057469138278350; _fbp=fb.1.1705746913829.9076664878; __gads=ID=5af9a184b2cf1a1b:T=1705745406:RT=1705746914:S=ALNI_MY_6tnS3D2jgRtciJ1lWH0-7nmzag; __gpi=UID=00000cebc5863588:T=1705746914:RT=1705746914:S=ALNI_MbP2VGj-OK80cVcS6QYqslfQCaxYg; jts-rw={"u":"58676170574540047070582"}; jts-fbp=fb.1.1705746913829.9076664878; wp_ak_pct=0|20230131; bm_sv=67131FD38CF3F58F08A1CA2E36BD3F28~YAAQDpZUaDDiEfWMAQAAE9CHJhZ3YhL862uBpSTG2x7daOAYlbG0AJSX+LTC4if9A76LUO+fh0fJjW5iFuSrIfSvy+f0kBZK3oLVWf2QbJC2dQDn0abkKqTnqBuiZRWS9l5oj+MQuwf+vYx9YFoQRhq95MHl+wNd32mH9S3WGevCx0PPzPl1g8Z9XuviAKZaVXB/7FPoCcskkraBuwLTOm3I0cr+v1geF17y/GVPT9dHsG0cMZs3A0MXw6x/WrEabPQVBThBOTND~1; RT="z=1&dm=www.washingtonpost.com&si=59776052-6824-4b3c-80af-30ebe3468561&ss=lrlwruvu&sl=3&tt=fjq&obo=1&rl=1&nu=3tjflmxg&cl=wdcg&ld=1n54w&r=2xpaxrjb&ul=1n559"',
    'referer': 'https://www.washingtonpost.com/?reload=true&_=1705746910714',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
washington_post_homepage_params = {
    'reload': 'true',
    'itid': 'force_refresh',
    '_': '1705748470058',
}


def scrap_url(url, header, cookie, param):
    return requests.get(url, params=param, cookies=cookie, headers=header)


def scrap_washington_homepage_headline():
    try:
        response = scrap_url(washington_post_homepage_url, washington_post_homepage_params,
                             washington_post_homepage_cookie, washington_post_homepage_headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = soup.find_all('a', {'data-pb-local-content-field': 'web_headline'})
        for i, ele in enumerate(tags):
            href = ele.get('href')
            text = ele.text.strip()
            print("URL:", href)
            print("Text:", text)
            if i == 2:
                get_single_news(href, text)
                break
            print("---")
    except Exception as e:
        print("Get washington homepage url failed:", str(e))


def get_single_news(url, headline):
    try:
        content = []
        response = scrap_url(url, washington_post_homepage_params,
                             washington_post_homepage_cookie, washington_post_homepage_headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        potential = soup.findAll('div', {'class': 'wpds-c-PJLV article-body', 'data-qa': 'article-body'})
        for ele in potential:
            p_tag = ele.find('p', {'data-testid': 'drop-cap-letter'})
            if p_tag is not None:
                # p.text()将返回文章中的纯文本内容，不会包含URL。要获取链接的文本，请使用p.find('a').text或p.find('a')['href']
                content.append(p_tag.text.strip())
        print("Get washington news success, url:", url, "headline:", headline, "detail:", " ".join(content))
    except Exception as e:
        print("Get washington news failed, url:", url, "headline:", headline, str(e))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('program start...', end="\n")
    scrap_washington_homepage_headline()
