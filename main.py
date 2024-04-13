# Importing Required Libraries, Imported os Module For Security 
import telebot
# Import the PIL package
from PIL import Image, ImageDraw, ImageFont
from englisttohindi.englisttohindi import EngtoHindi
import keep_alive




# Specify the font and size
font = ImageFont.truetype('NotoSans-Bold.ttf', 14)
fontJCO = ImageFont.truetype('NotoSans-Bold.ttf', 12)
fontFare = ImageFont.truetype('NotoSans-Bold.ttf', 18)
fontHindi = ImageFont.truetype('NotoSans-Bold.ttf', 16)


# Getting Bot Token From Secrets
# BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Creating Telebot Object
bot = telebot.TeleBot('6655445920:AAGZcbEuIyhsN8CXCVjWPCRDky6tePpCriw')

# Whenever Starting Bot
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
  bot.send_message(message.chat.id, "Welcome To The Desi Jugaad ")


@bot.message_handler(commands=['newticket'])
def new_ticket(msg):
  img = Image.open("temp.jpeg")
  draw = ImageDraw.Draw(img)
  bot.reply_to(msg, "So, You Want A Ticket")
  bot.reply_to(msg, "Follow The Instructions Below ")
  source = bot.send_message(msg.chat.id, "Tell Me Your Source Station")
  bot.register_next_step_handler(source, add_source, draw, img )


def add_source(source, draw, img):
  # SOURCE
  draw.text((210, 720), source.text.upper() , (50,50,50,200), font=font)
  draw.text((210, 695), EngtoHindi(source.text).convert , (50,50,50,200), font=fontHindi)
  # img.save("image_with_text.jpeg")
  # bot.send_message(source.chat.id, "Your Ticket Is Comming ")
  # img = Image.open("image_with_text.jpeg")
  # bot.send_photo(source.chat.id, img)  
  dest = bot.send_message(source.chat.id, "Tell Me Your Destiantion Station")
  bot.register_next_step_handler(dest, add_dest , draw, img)

def add_dest(dest, draw, img):
  # DESTINATION
  draw.text((435, 725), (dest.text).upper() , (50,50,50,200), font=font)
  draw.text((435, 700), EngtoHindi(dest.text).convert , (50,50,50,200), font=fontHindi)
  bot.send_message(dest.chat.id, "Tell Me Your Route ")
  via = bot.send_message(dest.chat.id, "Example : LDH-PNP-DLI")
  bot.register_next_step_handler(via, add_via,  draw, img )

def add_via(via, draw, img):
  # VIA
  draw.text((212, 792), via.text.upper() , (50,50,50,200), font=font)
  img.save("image_with_text.jpg")
  num = bot.send_message(via.chat.id, "Tell Me Number Of Passengers You Have ")
  bot.register_next_step_handler(num, add_num , draw, img)

def add_num(num, draw, img):
  draw.text((265, 835), num.text , (50,50,50,200), font=font)
  img.save("image_with_text.jpg")
  distance = bot.send_message(num.chat.id, "Tell Me Total Distance (Only Number)")
  bot.register_next_step_handler(distance, add_distance, draw, img )


def add_distance(distance, draw, img):
  # distance
  draw.text((428, 980), f"{distance.text} KM" , (50,50,50,200), font=font)
  img.save("image_with_text.jpg")
  fare = bot.send_message(distance.chat.id, "Tell Me Total Fare (Only Number)")
  bot.register_next_step_handler(fare, add_fare , draw, img)

def add_fare(fare, draw, img):
  # FARE
  draw.text((570, 590), f"₹{fare.text}.00/-" , (50,50,50,200), font=fontFare)
  img.save("image_with_text.jpg")
  date = bot.send_message(fare.chat.id, "Write Complete Date In Form dd-mm-yyyy")
  bot.register_next_step_handler(date, add_date , draw, img)

def add_date(date, draw, img):
  # DATE
  draw.text((212, 1023), f"JCO ON: {date.text}" , (50,50,50,200), font=font, antialias=True)
  img.save("image_with_text.png", quality=5)
  bot.send_message(date.chat.id, "Your Ticket Is Comming ")
  bot.send_document(date.chat.id, open('image_with_text.png', 'rb'))
  
# Waiting For New Messages

keep_alive.keep_alive()
bot.infinity_polling()
