import getpass
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
import configparser
import os


#///////////////////FOR LOGIN
class TG_CONN(): 

    async def login(self, phone):
            data_saved_bool = os.path.exists(f'./adx_graph/accounts_info/{phone}.data')
            await self.tg_connect(phone,data_saved_bool)

    async def tg_connect(self, phone, data_saved_bool):
        if data_saved_bool:
            await self.login_api(phone)
        else:
            cpass = configparser.RawConfigParser()
            cpass.add_section('cred')
            xid = input("введите api ID : ")
            cpass.set('cred', 'id', xid)
            xhash = input("введите hash ID : ")
            cpass.set('cred', 'hash', xhash)
            xphone = phone
            cpass.set('cred', 'phone', xphone)
            try:
                setup = open(f'./adx_graph/accounts_info/{phone}.data', 'w')
            except FileNotFoundError:
                print("создайте папку accounts_info")
            cpass.write(setup)
            setup.close()
            print("данные сохранени ")
            
            print('питаемся войти......')
            global file_rem
            file_rem = False
            self.login_api(phone)
            if file_rem == False:
                file = open("accounts.txt", 'a')
                file.write(f'\n{phone}')
                file.close
            
            
    async def login_api(self, phone):
        account_data = configparser.RawConfigParser()
        account_data.read(f'./adx_graph/accounts_info/{phone}.data')
        try:
            api_id = account_data['cred']['id']
            api_hash = account_data['cred']['hash']
            phone = account_data['cred']['phone']
            client = TelegramClient(phone, api_id, api_hash)
        except KeyError:
            pass
        try:
            client.connect()
        except:
            print("struct.error")
            client.disconnect()
            os.remove(f"{phone}.session")

        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
            except:
            #     print("The api_id/api_hash combination is invalid ")
                print("Удаляем сохраненные данные, попробуйте еще раз")
                # os.remove(f"{phone}.session")
                os.remove(f'./adx_graph/accounts_info/{phone}.data')
                file_rem = True
                client.disconnect()
                os.remove(f"{phone}.session")
            try:
                client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                client.sign_in(password=getpass.getpass())
            except ValueError:
                file_rem = True
                if file_rem == 0:
                    print("Ошибка")
                os.remove(f'./adx_graph/accounts_info/{phone}.data')
                client.disconnect()
                os.remove(f"{phone}.session")
            except FileNotFoundError:
                print("файли уже были удалени")
                client.disconnect()
                os.remove(f"{phone}.session")
            except ConnectionError:
                print("Была найдена ошика, повторите попитку")
        else:
            
            print(f"TG {phone} loggined sucssesfully!")
            
        #//////////////////FOR RETURN CLIENT
    async def client_up(self, phone):
        account_data = configparser.RawConfigParser()
        account_data.read(f'./adx_graph/accounts_info/{phone}.data')
        print(phone)
        try:
            api_id = account_data['cred']['id']
            api_hash = account_data['cred']['hash']
            phone = account_data['cred']['phone']
            client = TelegramClient(f'./adx_graph/sessions/{phone}', api_id, api_hash)
        except KeyError:
            print('Eще нет файла с данными об аккаунте, пожалуйста запустите с флагом -login')
            # Делать при ошибки считивания с файла параметров для входа
        await client.connect()
        return client

import random
def get_phones(accounts):
    accounts = [acc.strip('\n') for acc in accounts if '\n' in acc]
    random.shuffle(accounts)
    for i in accounts:
        if i == '':
            accounts.remove(i)
    return accounts

tg_conn = TG_CONN()