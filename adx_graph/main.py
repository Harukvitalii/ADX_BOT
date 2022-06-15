

from adx_graph.channel_info import channel_info
from adx_graph.func import get_phones


async def make_post_stat(tg_channel, msg_id):
    accounts = open("./adx_graph/accounts.txt", 'r', encoding='utf-8').readlines()
    accounts = get_phones(accounts=accounts)
    phonetg = accounts[0]
    view,forward = await channel_info.post_statistics(tg_channel=tg_channel, msg_id=msg_id, phone=phonetg)

    return view,forward

