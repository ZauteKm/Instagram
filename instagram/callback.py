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
from instaloader import Profile
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong

HELP=Config.HELP
session=f"./{USER}"

STATUS=Config.STATUS

insta = Config.L

@Client.on_callback_query()
async def cb_handler(bot: Client, query: CallbackQuery):
    cmd, username = query.data.split("#")
    profile = Profile.from_username(insta.context, username)
    mediacount = profile.mediacount
    name = profile.full_name
    profilepic = profile.profile_pic_url
    igtvcount = profile.igtvcount
    followers = profile.followers
    folllowing = profile.followees
    
    if query.data.startswith("help"):
        await query.message.edit_text(
            HELP,
            reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
					InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122"),
                    InlineKeyboardButton("⚙️Update Channel", url="https://t.me/subin_works")
				],
				[
					InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
					InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
				]
			]
			)
		)
    
    
    elif query.data.startswith("ppic"):
        profile = Profile.from_username(insta.context, username)
        profilepichd = profile.profile_pic_url
        await query.answer()
        await bot.send_document(chat_id=query.from_user.id, document=profilepichd, file_name=f"{username}.jpg", force_document=True)
    
    
   
    elif query.data.startswith("post"):
        await query.message.delete()
        await bot.send_message(
            query.from_user.id,
            f"What type of post do you want to download?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Photos", callback_data=f"photos#{username}"),
                        InlineKeyboardButton("Videos", callback_data=f"video#{username}")
                    ]
                ]
            )
        )
    

    

    elif query.data.startswith("photo"):
        if mediacount==0:
            await query.edit_message_text("There are no posts by the user")
            return
        m= await query.edit_message_text("Starting Downloading..\nThis may take time depending upon number of Posts.")      
        dir=f"{query.from_user.id}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-videos",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
            ]
        await download_insta(command, m, dir)
        chat_id=query.from_user.id
        await upload(m, bot, chat_id, dir)
    


    elif query.data.startswith("video"):
        if mediacount==0:
            await query.edit_message_text("There are no posts by the user")
            return
        m= await query.edit_message_text("Starting Downloading..\nThis may take longer time Depending upon number of posts.")    
        dir=f"{query.from_user.id}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-pictures",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
            ]
        await download_insta(command, m, dir)
        chat_id=query.from_user.id
        await upload(m, bot, chat_id, dir)

    elif query.data.startswith("igtv"):
        await query.message.delete()
        await bot.send_message(
            query.from_user.id,
            f"Do you Want to download all IGTV posts?\nThere are {igtvcount} posts.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Yes", callback_data=f"yesigtv#{username}"),
                        InlineKeyboardButton("No", callback_data=f"no#{username}")
                    ]
                ]
            )
        )
    elif query.data.startswith("yesigtv"):
        if igtvcount==0:
            await query.edit_message_text("There are no IGTV posts by the user")
            return
        m= await query.edit_message_text("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
        dir=f"{query.from_user.id}/{username}"

        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--igtv",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
            ]
        await download_insta(command, m, dir)
        chat_id=query.from_user.id
        await upload(m, bot, chat_id, dir)



    elif query.data.startswith("followers"):
        await query.message.delete()
        chat_id=query.from_user.id
        m=await bot.send_message(chat_id, f"Fetching Followers List of {name}")
        f = profile.get_followers()
        followers=f"**Followers List for {name}**\n\n"
        for p in f:
            followers += f"\n[{p.username}](www.instagram.com/{p.username})"
        try:
            await m.delete()
            await bot.send_message(chat_id=chat_id, text=followers)
        except MessageTooLong:
            followers=f"**Followers List for {name}**\n\n"
            f = profile.get_followers()
            for p in f:
                followers += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s followers.txt", "w")
            text_file.write(followers)
            text_file.close()
            await bot.send_document(chat_id=chat_id, document=f"./{username}'s followers.txt", caption=f"{name}'s followers\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
            os.remove(f"./{username}'s followers.txt")
    



    
    elif query.data.startswith("followees"):
        await query.message.delete()
        chat_id=query.from_user.id
        m=await bot.send_message(chat_id, f"Fetching Followees of {name}")
        
        f = profile.get_followees()
        followees=f"**Followees List for {name}**\n\n"
        for p in f:
            followees += f"\n[{p.username}](www.instagram.com/{p.username})"
        try:
            await m.delete()
            await bot.send_message(chat_id=chat_id, text=followees)
        except MessageTooLong:
            followees=f"**Followees List for {name}**\n\n"
            f = profile.get_followees()
            for p in f:
                followees += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s followees.txt", "w")
            text_file.write(followees)
            text_file.close()
            await bot.send_document(chat_id=chat_id, document=f"./{username}'s followees.txt", caption=f"{name}'s followees\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
            os.remove(f"./{username}'s followees.txt")





    elif query.data.startswith("no"):
        await query.message.delete()
    


    else:
        dir=f"{query.from_user.id}/{username}"
        chat_id=query.from_user.id   
        await query.message.delete()
        m= await bot.send_message(chat_id, "Starting Downloading..\nThis may take longer time Depending upon number of posts.") 
        cmd, username = query.data.split("#")   
        if cmd == "feed":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--no-captions",
                "--no-video-thumbnails",
                "--login", USER,
                "--sessionfile", session,
                "--dirname-pattern", dir,
                ":feed"
                ]
            await download_insta(command, m, dir)
        elif cmd=="saved":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--no-captions",
                "--no-video-thumbnails",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                ":saved"
                ]
            await download_insta(command, m, dir)
        elif cmd=="tagged":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--tagged",
                "--no-captions",
                "--no-video-thumbnails",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
                ]
            await download_insta(command, m, dir)
        elif cmd=="stories":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--stories",
                "--no-captions",
                "--no-video-thumbnails",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
                ]
            await download_insta(command, m, dir)
        elif cmd=="fstories":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-captions",
                "--no-posts",
                "--no-video-thumbnails",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                ":stories"
                ]
            await download_insta(command, m, dir)
        elif cmd=="highlights":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--highlights",
                "--no-captions",
                "--no-video-thumbnails",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
                ]
            await download_insta(command, m, dir)
        await upload(m, bot, chat_id, dir)
