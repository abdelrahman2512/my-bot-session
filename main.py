import asyncio
from asyncio.exceptions import TimeoutError

from pyrogram import * 
from pyrogram.types import * 
from pyrogram.errors import * 

from pyromod import listen

import requests
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

MONGO = "mongodb+srv://devcoder:aaee1122@cluster0.m4rtiot.mongodb.net/?retryWrites=true&w=majority"

mongo = MongoClient(MONGO)

mongodb = mongo.bot
userdb = mongodb.users
sudodb = mongodb.sudo

ME = 5814324132

app_id = 12643300
api_hash = "73c1a336adc28a59661ff7761ff02672"
token = "5924205984:AAFHMgblw7hvw9WZahepCgRESke886KHA0s"

app = Client(
"s_s.",
api_id=app_id,
api_hash=api_hash,
bot_token=token
)

S_Message = """
**Hey , {} ! 

- This is string session Generator √ 
- you can get pyrogram session from here √

Just Click the button below 👇**
"""

Sub = """ 
**Sorry You must Join Bot Ch To contenu ! **

- [{}](https://t.me/xco_de)  √ 
"""

sub_bu = InlineKeyboardMarkup([[InlineKeyboardButton("source",url="xco_de.t.me")]])

start_bu = InlineKeyboardMarkup([[InlineKeyboardButton("Generate",callback_data="gen")],[InlineKeyboardButton("source",url="xco_de.t.me"),
InlineKeyboardButton("Dev >_",user_id=int(5814324132))]])

dev_key = ReplyKeyboardMarkup([[
("نسخه احتياطيه"),("اذاعه")],[
("الاحصائيات"),("استخراج جلسه")],[
("رفع مطور"),("تنزيل مطور")],[
("حذف الكيبورد 🔽")]
],resize_keyboard=True)

dev_M = "**مرحبا بك مطور البوت 🗣\nيمكنك التحكم في البوت \nعن طريق الكيبورد الذي ظهر بالاسفل 👇"

hash_M = """
**Ok Now send Your `API_HASH` To Contenu √ **
"""
ID_M = """
**Ok Now send Your `API_ID` To Contenu √**
"""
ph_M = """
**Ok Now Send Your Telegram Phone Number Like : +01111111111 √**

- Phone Number Must Be with  CountryCode .√
"""

#### ---> dev Coder <---- ###

async def is_user(user_id:int) -> bool:
	user = await userdb.find_one({"user_id":user_id})
	if not user:
		return False
	return True
	
async def add_user(user_id:int) -> bool:
	is_served = await is_user(user_id=user_id)
	if is_served:
		return
	return userdb.insert_one({"user_id":user_id})
	
async def get_users() -> list:
	users_list = []
	async for user in userdb.find({"user_id":{"$gt":0}}):
		users_list.append(user)
	return users_list

async def is_sudo(user_id:int) -> bool:
	sudo = await sudodb.find_one({"user_id":user_id})
	if not sudo:
		return False
	return True
	
async def add_sudo(user_id:int) -> bool:
	is_served = await is_sudo(user_id=user_id)
	if is_served:
		return 
	return sudodb.insert_one({"user_id":user_id})

async def del_sudo(user_id:int) -> bool:
	is_served = await is_sudo(user_id=user_id)
	if is_served:
		return sudodb.delete_one({"user_id":user_id})
	return

async def get_sudousers() -> list:
	sudo_list = []
	async for sudo in sudodb.find({"user_id":{"$gt":0}}):
		sudo_list.append(sudo)
	return sudo_list
	
### ---> dev Coder <--- ###

@app.on_message(filters.command("start")&filters.private)
@app.on_edited_message(filters.command("start")&filters.private)
async def start_app(c:Client,m:Message):
	ch_id = m.chat.id
	men = m.from_user.mention
	user = m.from_user.id
	
	if not user == ME:
		if not await is_user(user_id=user):
			New = '➕ شخص جديد دخل الى البوت !\n\n'
			New += f'👤 الأسم: {m.from_user.first_name}\n'
			New += f'🔗 رابط حسابه: {m.from_user.mention}\n'
			New += f'🆔 الايدي: {m.from_user.id}\n\n'
			New += f'🌀 اصبح عدد المستخدمين: {len(await get_users())}'
			await add_user(user_id=user)
			await app.send_message(ME,New,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{m.from_user.first_name}",user_id=int(user))]]))
		do = requests.get(f"https://api.telegram.org/bot{token}/getChatMember?chat_id=@xco_de&user_id={user}").text
		if do.count("left") or do.count("Bad Request: user not found"):
			name = (await app.get_chat("@xco_de")).title
			await m.reply(Sub.format(name), 
			reply_markup=sub_bu,
			disable_web_page_preview=True
			)
		else:
			await m.reply(S_Message.format(m.from_user.mention),
			reply_markup=start_bu
			)
	else:
		if user == ME or user in await get_users():
			await m.reply(dev_M,
			reply_markup=dev_key
			)

### ---> dev Coder <--- ###

@app.on_message(filters.command("رفع مطور","")&filters.private)
async def add_dev(c:Client,m:Message):
	chid = m.chat.id
	if m.from_user.id == ME:
		Id = await app.ask(
		chid,
		"◍ ارسل ايدي المطور \n√"
		)
		dev = Id.text
		if not is_sudo(user_id=dev):
			await add_sudo(user_id=dev)
			name = (await app.get_users(dev)).mention
			await m.reply("**◍ تم رفعة مطور بنجاح \n√**")
		else:
			await m.reply("**◍ تم اضافته للمطورين سابقاا \n√")

if __name__ == "__main__":
	app.run()
	
	
