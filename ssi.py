import telebot

# Токени боти шумо мустақиман дар ин ҷо гузошта шуд
TOKEN = "8375477671:AAFboXMRKN0ON0oQz1oKBA9PNC9FpzxmaDM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.infinity_polling()
