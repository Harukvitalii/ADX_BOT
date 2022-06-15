from loader import pgbotdb


def check_if_not_adx_pay(channel_id, admin_id):
    posts = pgbotdb.get_all_posts_by_channel_id(channel_id, admin_id)
    print(posts)
    if len(posts)//9:
        return True 
    else: return False