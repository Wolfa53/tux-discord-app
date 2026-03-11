import discord, requests, json
from datetime import datetime
from zoneinfo import ZoneInfo

msg = "Error: UnboundLocalError: `msg` not found."
with open('bot_token.txt', 'r') as file:
   TOKEN = file.read()

today_cal = requests.get("https://en.pronouns.page/api/calendar/today")
def page(username):
    return json.loads(requests.get(f"https://en.pronouns.page/api/profile/get/{username}?version=2").text)
class MyClient(discord.Client):
    user: discord.ClientUser
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('--------')

    async def on_message(self, message):
        msg = ''
        if message.content.startswith(';page'):
            args = message.content.casefold().split()
            try:
                info = args[1]
            except IndexError or ValueError:
                info = 'help'
            try:
                user = args[2]
            except IndexError or ValueError:
                user = 'wolfa53_'

            user_page = page(user)
            avatar = user_page['avatar']
            if info == "avatar" or info == "pfp":
                msg = avatar

            elif info == "opinions":
                for i, opinion in enumerate(list(user_page['profiles']['en']['opinions'].keys())):
                    try:
                        msg = f"{msg}\n\n{opinion}(icon goes here?)"
                    except NameError:
                        msg = f"{opinion}(icon goes here?)"
                    for j, oattr in enumerate(user_page['profiles']['en']['opinions'][opinion]):
                        msg = f"{msg}\n {oattr}: {user_page['profiles']['en']['opinions'][opinion][oattr]}"
                        if j == 3:
                            if user_page['profiles']['en']['opinions'][opinion][oattr] == "bold":
                                msg = f"{msg}\n {oattr}: **bold**"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "italics":
                                msg = f"{msg}\n {oattr}: *italics*"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "small":
                                msg = f"{msg}\n-# {oattr}: small"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "bold-italics":
                                msg = f"{msg}\n {oattr}: *\**bold & italics*\**"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "spoiler":
                                msg = f"{msg}\n {oattr}: ||spoiler||"

            elif info in ("pronouns names"):
                for i, item in enumerate(user_page['profiles']['en'][info]):
                    msg = f"{msg}\n{item['value']} - {item['opinion']}"

            elif info == "age":
                for cEvent in user_page['profiles']['en']['customEvents']:
                    if "birthday" in cEvent['name'].casefold():
                        msg = f"Age: {user_page['profiles']['en']['age']}\nBirthday: {cEvent['month']}-{cEvent['day']}"
                        break

            elif info == "flags":
                msg = "Flags:"
                for flag in user_page['profiles']['en']['flags']:
                    msg = f"{msg}\n{flag}"
                if len(user_page['profiles']['en']['customFlags']):
                    msg = (f"{msg}\n\nCustom Flags:")
                    for j in range(len(user_page['profiles']['en']['customFlags'])):
                        cflag = user_page['profiles']['en']['customFlags'][j]['name']
                        msg = f"{msg}\n{cflag}"

            elif info in ("description links"):
                msg = user_page['profiles']['en'][info]

            elif info == "timezone" or info == "tz":
                msg = user_page['profiles']['en']['timezone']['tz']

            elif info == "words":
                for i, cat in enumerate(user_page['profiles']['en'][info]):
                    msg = f"{msg}\n**{cat['header']}**"
                    for word in user_page['profiles']['en'][info][i]['values']:
                        if word['opinion'] == "meh":
                            opinion = ":thumbsup: (meh)"
                        elif word['opinion'] == "yes":
                            opinion = "**:heart: (yes)**"
                        elif word['opinion'] == "jokingly":
                            opinion = ":stuck_out_tongue: (jokingly)"
                        elif word['opinion'] == "no":
                            opinion = ":thumbsdown: (no)"
                        elif word['opinion'] == "close":
                            opinion = ":busts_in_silhouette: (close only)"
                        else:
                            opinion = word['opinion']
                        msg = f"{msg}\n{word['value']} - {opinion}"

            elif info == "help":
                msg = "The page command is used to find information from a user's pronoun page.\nUsage: `;page *info* *user*`\n 'info' is the information you want to receive, 'user' is the username of the pronoun page account. Contact Aki (run `;about` for contact info) for further assistance if needed."

            elif info == "all":
