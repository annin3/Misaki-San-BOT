import discord
import requests
import imasparql
import env.token


async def search_asmr(name):
    response = requests.get("https://www.dlsite.com/maniax/sapi/=/keyword/%s/work_type_category/audio/ana_flg/off/format/json" %name)
    if response.status_code == 200:
        list = response.json()
        if len(list) == 0:
           
            return "%sさんに関する発売中の音声作品は見つかりませんでした・・・" %name
        else :
            ans = "なんとっ！%sさんに関する発売中の音声作品が%d件見つかりました！\n" %(name,len(list))
            if len(list) > 3:
                ans += "上位3件を表示します\n"
            print(list)
            for l in list[0:3]:
                ans += "https://www.dlsite.com/home-touch/work/=/product_id/%s.html\n" %l["product_id"]

            return ans
                
    else:
        print("通信に失敗しちゃいました・・・")

async def search_asmr_will(name):
    response = requests.get("https://www.dlsite.com/maniax/sapi/=/keyword/%s/work_type_category/audio/ana_flg/on/format/json" %name)
    if response.status_code == 200:
        list = response.json()
        if len(list) == 0:
           
            return "%sさんに関する発売予定の音声作品は見つかりませんでした・・・" %name
        else :
            ans = "なんとっ！%sさんに関する発売予定の音声作品が%d件見つかりました！\n" %(name,len(list))
            if len(list) > 3:
                ans += "上位3件を表示します\n"
            print(list)
            for l in list[0:3]:
                ans += "https://www.dlsite.com/home-touch/announce/=/product_id/%s.html\n" %l["product_id"]

            return ans
                
    else:
        print("通信に失敗しちゃいました・・・")


client = discord.Client()

@client.event
async def on_message(message):
    message_l = message.content.split()
    if message_l[0] == '/asmr':
        ans = await search_asmr(message_l[1])
        await message.channel.send(ans)
        ans = await search_asmr_will(message_l[1])
        await message.channel.send(ans)

    if message_l[0] == '/idol_asmr':
        cv_name = imasparql.get_idol_cv(message_l[1])
        if cv_name != None:
            print(cv_name)
            await message.channel.send("%sさんのCVは%sさんです。%sさんの音声作品を検索します。" %(message_l[1],cv_name,cv_name))
            ans = await search_asmr(cv_name)
            await message.channel.send(ans)
            ans = await search_asmr_will(cv_name)
            await message.channel.send(ans)
        else:
            await message.channel.send("声優さんの検索に失敗しちゃいました・・・")


client.run(env.token.TOKEN)