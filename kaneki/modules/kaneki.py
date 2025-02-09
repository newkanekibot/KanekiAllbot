import random
import requests
from bs4 import BeautifulSoup as bs
from pyjokes import get_joke
from telethon.errors import ChatSendMediaForbiddenError

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

import kaneki.modules.kaneki_strings as kaneki_strings
from kaneki import dispatcher
from kaneki.modules.disable import DisableAbleCommandHandler
from kaneki.events import register


@register(pattern="^/joke ?(.*)")
async def joke(event):
    await event.reply(get_joke())


@register(pattern="^/insult ?(.*)")
async def insult(event):
    m = await event.reply("Generating...")
    nl = "https://fungenerators.com/random/insult/new-age-insult/"
    ct = requests.get(nl).content
    bsc = bs(ct, "html.parser", from_encoding="utf-8")
    cm = bsc.find_all("h2")[0].text
    await m.edit(f"{cm}")


@register(pattern="url ?(.*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.reply("Give some url")
        return
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.reply(
            "**Shortened url**==> {}\n**Given url**==> {}.".format(
                response_api, input_str
            ),
        )
    else:
        await event.reply("`Something went wrong. Please try again Later.`")


AD_STRINGS = (
    "_*kembali dengan versi terbaik, karna di sini aku masih menunggumu,masih tentang kamu*_",
    "_*healing terbaik jatuh kepada rebahan, jalan jalan dan makanan enak*_",
    "_*sorry I'm not a perfect person like you, also not arrogant like you,and it's not something that requires me to be jealous.*_",
    "_*maaf aku bukan orang yang sempurna sepertimu, juga tidak sombong sepertimu, dan itu bukan sesuatu yang mengharuskan saya untuk cemburu.*_",
    "_*Suara tawanya, sangat ingin ku simpan dikotak musik hatiku. Aku selalu ingin memeluknya. Biarkan pelukanku menjadi pelindungnya bahkan hatiku akan selalu menjadi rumahnya dalam jangka waktu panjang. Senyumnya selalu terukir disetiap benakku dan ciummannya seperi bunga mawar yang bermekaran setiap harinya. Ini untukmu yang pernah berbagi kehangatan padaku.*_",
)


def kaneki(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name
    reply_photo = (
        message.reply_to_message.reply_photo
        if message.reply_to_message
        else message.reply_photo
    )
    reply_photo(random.choice(kaneki_strings.KANEKI_IMG))


def diaryaryza(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(random.choice(AD_STRINGS), parse_mode=ParseMode.MARKDOWN)


__help__ = """
 ❍ `/kaneki`*:* gives random kaneki media.
 ❍ `/asupan`*:* gives random asupan medi.
 ❍ `/chika`*:* gives random chika media.
 ❍ `/wibu`*:* gives random wibu media.
 ❍ `/apakah`*:* For ask question about someone with AI.
 ❍ `/diaryaryza`*:* Check Aja.
 ❍ `/apod`*:* Get Astronomy Picture of Day by NASA.
 ❍ `/devian` <search query> ; <no of pics> *:* Devian-Art Image Search.
 ❍ `/joke`*:* To get random joke.
 ❍ `/inslut`*:* Insult someone..
 ❍ `/url <long url>`*:* To get a shorten link of long link.
"""


KANEKI_HANDLER = DisableAbleCommandHandler("kaneki", kaneki, run_async=True)
dispatcher.add_handler(KANEKI_HANDLER)

DIARYARYZA_HANDLER = DisableAbleCommandHandler("diaryaryza", diaryaryza, run_async=True)
dispatcher.add_handler(DIARYARYZA_HANDLER)

__mod_name__ = "Kaneki Extras"


__command_list__ = ["kaneki", "diaryaryza"]
__handlers__ = [KANEKI_HANDLER, DIARYARYZA_HANDLER]
