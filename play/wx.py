from wxpy import *
bot = Bot(console_qr=True)
my_friend = bot.friends().search('Loading')[0]
print(my_friend)