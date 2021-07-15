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

import pytz
import asyncio
from config import Config
from datetime import datetime
import shutil
import glob
from videoprops import get_audio_properties
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
IST = pytz.timezone('Asia/Kolkata')
USER=Config.USER


session=f"./{USER}"

#A function to download content from Instagram
async def download_insta(command, m, dir):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    while True:
        output = await process.stdout.readline()
        if output == b'':
            print("Finished Output")
            break
        if output:
            datetime_ist = datetime.now(IST)
            ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
            msg="CURRENT_STATUS ⚙️ : <code>{}</code>\nLast Updated :<code>{}</code>".format(output.decode("UTF8"), ISTIME)
            msg=msg.replace(f'{dir}/', 'DOWNLOADED : ')
            try:
                await m.edit(msg)
            except:
                pass
            print(output.decode("UTF8"))
    while True:
        error = await process.stderr.readline()
        if error == b'':
            print("Finished No error")
            break
        if error:
            datetime_ist = datetime.now(IST)
            ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
            ermsg="ERROR ❌ : <code>{}</code>\nLast Updated : <code>{}</code>".format(error.decode("UTF8"), ISTIME)
            try:
                await m.edit(ermsg)
            except:
                pass
            print(error.decode("UTF8"))
    return True


def acc_type(val):
    if(val):
        return "🔒Private🔒"
    else:
        return "🔓Public🔓"

def yes_or_no(val):
    if(val):
        return "Yes"
    else:
        return "No"

#A functionUpload Content to Telegram
async def upload(m, bot, chat_id, dir):

    videos=glob.glob(f"{dir}/*.mp4")
    VDO=[]
    GIF=[]
    
    for video in videos:
        try:
            has_audio = get_audio_properties(video)
            VDO.append(video)
        except Exception as e:
            has_audio=None
            GIF.append(video)
            pass
    PIC=glob.glob(f"{dir}/*.jpg")
    
    print(f"Gif- {GIF}")
    print(f"\n\nVideo - {VDO}")
    print(f"\n\nPictures - {PIC}")


    totalpics=len(PIC)
    totalgif=len(GIF)
    totalvideo=len(VDO)
    TOTAL=totalpics+totalvideo+totalgif
    if TOTAL==0:
        await m.edit("There are nothing to Download.")
        return
    await m.edit("Now Starting Uploading to Telegram...")
    await m.pin(disable_notification=False, both_sides=True)



    total=TOTAL
    up=0
    rm=TOTAL
    if totalpics==1:
        pic=' '.join([str(elem) for elem in PIC])

        await bot.send_photo(chat_id=chat_id, photo=pic)
        up+=1
        rm-=1
        await m.edit(f"Total: {total}\nUploaded: {up} Remaining to upload: {rm}")
    if totalvideo==1:
        video=' '.join([str(elem) for elem in VDO])
        await bot.send_video(chat_id=chat_id, video=video)
        up+=1
        rm-=1
        await m.edit(f"Total: {total}\nUploaded: {up} Remaining to upload: {rm}")
    if totalgif==1:
        video=' '.join([str(elem) for elem in GIF])
        await bot.send_video(chat_id=chat_id, video=video)
        up+=1
        rm-=1
        await m.edit(f"Total: {total}\nUploaded: {up} Remaining to upload: {rm}")
    if totalpics >= 2:
        for i in range(0, len(PIC), 10):
            chunk = PIC[i:i + 10]
            print(chunk)
            media = []
            for photo in chunk:
                media.append(InputMediaPhoto(media=photo))
                up+=1
                rm-=1
            try:
                await bot.send_media_group(chat_id=chat_id, media=media, disable_notification=True)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.send_media_group(chat_id=chat_id, media=media, disable_notification=True)
            await m.edit(f"Total: {total}\nUploaded: {up} Remaining to upload: {rm}")

    if totalvideo >= 2:
        for i in range(0, len(VDO), 10):
            chunk = VDO[i:i + 10]
            print(chunk)
            media = []
            for video in chunk:
                media.append(InputMediaVideo(media=video))
                up+=1
                rm-=1
            try:
                await bot.send_media_group(chat_id=chat_id, media=media, disable_notification=True)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.send_media_group(chat_id=chat_id, media=media, disable_notification=True)
            await m.edit(f"Total: {total}\nUploaded: {up} Remaining to upload: {rm}")
    if totalgif >= 2:
        for gif in GIF:
            try:
                await bot.send_video(chat_id=chat_id, video=gif)
                up+=1
                rm-=1
                await m.edit(f"Total: {total}\nUploaded: {up} Remaining to upload: {rm}")
            except FloodWait as e:
                await bot.send_video(chat_id=chat_id, video=gif)
                up+=1
                rm-=1
                await m.edit(f"Total: {total}\nUploaded: {up} Remaining to upload: {rm}")
    await m.unpin()
    await bot.send_message(
        chat_id=chat_id,
        text=f"Succesfully Uploaded {up} Files to Telegram.\nIf you found me helpfull Join My Updates Channel",
        reply_markup=InlineKeyboardMarkup(
            [
                [
					InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
					InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122")
				],
				[
					InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
                    InlineKeyboardButton("⚡️Update Channel", url="https://t.me/subin_works")
				]
			]
			)
		)
    total=TOTAL
    up=0
    rm=TOTAL
    shutil.rmtree(dir, ignore_errors=True)
