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

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from config import Config
from utils import *
import os
from instaloader import Profile, TwoFactorAuthRequiredException, BadCredentialsException
from asyncio.exceptions import TimeoutError

USER=Config.USER
STATUS=Config.STATUS
OWNER=Config.OWNER
HOME_TEXT=Config.HOME_TEXT

insta = Config.L


@Client.on_message(filters.command("login") & filters.private)
async def login(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER), 
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122")
					],
                    [
                        InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
						InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
                    ],
                    [
                        InlineKeyboardButton("👨🏼‍🦯How To Use?", callback_data="help#subin")

                    ]
					
				]
			)
		)
        return
    username=USER
    if 1 in STATUS:
        m=await bot.send_message(message.from_user.id, "Fetching details from Instagram")
        profile = Profile.own_profile(insta.context)
        mediacount = profile.mediacount
        name = profile.full_name
        bio = profile.biography
        profilepic = profile.profile_pic_url
        igtvcount = profile.igtvcount
        followers = profile.followers
        following = profile.followees
        await m.delete()
        await bot.send_photo(
            chat_id=message.from_user.id,
            caption=f"You are already Logged In as {name}\n\n**Your Account Details**\n\n🏷 **Name**: {name}\n🔖 **Username**: {profile.username}\n📝 **Bio**: {bio}\n📍 **Account Type**: {acc_type(profile.is_private)}\n🏭 **Is Business Account?**: {yes_or_no(profile.is_business_account)}\n👥 **Total Followers**: {followers}\n👥 **Total Following**: {following}\n📸 **Total Posts**: {mediacount}\n📺 **IGTV Videos**: {igtvcount}",
            photo=profilepic
            )
        return
    while True:
        try:
            password = await bot.ask(text = f"Helo {USER} Enter your Instagram Password to login into your account 🙈", chat_id = message.from_user.id, filters=filters.text, timeout=30)
        except TimeoutError:
            await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /login")
            return
        passw=password.text
        break
    try:
        insta.login(username, passw)
        insta.save_session_to_file(filename=f"./{username}")
        f=await bot.send_document(
            chat_id=message.from_user.id,
            document=f"./{username}",
            file_name=str(message.from_user.id),
            caption="⚠️ KEEP THIS SESSION FILE SAFE AND DO NOT SHARE WITH ANYBODY"
            )
        file_id=f.document.file_id
        await bot.send_message(message.from_user.id, f"Now go to [Heroku](https://dashboard.heroku.com/apps) and set Environment variable.\n\n\n**KEY**: <code>INSTA_SESSIONFILE_ID</code>\n\n**VALUE**: <code>{file_id}</code>\n\nIf you do not set this you may need to Login again When Heroku restarts.", disable_web_page_preview=True)
        STATUS.add(1)
        m=await bot.send_message(message.from_user.id, "Fetching details from Instagram")
        profile = Profile.from_username(insta.context, username)
        mediacount = profile.mediacount
        name = profile.full_name
        bio = profile.biography
        profilepic = profile.profile_pic_url
        igtvcount = profile.igtvcount
        followers = profile.followers
        following = profile.followees
        await m.delete()
        await bot.send_photo(
            chat_id=message.from_user.id,
            caption=f"🔓Succesfully Logged In as {name}\n\n**Your Account Details**\n\n🏷 **Name**: {name}\n🔖 **Username**: {profile.username}\n📝 **Bio**: {bio}\n📍 **Account Type**: {acc_type(profile.is_private)}\n🏭 **Is Business Account?**: {yes_or_no(profile.is_business_account)}\n👥 **Total Followers**: {followers}\n👥 **Total Following**: {following}\n📸 **Total Posts**: {mediacount}\n📺 **IGTV Videos**: {igtvcount}",
            photo=profilepic
            )
    except TwoFactorAuthRequiredException:
        while True:
            try:
                code = await bot.ask(text = "Oh!!\nYour Instagram account has Two Factor Authentication enabled🔐\n\nAn OTP has been sent to your phone\nEnter the OTP", chat_id = message.from_user.id, filters=filters.text, timeout=30)
            except TimeoutError:
                await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /login")
                return
            codei=code.text
            try:
                codei=int(codei)
                break
            except:
                await bot.send_message(message.from_user.id, "OTP Should be Integer")
                continue
        try:
            insta.two_factor_login(codei)
            insta.save_session_to_file(filename=f"./{username}")
            f=await bot.send_document(
                chat_id=message.from_user.id,
                document=f"./{username}",
                file_name=str(message.from_user.id),
                caption="⚠️ KEEP THIS SESSION FILE SAFE AND DO NOT SHARE WITH ANYBODY"
                )
            file_id=f.document.file_id
            await bot.send_message(message.from_user.id, f"Now go to [Heroku](https://dashboard.heroku.com/apps) and set Environment variable.\n\n\n**KEY**: <code>INSTA_SESSIONFILE_ID</code>\n\n**VALUE**: <code>{file_id}</code>\n\nIf you do not set this you may need to Login again When Heroku restarts.", disable_web_page_preview=True)
            STATUS.add(1)
            m=await bot.send_message(message.from_user.id, "Fetching details from Instagram")
            profile = Profile.from_username(insta.context, username)
            mediacount = profile.mediacount
            name = profile.full_name
            bio = profile.biography
            profilepic = profile.profile_pic_url
            igtvcount = profile.igtvcount
            followers = profile.followers
            following = profile.followees
            await m.delete()
            await bot.send_photo(
                chat_id=message.from_user.id,
                caption=f"🔓Succesfully Logged In as {name}\n\n**Your Account Details**\n\n🏷 **Name**: {name}\n🔖 **Username**: {profile.username}\n📝**Bio**: {bio}\n📍**Account Type**: {acc_type(profile.is_private)}\n🏭**Is Business Account?**: {yes_or_no(profile.is_business_account)}\n👥**Total Followers**: {followers}\n👥**Total Following**: {following}\n📸**Total Posts**: {mediacount}\n📺**IGTV Videos**: {igtvcount}",
                photo=profilepic
                )
        except BadCredentialsException:
            await bot.send_message(message.from_user.id, "Wrong Credentials\n\n/login again")
            pass
        except Exception as e:
            await bot.send_message(message.from_user.id, f"{e}\nTry /login again")
        print("Logged in")
    except Exception as e:
        await bot.send_message(message.from_user.id, f"{e}\nTry again or Report this Issue to [Developer](tg://user?id=626664225)")

@Client.on_message(filters.command("logout") & filters.private)
async def logout(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER), 
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122")
					],
                    [
                        InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
						InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
                    ],
                    [
                        InlineKeyboardButton("👨🏼‍🦯How To Use?", callback_data="help#subin")

                    ]
					
				]
			)
		)
        return
    if 1 in STATUS:
        await message.reply_text("Succesfully Logged Out")
        STATUS.remove(1)
        os.remove(f"./{USER}")
    else:
        await message.reply_text("You are not Logged in\nUse /login first")