#                try:
                for i, opinion in enumerate(list(user_page['profiles']['en']['opinions'].keys())):
                    msg = f"{msg}\n\n{opinion}(icon goes here?)"
                    for j, oattr in enumerate(user_page['profiles']['en']['opinions'][opinion]):
                        msg = f"{msg}\n-# {oattr}: {user_page['profiles']['en']['opinions'][opinion][oattr]}"
                        if j == 3:
                            if user_page['profiles']['en']['opinions'][opinion][oattr] == "bold":
                                msg = f"{msg}\n {oattr}: **bold**"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "italics":
                                msg = f"{msg}\n {oattr}: *italics*"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "small":
                                msg = f"{msg}\n-# {oattr}: small"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "bold-italics":
                                msg = f"{msg}\n {oattr}: *\**bold & italics*\**"
                            elif user_page['profiles']['en']['opinions'][opinion][oattr] == "spoiler":
                                msg = f"{msg}\n {oattr}: ||spoiler||"
                msg = f"{msg}\n\n**Names**: "
                for i, item in enumerate(user_page['profiles']['en']['names']):
                    item = f"{item['value']} - {item['opinion']}"
                    msg = f"{msg}\n{item}"
#                except:
#                    pass
                msg = f"{msg}\n\n**Pronouns**: "
                for i, item in enumerate(user_page['profiles']['en']['pronouns']):
                    msg = f"{msg}\n{item['value']} - {item['opinion']}"

                msg = f"{msg}\n\n**Description**: {user_page['profiles']['en']['description']}"
                msg = f"{msg}\n**Links**: {user_page['profiles']['en']['links']}"
                for cEvent in user_page['profiles']['en']['customEvents']:
                    if "birthday" in cEvent['name'].casefold():
                        msg = f"{msg}\n**Age**: {user_page['profiles']['en']['age']}\n**Birthday**: {cEvent['month']}/{cEvent['day']}"
                        break
                msg = f"{msg}\n**Timezone**: {user_page['profiles']['en']['timezone']['tz']}"
                msg = f"{msg}\n**Flags**:"
                for flag in user_page['profiles']['en']['flags']:
                    msg = f"{msg}\n{flag}"
                if len(user_page['profiles']['en']['customFlags']):
                    msg = (f"{msg}\n\nCustom Flags:")
                    for j in range(len(user_page['profiles']['en']['customFlags'])):
                        cflag = user_page['profiles']['en']['customFlags'][j]['name']
                        msg = f"{msg}\n{cflag}"
            else:
                msg = "Invalid info option (or i haven't set it up yet be patient mf grr)\nUse `;page help` or ask Aki for help."
            
            for opinion in user_page['profiles']['en']['opinions']:
                msg.replace(opinion, user_page['profiles']['en']['opinions'][opinion]['description'])

        elif ';cal' == message.content:
            msg = today_cal.text.split(',')[3].split('":')[1].replace('"[English]', 'Today is').replace('"', '')

        elif message.content.startswith(';tz'):
            args = message.content.split()
            des_tz = args[1]
            msg = datetime.now(tz=ZoneInfo(des_tz)).strftime("%Z:\n\n%H:%M:%S\n%a, %d/%m/%y")

   
        elif message.content.startswith(";def"):
            #MAKE DICT!
            pass
            
        elif message.content == (';linux'):
            msg = 'is peak'

        elif message.content == ";ying":
            msg = "yang"

        elif message.content == ';ping':
            msg = 'pong'

        elif message.content == ';test':
            msg = 'working'

        elif message.content == ";cow":
            msg = "https://tenor.com/view/weird-gif-9742017\npeak."

        elif ';hello' == message.content:
            msg = f'Hello, {message.author.mention} !!'

#        elif message.content.startswith(';event'):
#            events = requests.get("guild_id")
#            msg = events.text
#            print(events.text)
#            event = None
#            if event.status == 2:
#                event.channel.send(f"Haii everyone! It's time for {event.name} !! It ends at {event.end_time}, so join {event.user_count} other users before it's over! {event.description}\n{event.cover_image}")
#            if event.status == 3:
#                event.channel.send(f"{event.name} is now over, come back at {event.start_time}!")
#            return
        
        elif ';help' == message.content:
            msg = "Here is a list of all commands for the Tux bot:\n`;help` - brings up this help menu\n`;about` - displays basic information about the bot\n`;cow` - displays a gif of a cow\n`;hello` - says hello back\n`;test` - responds 'working'\n`;ping` - responds 'pong'\n`;ying` - responds 'yang'\n`;linux` - responds 'is peak'\n`;tz {timezone_id}` - shows the current time in the given timezone\n`;cal` - shows today's queer calendar entries from pronouns.page\n`;page help` - displays the help menu for all pronouns.page card commands\n"

        elif ';about' == message.content:
            msg = "This is the Tux bot, created and developed by Aki.\nContact them through the [Tux Bot discord server](https://discord.gg/xRdT8ZeAqc)"

        else:
            return
        
        try:
            msg = msg.replace('\\n', '\n')
        except UnboundLocalError as e:
            msg = f"UnboundLocalError: {e}"
        await message.channel.send(msg)

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)