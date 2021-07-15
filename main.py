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
from pyrogram.raw import functions, types
from pyrogram import Client, idle
from pyromod import listen
from config import Config
STATUS=Config.STATUS

USER=Config.USER
bot = Client(
    "InstaSessibon",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    workers=50,
    instagram=dict(root="instagram")
    )


async def main():
    async with bot:
        await bot.download_media(Config.INSTA_SESSIONFILE_ID, file_name=f"./{Config.USER}")
        Config.L.load_session_from_file(USER, filename=f"./{USER}")
        STATUS.add(1)

if Config.INSTA_SESSIONFILE_ID:
    bot.run(main())

bot.start()
bot.send(
    functions.bots.SetBotCommands(
        commands=[
            types.BotCommand(
                command="start",
                description="Check if bot alive"
            ),
            types.BotCommand(
                command="help",
                description="How to use"
            ),
            types.BotCommand(
                command="login",
                description="login into your Instagram account"
            ),
            types.BotCommand(
                command="logout",
                description="Logout from Instagram"
            ),
            types.BotCommand(
                command="account",
                description="Shows details of logged in account"
            ),
            types.BotCommand(
                command="posts",
                description="Download all posts from given username"
            ),
            types.BotCommand(
                command="feed",
                description="Download posts in your feed"
            ),
            types.BotCommand(
                command="igtv",
                description="Download IGTV videos of given username"
            ),
            types.BotCommand(
                command="saved",
                description="Download specified number of posts from your saved posts "
            ),
            types.BotCommand(
                command="story",
                description="Download stories of given username"
            ),
            types.BotCommand(
                command="stories",
                description="Downloads stories off all your followees"
            ),
            types.BotCommand(
                command="followers",
                description="Sends a list of followers of given username"
            ),
            types.BotCommand(
                command="followees",
                description="Sends a list followees of given username"
            ),
            types.BotCommand(
                command="fans",
                description="Get a list of followees who is following back."
            ),
            types.BotCommand(
                command="notfollowing",
                description="Get a list of followees who is not following back."
            ),
            types.BotCommand(
                command="tagged",
                description="Download all posts tagged with given username"
            ),
            types.BotCommand(
                command="highlights",
                description="Downloads highlights from given username"
            ),
            types.BotCommand(
                command="restart",
                description="Stop all processes and restart bot"
            ),
        ]
    )
)

idle()
bot.stop()

