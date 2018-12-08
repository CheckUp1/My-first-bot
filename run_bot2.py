import requests
import vk_api

from Griz.config import *


def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text})


vk_bot = vk_api.VkApi(token=TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll['ts']
print("Готов к работе")
# +str(long_poll)}

while True:
    long_poll = requests.get(
        'https://{server}?act={act}&key={key}&ts={ts}&wait=1000'.format(server=server,
                                                                        act='a_check',
                                                                        key=key,
                                                                        ts=ts)).json()
    update = long_poll['updates']

    if update[0][0] == 4:
        print(update)
        user_id = update[0][3]
        user_name = vk_bot.method('users.get', {'user_ids': user_id})

        print(str(user_name[0]['first_name']) + ' ' +
              str(user_name[0]['last_name']) + ' написал(a) боту - ' + str(update[0][6]))
        text = update[0][6].lower()
        if 'привет' in str(text):
            write_msg(user_id, 'Привет, ' + (
                user_name[0]['first_name']) + ". \n Советую тебе послушать (Don't panic - Coldplay). \n Нравится?")
        elif "да" in str(text):
            write_msg(user_id, 'Рад это слышать, если хочешь еще напиши - (хочу)')
        elif "хочу" in str(text):
            write_msg(user_id, 'Предлагаю послушать My blood - Twenty one pilots ')
        elif "нет" in str(text):
            write_msg(user_id, 'Может тогда (She moves in her own way - The kooks')
        else:
            write_msg(user_id,
                      'Извени либо ты задаешь не правильную команду, либо я на это не запрограммирован. '
                      '\n P.S. Строго между нами , разраб туповат для чего то более)))')
    # меняем ts для следующего запроса
    ts = long_poll['ts']
