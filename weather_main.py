import requests
import datetime
from config import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=Token_bot)
dp = Dispatcher(bot)  


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Sálem! Maǵan qala atınıń jazıń, men sizge hawa rayı esabatın jiberemen!")


@dp.message_handler(commands=["admin"])
async def lesson(message: types.Message):
    await message.reply("👀Bul adminimizning telegram linki.\nEger sizde qandayda bir soraw bolsa,adminimizga jazıń👨‍💻",
                         reply_markup=admin)

#**************************************************************************#

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Quyashli \U00002600",
        "Clouds": "Bultlı \U00002601",
        "Rain": "Jawın \U00002614",
        "Drizzle": "Jawın \U00002614",
        "Thunderstorm": "Dúbeley \U000026A1",
        "Snow": "Qar \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = f"Men {city} hawa rayin qanday eken bilmiymen?"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***<b>{datetime.datetime.now().strftime('%Y-%m-%d')}</b>***\n"
              f"Hawa rayı:{city}\nTemperatura:{cur_weather}C° {wd}\n"
              f"Íǵallıq: {humidity}%\nBasım: {pressure} \nSamal: {wind} m/s\n"
              f"Quyash shıǵıwı: {sunrise_timestamp}\nQuyash batıwı: {sunset_timestamp}\nKúnniń dawam etiw waqti: {length_of_the_day}\n"
              f"***<b>Kúnińiz jaqsı o'tisin</b>***",
              parse_mode="HTML"
              )

    except:
        await message.reply("❓ Buday atli qala joq ❗")



    

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)