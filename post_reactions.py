from pyrogram.errors import FloodWait, MessageIdInvalid, ReactionInvalid, ChannelPrivate
from pyrogram import Client, enums
import random
import time
import cfg


app = Client(
    "alice",
    api_id=cfg.api_id,
    api_hash=cfg.api_hash
)
app.start()

banned = []
br = []
mids = {}
print("Checking chat links...")
for link in cfg.chats:
    s = app.get_chat(link)
    if enums.ChatType.CHANNEL == s.type:
        is_channel = True
    else:
        is_channel = False
    if is_channel:
        c = app.get_chat(link).linked_chat
        link = c.id
    mids[link] = []

print("Links checked!")
print("Bot initialised")
while True:
    for link in mids:
        if link not in banned:
            try:
                message = [msg for msg in app.get_chat_history(chat_id=link, limit=1)][0]
                if not message.id in mids[link]:
                    mids[link].append(message.id)
                    if cfg.chance == 0:
                        chance = 0
                    else:
                        chance = random.choice(list(range(cfg.chance)))
                    if message.from_user:
                        user_id = message.from_user.id
                    else:
                        user_id = 0
                    for _ in range(10):
                        reaction = random.choice(cfg.reactions)
                        if reaction not in br:
                            break
                    if chance == 0 and user_id not in cfg.ignorelist:
                        print("Sending reaction...")
                        print(f"chat_id:{link}\tuser_id: {user_id}\treaction: {reaction}")
                        try:
                            app.send_reaction(link, message.id, reaction)
                        except ReactionInvalid as e:
                            print(e, reaction)
                            br.append(reaction)
            except FloodWait as e:
                print(e)
                time.sleep(e.value+2)
            except MessageIdInvalid as e:
                print(e)
            except ChannelPrivate:
                print(f"{link} is banned!")
                banned.append(link)
            except Exception as e:
                print(e)
        time.sleep(random.randint(2, 5))
