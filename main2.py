import pymongo
from pyrogram import * 
from pyrogram.types import * 
from pyrogram.errors import * 

from pyromod import listen

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

MONGO = "mongodb+srv://devcoder:aaee1122@cluster0.m4rtiot.mongodb.net/?retryWrites=true&w=majority"

mongo = MongoClient(MONGO)

db = mongo.wbb

usersdb = db.users
sudousersdb = db.sudousers
groupsdb = db.groups

app = Client("db",12643300,"73c1a336adc28a59661ff7761ff02672","5924205984:AAFHMgblw7hvw9WZahepCgRESke886KHA0s")

sudo = int(5814324132)

async def is_user(user_id:int) -> bool:
	user = await usersdb.find_one({"user_id":user_id})
	if not user:
		return False
	return True

async def add_user(user_id:int) -> bool:
	is_served = await is_user(user_id=user_id)
	if is_served:
		return
	return usersdb.insert_one({"user_id":user_id})
	
async def get_users() -> list:
	users_list = []
	async for user in usersdb.find_one({"user_id":{"$gt":0}}):
		users_list.append(user)
	return users_list
	
async def is_group(chat_id:int) -> bool:
	group = await groupsdb.find_one({"chat_id":chat_id})
	if not group:
		return False
	return True

async def add_group(chat_id:int) -> bool:
	is_served = await is_group(chat_id=chat_id)
	if is_served:
		return
	return await groupsdb.insert_one({"chat_id":chat_id})
	
async def get_groups() -> list:
	groups_list = []
	async for group in groupsdb.find_one({"chat_id":{"$gt":0}}):
		groups_list.append(group)
	return groups_list
	
async def get_sudoers() -> list:
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]
    
async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.append(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True


async def remove_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.remove(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True
    
users_keyboard = InlineKeyboardMarkup([
[
InlineKeyboardButton("المطور",user_id=sudo),
InlineKeyboardButton("source",url="xco_de.t.me")
]
])

dev_key = ReplyKeyboardMarkup([
[
("قسم المطورين")
],
[
("رفع مطور"),("تنزيل مطور")
],
[
("قسم الاذاعة")
],
[
("اذاعة للخاص"),("توجية للخاص")],
[("اذاعة جروبات"),("توجية جروبات")
],
[
("قسم الاحصائيات")
],
[
("عرض الاعضاء"),("عرض المجموعات")],
[("نسخه للاعضاء"),("نسخه للمجموعات")
],
[
("حذف الكيبورد 🔽")
]])

@app.on_message(filters.command("start")&filters.private&filters.incoming&filters.user(sudo))
async def st(c:Client,m:Message):
	await m.reply("""💌╖اهلا بيك حبيبي آلمـطـور
⚙️╢ تقدر تتحكم باوامر البوت عن طريق
🔍╢ الكيبور اللي ظهرتلك تحت ↘️
🔰╜ للدخول لقناة السورس @xco_de"""
,reply_markup=dev_key,
reply_to_message_id=m.id
)

@app.on_message(filters.command("start")&filters.private&filters.incoming)
async def start(c:Client,m:Message):
	user = m.from_user.id
	
	if user in await get_sudoers():
		await m.reply("""💌╖اهلا بيك حبيبي آلمـطـور
⚙️╢ تقدر تتحكم باوامر البوت عن طريق
🔍╢ الكيبور اللي ظهرتلك تحت ↘️
🔰╜ للدخول لقناة السورس @xco_de"""
,reply_markup=dev_key,
reply_to_message_id=m.id
)

	else:
		await m.reply("**Hi Bro in our Bot ✨",reply_markup=users_keyboard)
		

if __name__ == "__main__":
	app.run()
	
	
