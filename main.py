
import asyncio  
import random  
import string  
import re  
from telethon import TelegramClient, events  
from telethon.tl.functions.contacts import ResolveUsernameRequest  
from telethon.errors import UsernameNotOccupiedError, UsernameInvalidError  
  
API_ID = 8934899  
API_HASH = "bf3e98d2c351e4ad06946b4897374a1e"  
BOT_TOKEN = "8310654978:AAEly3ysgaOsgF06VDEtE7qdTevOx8C-ABs"  
  
tele_client = TelegramClient("botyee", API_ID, API_HASH)  
# المطور الوحيد @RR8R9    
user_states = {}  
  
@tele_client.on(events.NewMessage(pattern=r'^/start$'))  
async def start_handler(event):  
    await event.reply("أهلًا بك في بوت فحص وتوليد اليوزرات\n\n-  الأمر /generation لتوليد يوزرات .\n- الأمر /check لفحص اليوزر .")  
      
def generate_username_by_pattern(pattern):  
    letters = string.ascii_lowercase  
    digits = string.digits  
    all_chars = letters + digits  
    result = ""  
    char_map = {}  
  
    for i, char in enumerate(pattern):  
        if char == '_':  
            result += '_'  
            continue  
        if char not in char_map:  
            if i == 0:  
                char_map[char] = random.choice(letters)  
            else:  
                char_map[char] = random.choice(all_chars)  
        result += char_map[char]  
  
    return '@' + result  
  
def generate_usernames_by_pattern(pattern, count):  
    usernames = set()  
    while len(usernames) < count:  
        usernames.add(generate_username_by_pattern(pattern))  
    return list(usernames)  
  
@tele_client.on(events.NewMessage(pattern=r'^/generation'))  
async def handle_generation(event):  
    raw_text = event.raw_text  
    parts = raw_text.split()  
    if len(parts) != 2 or not re.match(r"^@[\w_]{3,}$", parts[1]):  
        await event.reply("أرسل الأمر بهذا الشكل:\n/generation @a_7_k أو @vvcvv")  
        return  
    username_pattern = parts[1][1:]   
    user_states[event.sender_id] = username_pattern  
    await event.reply("شكد عدد اليوزرات اللي تريد توليدها؟")  
  
@tele_client.on(events.NewMessage(pattern=r'^\d+$'))  
async def handle_count(event):  
    user_id = event.sender_id  
    pattern = user_states.get(user_id)  
    if pattern:  
        try:  
            count = int(event.raw_text)  
            if count > 100:  
                await event.reply("الحد الأقصى للتوليد هو 100.")  
                return  
            usernames = generate_usernames_by_pattern(pattern, count)  
            await event.reply("\n".join(usernames))  
        except ValueError:  
            await event.reply("أرسل رقم فقط.")  
        user_states.pop(user_id, None)  
  
@tele_client.on(events.NewMessage(pattern=r'^/check'))  
async def check_handler(event):  
    raw_text = event.raw_text  
    usernames = re.findall(r'@[\w_]{3,}', raw_text)  
    if not usernames:  
        await event.reply("أرسل الأمر بهذا الشكل:\n/check @username\nأو أرسل قائمة يوزرات بعد الأمر.")  
        return  
  
    results = []  
    for username in usernames:  
        uname = username.replace('@', '')  
        try:  
            result = await tele_client(ResolveUsernameRequest(uname))  
            peer = result.users[0] if result.users else result.chats[0]  
            if hasattr(peer, 'first_name'):  
                status = "ربط حساب"  
            elif hasattr(peer, 'title'):  
                if peer.broadcast:  
                    status = "ربط قناة"  
                else:  
                    status = "ربط كروب"  
            else:  
                status = "مربوط - نوع غير معروف"  
        except UsernameNotOccupiedError:  
            status = "متاح"  
        except UsernameInvalidError:  
            status = "مبند(منصة)"  
        except Exception as e:  
            status = f"خطأ: {str(e)}"  
  
        results.append(f"- {username} - ➤ {status}")  
        await asyncio.sleep(3)    
  
    await event.reply("\n".join(results[:50]))  
  
async def main():  
    await tele_client.start(bot_token=BOT_TOKEN)  
    await tele_client.run_until_disconnected()  
  
if __name__ == "__main__":  
    asyncio.run(main())
