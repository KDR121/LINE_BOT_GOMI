import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
import datetime

file = open("info.json","r")
info = json.load(file)

CHANNEL_ACCESS_TOKEN = info["CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def main():
    USER_ID = info["USER_ID"]
    today = datetime.datetime.today() + datetime.timedelta(hours = 9)
    tomorrow = datetime.datetime.today() + datetime.timedelta(days = 1) + datetime.timedelta(hours = 9)
    #-------------------------------
    #月曜日、木曜日は燃えるゴミの日
    #火曜日はプラスティックの日
    #毎月第一・三水曜日はビン・缶の日
    #-------------------------------
    #通常の日の処理
    if today.strftime("%A") == "Monday":
        gomi_info = "燃えるゴミの日"
        gomi_tomorrow_info = "プラスチックの日"
    elif today.strftime("%A") == "Tuesday":
        gomi_info = "プラスチックの日"
        if (tomorrow.day - 1) // 7 != (0 or 2):#第一と第三週
            gomi_tomorrow_info = "ビン・缶等出せる日"
        else:
            gomi_tomorrow_info = "何もない日"
    elif today.strftime("%A") == "Wednesday":
        if (today.day - 1) // 7 != (0 or 2):#第一と第三週
            gomi_info = "ビン・缶等出せる日"
        else:
            gomi_info = "何もない日"
        gomi_tomorrow_info = "燃えるゴミの日"
    elif today.strftime("%A") == "Thursday":
        gomi_info = "燃えるゴミの日"
        gomi_tomorrow_info = "何もない日"
    elif today.strftime("%A") == "Friday":
        gomi_info = "何もない日"
        gomi_tomorrow_info = "何もない日"
    elif today.strftime("%A") == "Saturday":
        gomi_info = "何もない日"
        gomi_tomorrow_info = "何もない日"
    elif today.strftime("%A") == "Sunday":
        gomi_info = "何もない日"
        gomi_tomorrow_info = "燃えるゴミの日"
    else:
        gomi_info = "error"
        gomi_tomorrow_info = "error"
    #------------------------------
    #特別な日を除く
    #月曜なのに燃えるゴミの日じゃない時
    #not_moeru_day = [0923,0103,0321]
    #for t in not_moeru_day:
    #-----------------------------
    today_youbi = "error"
    youbi ={"Monday":"月", "Tuesday":"火","Wednesday":"水","Thursday":"木","Friday":"金","Saturday":"土","Sunday":"日"}
    for k, v in youbi.items():
        if k == today.strftime("%A"):
            today_youbi = v
        if k == tomorrow.strftime("%A"):
            tomorrow_youbi = v

    str_message = str("今日({}月{}日({}))は{}です。\n明日({}月{}日({}))は{}です。".format(today.month, today.day, today_youbi, gomi_info, tomorrow.month, tomorrow.day, tomorrow_youbi, gomi_tomorrow_info))
    messages = TextSendMessage(text = str_message)
    #line_bot_api.push_message(USER_ID, messages = messages)
    line_bot_api.broadcast(messages = messages)

if __name__ == "__main__":
    main()

