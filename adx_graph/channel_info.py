
from telethon.tl.functions.channels import GetFullChannelRequest
import datetime
from adx_graph.func import tg_conn
from adx_graph.func import get_phones

accounts = open("./adx_graph/accounts.txt", 'r', encoding='utf-8').readlines()
accounts = get_phones(accounts=accounts)
phone = accounts[0]

class CHANNEL_INFO():
    async def post_statistics(self, tg_channel, msg_id, phone):
        """Возвращает статистику поста"""
        print(phone)
        client = await tg_conn.client_up(phone)
        count = 0
        views = []
        forwards = []
        async for message in client.iter_messages(tg_channel):
            count += 1
            if count >=200:
                await client.disconnect()
                return 0,0
            if message.id==msg_id:
                await client.disconnect()
                return message.views, message.forwards
            else: continue
            


        return views, forwards


channel_info = CHANNEL_INFO()




def format_number_to_k(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])




