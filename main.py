import discord
import requests
import imasparql
import env.token

async def embed(id):
    response = requests.get("https://www.dlsite.com/home/product/info/ajax?product_id=%s" %id).json()
    img = response[id]["work_image"]
    dl_count = response[id]["dl_count"]
    wishlist_count = response[id]["wishlist_count"]
    title_name = response[id]["work_name"]
    is_sale = response[id]["is_sale"]
    on_sale = response[id]["on_sale"]
    price = response[id]["price"]
    print(is_sale)
    if not is_sale or on_sale == 0:
        url = "https://www.dlsite.com/home-touch/announce/=/product_id/%s.html" %id
    else:
        url = "https://www.dlsite.com/maniax/dlaf/=/link/work/aid/annin3/id/%s.html" %id
    print(url)
    print(title_name)
    embed=discord.Embed(title=title_name, url=url)
    embed.add_field(name="販売数", value=dl_count, inline=True)
    embed.add_field(name="お気に入り数", value=wishlist_count, inline=True)
    embed.add_field(name="価格", value="%s円" %price, inline=True)
    embed.set_thumbnail(url="https:%s" %img)
    return embed


async def search_asmr(name, message):
    response = requests.get("https://www.dlsite.com/maniax/sapi/=/keyword/%s/work_type_category/audio/ana_flg/off/format/json" %name)
    if response.status_code == 200:
        list = response.json()
        if len(list) == 0:
            await message.channel.send("%sさんに関する発売中の音声作品は見つかりませんでした・・・" %name)
        else :
            ans = "なんとっ！%sさんに関する発売中の音声作品が%d件見つかりました！\n" %(name,len(list))
            if len(list) > 3:
                ans += "上位3件を表示します"
            await message.channel.send(ans)
            for l in list[0:3]:
                id = l["product_id"]
                await message.channel.send(embed = await embed(id))       
    else:
        print("通信に失敗しちゃいました・・・")

async def search_asmr_will(name, message):
    response = requests.get("https://www.dlsite.com/maniax/sapi/=/keyword/%s/work_type_category/audio/ana_flg/on/format/json" %name)
    if response.status_code == 200:
        list = response.json()
        if len(list) == 0:
           
            await message.channel.send("%sさんに関する発売予定の音声作品は見つかりませんでした・・・" %name)
        else :
            ans = "なんとっ！%sさんに関する発売予定の音声作品が%d件見つかりました！\n" %(name,len(list))
            if len(list) > 3:
                ans += "上位3件を表示します"
            await message.channel.send(ans)
            for l in list[0:3]:
                id = l["product_id"]
                await message.channel.send(embed = await embed(id))          
    else:
        print("通信に失敗しちゃいました・・・")


client = discord.Client()

@client.event
async def on_message(message):
    message_l = message.content.split()
    if message_l[0] == '/asmr':
        await search_asmr(message_l[1], message)
        await search_asmr_will(message_l[1], message)

    if message_l[0] == '/idol_asmr':
        cv_name = imasparql.get_idol_cv(message_l[1])
        if cv_name != None:
            print(cv_name)
            await message.channel.send("%sさんのCVは%sさんです。%sさんの音声作品を検索します。" %(message_l[1],cv_name,cv_name))
            await search_asmr(cv_name, message)
            await search_asmr_will(cv_name, message)
        else:
            await message.channel.send("声優さんの検索に失敗しちゃいました・・・")


client.run(env.token.TOKEN)