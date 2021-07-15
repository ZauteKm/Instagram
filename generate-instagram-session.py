"""
Instagram-Bot, Telegram Instagram Bot

Copyright (C) 2021 Zaute Km

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import UserIsBlocked
import asyncio
import os
from instaloader import Instaloader, TwoFactorAuthRequiredException

L = Instaloader()


async def generate():
    print("Enter your Telegram API_ID")
    API_ID = input()
    print("Enter API_HASH")
    API_HASH = input()
    print("Enter Your BOT_TOKEN from @BotFather")
    BOT_TOKEN = input()

    bot = Client("INSTASESSION", API_ID, API_HASH, bot_token=BOT_TOKEN)
    await bot.start()
    print("Now Enter your Instagram username")
    id = input()
    print("Enter Your Instagram Password")
    pwd = input()
    try:
        L.login(id, pwd)
        L.save_session_to_file(filename=f"./{id}")
    except TwoFactorAuthRequiredException:
        print(
            "Your account has Two Factor authentication Enabled.\nNow Enter the code recived on your mobile."
        )
        code = input()
        L.two_factor_login(code)
        L.save_session_to_file(filename=f"./{id}")
    except Exception as e:
        print(e)
        return
    print("Succesfully Logged into Instagram")
    while True:
        print("To send your Session file enter Your Telegram ID as Integer")
        tg_id = input()
        try:
            owner = int(tg_id)
            break
        except:
            print("Oops Thats Invalid, Enter ID as Integer")
    try:
        f = await bot.send_document(
            chat_id=owner,
            document=f"./{id}",
            file_name=tg_id,
            caption=
            "⚠️ KEEP THIS SESSION FILE SAFE AND DO NOT SHARE WITH ANYBODY",
        )
        file_id = f.document.file_id
        await bot.send_message(
            chat_id=owner,
            text=
            f"<b>INSTA_SESSIONFILE_ID</b>\n\n<code>{file_id}</code>\n\n⬆️ This StringSession is generated using https://replit.com/@ZauteKm/GenerateInstagramSession\n<b>Please Subscribe</b> ❤️ @ZauteKm"
        )
        print(
            "I have messaged you the INSTA_SESSIONFILE_ID. Check your telegram messages"
        )
    except PeerIdInvalid:
        print(
            "It seems you have not yet started the bot or Telegram ID given is invalid. Send /start to your bot first and try again"
        )
    except UserIsBlocked:
        print(
            "It seems you have BLOCKED the Bot. Unblock the bot and try again."
        )
    except Exception as e:
        print(e)
    await bot.stop()
    os.remove(f"./{id}")
    os.remove("INSTASESSION.session")


loop = asyncio.get_event_loop()
loop.run_until_complete(generate())
