import requests
import env.token

def dmm_affiliate(keyword):
    response = requests.get(env.token.DMM_URL %keyword).json()
    items = response["result"]["items"]
    print(len(items))


    ans = "dmmにて「%s」で検索します \n" %keyword
    if len(items) > 3:
        ans += "上位3件を表示します \n"
        for item in items[0:3]:
           ans = ans + item["title"]  + "\n" + item["affiliateURL"] + "\n"
    elif len(items) == 0:
        ans += "該当する商品はありませんでした。検索ワードを変更してください。"
    else:
        for item in items[0:3]:
           ans = ans + item["title"]  + "\n" + item["affiliateURL"] + "\n"
             
    return ans
        # embed=discord.Embed(title=title_name, url=url)
        # embed.add_field(name="販売数", value=dl_count, inline=True)
        # embed.add_field(name="お気に入り数", value=wishlist_count, inline=True)
        # embed.add_field(name="価格", value="%s円" %price, inline=True)
        # embed.set_thumbnail(url="https:%s" %img)

