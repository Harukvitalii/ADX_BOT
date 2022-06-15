
import psycopg2
from data.config import HOST, db_name, password, user,port
import json
from psycopg2.errors import UniqueViolation
        
class PGBOTDB:
    def __init__(self):
        self.conn = psycopg2.connect(
        host=HOST,
        user = user,
        password = password,
        database=db_name,
        port = port,
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    """USERS TABLE"""
    def create_tables(self):
        """SET TIME ZONE"""
        self.cursor.execute("""SET TIME ZONE 'Europe/Moscow';""")
        
        """users"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial NOT NULL PRIMARY KEY,
                first_name varchar(50),
                nick_name varchar(50),
                user_id bigint UNIQUE NOT NULL,
                is_admin boolean,
                date_enter DATE,
                balance integer NULL,
                spent_on_ad integer NOT NULL,
                earned integer NOT NULL,
                referral_balance integer NOT NULL
                );""")
        self.conn.commit()

        """channels"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS channels(
                id serial NOT NULL PRIMARY KEY,
                channel_id bigint unique not null,
                admin_id bigint not null,
                name varchar(100),
                link varchar(75),      
                description varchar(1000),
                comment varchar(1000),
                channels_theme varchar(50),
                banned_themes varchar(500),
                times_for_posts varchar(255));""")
        self.conn.commit()

        """channel_conditions"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS channel_conditions(
                id serial NOT NULL PRIMARY KEY,
                channel_id bigint unique not null,
                conditions varchar(200) not null);""")

        """posts"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS posts (
            id bigserial NOT NULL PRIMARY KEY,
            channel_id bigint not null,
            ordered_by_id bigint not null,
            text varchar(1400),
            parse_mode varchar(10),
            pictue_id varchar(150),
            post_price integer not null,
            time_in_channel timestamp without time zone not null,
            end_of_post timestamp without time zone not null,
            bill_id varchar(50) unique not null,
            confirmed varchar(15),
            message_id bigint,
            kb varchar(400));""")

        """post_statistics"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS post_statistics (
            id bigserial NOT NULL PRIMARY KEY,
            channel_id bigint,
            advertiser_id bigint,
            name varchar(75),
            text varchar(2500),
            image varchar(300),
            date_of_post timestamp without time zone not null,
            end_of_post timestamp without time zone not null,
            views_count integer,
            forwards_count integer,
            message_id integer);""")

        """channel_statistics"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS channel_statistics (
            id bigserial NOT NULL PRIMARY KEY,
            channel_id bigint unique not null,
            date date not null,
            subscribers integer,
            average_views integer,
            average_forwards integer,
            views_yesterday integer,
            views_2days integer,
            views_3days integer,
            views_4days integer,
            ERR float(4),
            CPV float(3));""")
        
        """user_basket"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS user_basket (
            id bigserial NOT NULL PRIMARY KEY,
            admin_id bigint not null,
            channel_id bigint not null,
            time_for_post timestamp without time zone,
            conditions varchar(15),
            price integer,
            paid boolean);""")

        """user_back_from_times"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS user_back_from_times (
            id bigserial NOT NULL PRIMARY KEY,
            user_id bigint unique not null,
            channel_id bigint,
            page integer,
            sort_by varchar(5),
            reverse varchar(6),
            theme varchar(50));""")

        """qiwi_bills"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS qiwi_bills (
            id bigserial NOT NULL PRIMARY KEY,
            qiwi_p2p_key varchar(300) not null,
            user_id bigint not null,
            deposit integer not null,
            bill_id varchar(50) unique not null,
            created_date timestamp without time zone);""")
        
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS channel_participants (
            id bigserial NOT NULL PRIMARY KEY,
            channel_id bigint not null,
            date_scrap date not null,
            participants integer not null);""")


        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS user_requisites (
            id serial NOT NULL PRIMARY KEY,
            user_id bigint unique not null,
            p2p_qiwi_token varchar(300),
            wm_token varchar(300),
            yoomoney_token varchar(300),
            btc_banker_token varchar(300));""")
        
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS user_referral (
            id serial NOT NULL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            referral BIGINT unique NOT NULL,
            paid boolean NOT NULL,
            free_slot varchar(100));""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS channel_stat_imgs (
            id serial NOT NULL PRIMARY KEY,
            channel_id bigint unique,
            img_link varchar(50),
            logo_img_link varchar(50));""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin_ad_posts (
            id serial NOT NULL PRIMARY KEY,
            admin_id bigint,
            text varchar(1500),
            picture_id varchar(150),
            parse_mode varchar(10),
            kb varchar(500),
            name varchar(50));""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS inline_links (
            id serial NOT NULL PRIMARY KEY,
            identifier varchar(12) unique,
            channel_id bigint,
            channel_link varchar(75),
            condition varchar(25), 
            post_price integer,
            time timestamp without time zone);""")


        self.cursor.execute('''SHOW timezone;''')
        res = self.cursor.fetchone()
        print(res)



    def register_user(self,first_name, nick_name, user_id, date_enter, balance, spent_on_ad, earned, referral_balance):
        self.cursor.execute("""INSERT INTO users(first_name,nick_name, user_id, date_enter, balance, spent_on_ad, earned, referral_balance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",
        (first_name, nick_name, user_id, date_enter, balance, spent_on_ad, earned, referral_balance))
        
        self.cursor.execute("""INSERT INTO user_back_from_times (user_id) VALUES (%s)""",(user_id,))
        self.cursor.execute("""INSERT INTO user_requisites (user_id) VALUES (%s)""",(user_id,))

    def register_referral(self,inviter,invitee):
        paid = 'no'
        try: 
            int(inviter)
            int(invitee)
            self.cursor.execute("""INSERT INTO user_referral (user_id,referral,paid) VALUES (%s,%s,%s)""",(inviter,invitee,paid))
        except ValueError:
            print("not an integers", inviter,invitee)
        except UniqueViolation:
            return "UniqueViolation"
        return True

    def is_exists_user(self, user_id):
        self.cursor.execute("""SELECT * FROM users WHERE user_id = (%s);""",(user_id,))
        res = self.cursor.fetchone()
        if res == None:
            return False
        else: return True
    
    def user_is_admin(self,user_id):
        self.cursor.execute("""SELECT is_admin from users WHERE user_id = (%s);""", (user_id,))
        res = self.cursor.fetchone()
        print('is admin',res)
        return res[0]


    def set_user_admin(self,user_id):
        self.cursor.execute("""UPDATE users SET is_admin = 'yes' WHERE user_id = (%s);""", (user_id,))

    def user_is_adveriser(self,user_id):
        self.cursor.execute("""UPDATE users SET is_admin = 'no' WHERE user_id = (%s);""", (user_id,))


    def upadte_user_role(self,user_id,role):
        if role == 'admin': self.cursor.execute("""UPDATE users SET is_admin = 'yes' WHERE user_id = (%s);""", (user_id,))
        elif role == 'advertiser': self.cursor.execute("""UPDATE users SET is_admin = 'no' WHERE user_id = (%s);""", (user_id,))


    def is_exists_admin(self, user_id):
        self.cursor.execute("""SELECT is_admin FROM users WHERE user_id = (%s);""",(user_id,))
        res = self.cursor.fetchone()
        return res[0]

    def user_info(self, user_id):
        self.cursor.execute("""SELECT * FROM users WHERE user_id = (%s);""",(user_id,))
        res = self.cursor.fetchone()
        return res


    """CHANNELS"""
    def save_channel_info(self, channel_id, admin_id, name, link, description, comment, channels_theme, banned_themes,times_for_posts):
        self.cursor.execute("""INSERT INTO channels 
        (channel_id, admin_id, name, link, description, comment, channels_theme, banned_themes,times_for_posts) VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
        (channel_id, admin_id, name, link, description, comment, channels_theme, banned_themes,times_for_posts))

    def select_channels(self, admin_id):
        self.cursor.execute("""
        SELECT * FROM channels WHERE admin_id = %s;
        """,(admin_id,))
        res = self.cursor.fetchall()
        return res

    def select_channels_for_del(self, admin_id):
        self.cursor.execute("""
        SELECT name, channel_id FROM channels WHERE admin_id = %s;
        """,(admin_id,))
        res = self.cursor.fetchall()
        return res

    def select_all_channels_for_del(self):
        self.cursor.execute("""
        SELECT name, channel_id FROM channels;
        """)
        res = self.cursor.fetchall()
        return res

    def select_channel_by_link(self, link):
        self.cursor.execute("""
        SELECT channel_id FROM channels WHERE link = %s;
        """,(link,))
        res = self.cursor.fetchone()
        return res[0]

    def select_channel(self, channel_id: int):
        """id,channel_id, admin_id, name, link, description, comment, channels_theme, banned_themes,times_for_posts"""
        self.cursor.execute("""
        SELECT * FROM channels WHERE channel_id = %s;
        """,(channel_id,))
        res = self.cursor.fetchone()
        return res
    
    def select_channels_by_theme(self,theme):
        self.cursor.execute("SELECT * FROM channels WHERE channels_theme LIKE %s",(theme+'%',))
        return self.cursor.fetchall()


    def get_all_channels(self):
        """id, channel_id, admin_id, name, link, description, comment, channels_theme, banned_themes,times_for_posts"""
        self.cursor.execute("""SELECT * FROM channels""")
        res = self.cursor.fetchall()
        return res
    
    def select_all_channels_buy_theme(self, theme_name):
        self.cursor.execute("""SELECT * FROM channels WHERE channels_theme = %s""", (theme_name,))
        res = self.cursor.fetchall()
        return res

    def channel_change_name(self, channel_id, new_name):
        self.cursor.execute("""UPDATE channels SET name = %s WHERE channel_id = %s""", (new_name, channel_id))

    def channel_change_link(self, channel_id, new_link):
        self.cursor.execute("""UPDATE channels SET link = %s WHERE channel_id = %s""", (new_link, channel_id))

    def channel_change_comment(self, channel_id, comment):
        self.cursor.execute("""UPDATE channels SET comment = %s WHERE channel_id = %s""", (comment, channel_id))

    def channel_change_description(self, channel_id, new_description):
        self.cursor.execute("""UPDATE channels SET description = %s WHERE channel_id = %s""", (new_description, channel_id))

    def channel_change_channels_theme(self, channel_id, new_channels_theme):
        self.cursor.execute("""UPDATE channels SET channels_theme = %s WHERE channel_id = %s""", (new_channels_theme, channel_id))
  
    def channel_change_banned_themes(self, channel_id, new_banned_themes):
        self.cursor.execute("""UPDATE channels SET banned_themes = %s WHERE channel_id = %s""", (new_banned_themes, channel_id))

    def channel_change_times_for_posts(self, channel_id, new_times_for_posts):
        self.cursor.execute("""UPDATE channels SET times_for_posts = %s WHERE channel_id = %s""", (new_times_for_posts, channel_id))

    def delete_channel(self, channel_id):
        self.cursor.execute("""DELETE FROM channels WHERE channel_id = %s""", (channel_id,))
        self.cursor.execute("""DELETE FROM channel_conditions WHERE channel_id = %s""", (channel_id,))
        self.cursor.execute("""DELETE FROM channel_participants WHERE channel_id = %s""", (channel_id,))
        self.cursor.execute("""DELETE FROM post_statistics WHERE channel_id = %s""", (channel_id,))
        self.cursor.execute("""DELETE FROM channel_statistics WHERE channel_id = %s""", (channel_id,))
        
    
    """CHANNELS CONDITIONS"""


    def save_conditions(self,channel_id, conditions):
        self.cursor.execute("""INSERT INTO channel_conditions
        (channel_id, conditions) VALUES
        (%s,%s);""",(channel_id,conditions))

    def conditions_change_condition(self, channel_id, conditions):
        self.cursor.execute("""UPDATE channel_conditions SET conditions = %s WHERE channel_id = %s""", (conditions, channel_id))
    
    def get_conditions(self, channel_id):
        """Возвращает условия при суплае айди канала одно"""
        self.cursor.execute("""SELECT conditions FROM channel_conditions WHERE channel_id = %s""",(channel_id,))
        res = self.cursor.fetchone()
        return json.loads(res[0])

    def select_conditions(self,channel_id):
        self.cursor.execute("""SELECT conditions FROM channel_conditions
        WHERE channel_id=%s;""",(channel_id,))
        res = self.cursor.fetchone()
        return res[0]



    """POST STATISTICS"""


    def deploy_post(self,channel_id,advertiser_id,date_of_post,end_of_post,text,image):
        name = self.select_channel(channel_id=channel_id)[3]
        self.cursor.execute("""INSERT INTO post_statistics (channel_id,advertiser_id,name,date_of_post,end_of_post,text,image) VALUES
        (%s,%s,%s,%s,%s,%s)""",(channel_id,advertiser_id,name,date_of_post,end_of_post,text,image))


    def update_post_views_forwards(self,chan_id,v,f):
        
        self.cursor.execute("""UPDATE post_statistics SET views_count = %s, forwards_count = %s WHERE channel_id = %s""",(v,f,chan_id))
    
    
    
    """CHANNEL_STATISTICS"""


    def save_day_channel_statistics(self,subscribers, average_views, views_yesterday, average_forwards, ERR, CPV_1000, channel_id,date,views_2days,views_3days,views_4days):
        self.cursor.execute("""INSERT INTO channel_statistics (subscribers, average_views, views_yesterday, average_forwards, err, cpv, channel_id,date,views_2days,views_3days,views_4days)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (channel_id)
        DO UPDATE SET 
        subscribers = %s, 
        average_views = %s, 
        views_yesterday = %s, 
        average_forwards = %s, 
        err = %s, 
        cpv = %s, 
        date = %s,
        views_2days = %s,
        views_3days = %s,
        views_4days = %s""",
        (subscribers, average_views, views_yesterday, average_forwards, ERR, CPV_1000, channel_id,date,views_2days,views_3days,views_4days,
        subscribers, average_views, views_yesterday, average_forwards, ERR, CPV_1000,date,views_2days,views_3days,views_4days))
        
    def select_all_channel_statistics_today(self):
        self.cursor.execute("""SELECT * FROM channel_statistics""")
        res = self.cursor.fetchall()
        return res

    def select_channel_statistic_today(self, channel_id):
        self.cursor.execute("""SELECT * FROM channel_statistics WHERE channel_id = %s""",(channel_id,))
        res = self.cursor.fetchall()
        return res[-1]
    
    
    
    """user_back_from_times"""


    def insert_user_back_from_times(self,user_id,channel_id, page, sort_by, reverse, theme = "-"):
        self.cursor.execute("""UPDATE user_back_from_times SET channel_id=%s, page=%s, sort_by=%s, reverse=%s, theme=%s
                                WHERE user_id = %s;""",
                               (channel_id, page, sort_by, reverse, theme,user_id))


    def update_user_back_from_times(self,user_id,channel_id, page, sort_by, reverse, theme = "-"):
        if "$nt" in channel_id: channel_id = channel_id.replace("$nt", '')
        print(user_id,channel_id, page, sort_by, reverse, theme)
        reverse = 'True' if reverse=='T' else True
        self.cursor.execute("""UPDATE user_back_from_times 
                               SET channel_id=%s, page=%s, sort_by=%s, reverse=%s, theme=%s
                               WHERE user_id = %s;""",
                               (channel_id, page, sort_by, reverse, theme,user_id))

    def select_user_back_from_times(self,user_id):
        self.cursor.execute("""SELECT * FROM user_back_from_times
                               WHERE user_id = %s;""",(user_id,))
        res = self.cursor.fetchone()
        return res


    """POSTS"""

    def save_post_from_user(self,channel_id, ordered_by_id, text, pictue_id, parse_mode, time_in_channel, end_of_post, confirmed,bill_id,post_price,kb):
        self.cursor.execute("""INSERT INTO posts 
        (channel_id, ordered_by_id, text, pictue_id, parse_mode, time_in_channel, end_of_post,bill_id, confirmed,post_price,kb)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s);""",
        (channel_id, ordered_by_id, text, pictue_id, parse_mode, time_in_channel, end_of_post,bill_id, confirmed,post_price,kb))
        
    def confirm_post_payment(self, bill_id):
        self.cursor.execute("""UPDATE posts SET confirmed = 'PAID' WHERE bill_id =%s""",(bill_id,))


    def get_posts(self):
        self.cursor.execute("SELECT * FROM posts WHERE confirmed != 'DONE'")
        res = self.cursor.fetchall()
        return res

    def get_all_posts_by_channel_id(self,channel_id, ADMIN):
        self.cursor.execute("SELECT * FROM posts WHERE channel_id=%s AND ordered_by_id != %s AND confirmed != 'False'",(channel_id,ADMIN))
        res = self.cursor.fetchall()
        return res


    def posts_ads_statistics(self,user_id,page:int):
        print("page ", page)
        self.cursor.execute("SELECT * FROM posts WHERE ordered_by_id = %s",(user_id,))
        posts = self.cursor.fetchall()
        print(posts)
        if page>=len(posts):
            page = 0
        try:
            return page, posts[int(page)]
        except IndexError:
            print("indexerrorrrororor")
            return 'no data', ''

    def posts_admin_ads_statistics(self,channels:list,page):
        posts_info=[]
        for channel in channels:
            channel_id = channel[1]
            self.cursor.execute("SELECT * FROM posts WHERE channel_id = %s",(channel_id,))
            posts = self.cursor.fetchall()
            for post in posts:
                posts_info.append(post)
        if page>=len(posts_info):
            page = 0
        try:
            return page, posts_info[int(page)]
        except IndexError:
            return 'no data', ''

    def posts_stats_views(self,msg_id,chan_id):
        self.cursor.execute("SELECT views_count FROM post_statistics WHERE channel_id = %s AND message_id=%s",(chan_id,msg_id))
        views = self.cursor.fetchone()
        return views[0]


    def average_cpv_in_category(self,category):
        self.cursor.execute("SELECT channel_id FROM channels WHERE channels_theme LIKE %s",(category+'%',))
        channel_ids = self.cursor.fetchall()
        cpv = []
        for id in channel_ids:
            self.cursor.execute("""SELECT cpv FROM channel_statistics WHERE channel_id = %s""",(id,))
            chan_cpv = self.cursor.fetchone()
            cpv.append(chan_cpv[0])
        res = 0.0
        for cp in cpv: 
            res+=float(cp)
        return round(res,2)


    def post_update_status_sent(self,bill_id, message_id):
        self.cursor.execute("""UPDATE posts SET message_id = %s, confirmed = 'SENT'
         WHERE bill_id = %s""",(message_id,bill_id))

    def post_update_status_done(self,bill_id):
        self.cursor.execute("""UPDATE posts SET confirmed = 'DONE'
         WHERE bill_id = %s""",(bill_id,))

    def get_post_by_bill_id(self,bill_id):
        self.cursor.execute("SELECT * FROM posts WHERE bill_id = %s",(bill_id,))
        res = self.cursor.fetchone()
        return res

    """QIWI_BILLS"""
    

    def create_qiwi_bill(self,qiwi_p2p_key, user_id,deposit,bill_id,created_date):
        self.cursor.execute("""INSERT INTO qiwi_bills 
        (qiwi_p2p_key, user_id,deposit,bill_id,created_date)
        VALUES (%s,%s,%s,%s,%s);""",
        (qiwi_p2p_key, user_id,deposit,bill_id,created_date))

    def is_exists_qiwi_bill(self, bill_id):
        self.cursor.execute('SELECT * FROM qiwi_bills WHERE bill_id = %s;', (bill_id,))
        res = self.cursor.fetchone()
        return bool(res), res

    def get_all_bills(self):
        self.cursor.execute("""SELECT user_id, bill_id,created_date FROM qiwi_bills""")
        res = self.cursor.fetchall()
        return res

    def del_bill(self,bill_id):
        self.cursor.execute("""DELETE FROM qiwi_bills WHERE bill_id = %s""",(bill_id,))


    """user_requisites"""

    def is_exist_qiwi_p2p_key(self,user_id):
        self.cursor.execute("""SELECT p2p_qiwi_token FROM user_requisites WHERE user_id = %s""",(user_id, ))
        res = self.cursor.fetchone()
        if res[0] == None: 
            return False
        else: return True


    def save_p2p_qiwi_token(self,user_id, token):
        # self.cursor.execute("""INSERT INTO user_requisites (user_id) VALUES (%s)""",(user_id,))
        self.cursor.execute("""UPDATE user_requisites SET p2p_qiwi_token = %s WHERE user_id = %s""",(token,user_id))


    def get_p2p_qiwi_token(self,user_id):
        self.cursor.execute("""SELECT p2p_qiwi_token FROM user_requisites WHERE user_id = %s""",(user_id,))
        return self.cursor.fetchone()[0]
    
    def get_channel_stat_img(self,channe_id,all=False):
        if all:
            self.cursor.execute("""SELECT * FROM channel_stat_imgs""")
            return self.cursor.fetchall()
        else: 
            self.cursor.execute("""SELECT img_link FROM channel_stat_imgs WHERE channel_id = %s""",(channe_id,))
            return self.cursor.fetchone()[0]
    
    

    def get_channel_logo_img(self,channe_id):
        self.cursor.execute("""SELECT logo_img_link FROM channel_stat_imgs WHERE channel_id = %s""",(channe_id,))
        return self.cursor.fetchone()[0]
    """BALANCES"""

    def add_balance_to_spent_on_ads(self,user_id,spent):
        self.cursor.execute("""SELECT spent_on_ad FROM users WHERE user_id = %s""",(user_id,))
        res = self.cursor.fetchone()[0]
        self.cursor.execute("""UPDATE users SET spent_on_ad = %s WHERE user_id = %s""",(int(res)+int(spent),user_id))

    
    def add_balance_to_earned(self,user_id,spent):
        self.cursor.execute("""SELECT earned FROM users WHERE user_id = %s""",(user_id,))
        res = self.cursor.fetchone()[0]
        self.cursor.execute("""UPDATE users SET earned = %s WHERE user_id = %s""",(int(res)+int(spent),user_id))

    """admin_posts"""
    def save_ads_post_for_admin(self,admin_id,text,picture_id,parse_mode,kb,name):
        self.cursor.execute("""INSERT INTO admin_ad_posts 
        (admin_id,text,picture_id,parse_mode,kb,name)
        VALUES (%s,%s,%s,%s,%s,%s);""",
        (admin_id,text,picture_id,parse_mode,kb,name))


    def select_ads_post_for_admin(self,admin_id, imgs = True):
        if imgs == 'ALL':
            self.cursor.execute("""SELECT * FROM admin_ad_posts WHERE admin_id = %s""",(admin_id,))
        elif imgs:
            self.cursor.execute("""SELECT * FROM admin_ad_posts WHERE admin_id = %s AND picture_id != '0'""",(admin_id,))
        else: 
            self.cursor.execute("""SELECT * FROM admin_ad_posts WHERE admin_id = %s AND picture_id = '0'""",(admin_id,))
        
        res = self.cursor.fetchall()
        return res


    def select_ad_post_from_db_where_increment(self,increment):
        self.cursor.execute("""SELECT * FROM admin_ad_posts WHERE id = %s""",(increment,))
        res = self.cursor.fetchone()
        return res

    def delete_ads_post_for_admin_by_id(self,post_id):
        self.cursor.execute("""DELETE FROM admin_ad_posts WHERE id = %s""",(post_id,))


    """inline_links"""
    def add_order_link_for_admin(self,identifier, channel_id,channel_link,condition, post_price,time):
        self.cursor.execute("""INSERT INTO inline_links 
        (identifier, channel_id,channel_link,condition, post_price,time)
        VALUES (%s,%s,%s,%s,%s,%s) 
        ON CONFLICT (identifier) DO NOTHING""",
        (identifier, channel_id,channel_link,condition, post_price,time))


    def select_order_link_for_admin(self,identifier):
        """identifier, channel_id,channel_link,condition, post_price,time"""
        self.cursor.execute("""SELECT * FROM inline_links WHERE identifier = %s""",(identifier,))
        res = self.cursor.fetchone()
        return res


    def version(self):
        self.cursor.execute("SELECT version();")
        print(self.cursor.fetchone())

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()