from vkbottle.bot import Bot, Message, rules
import sqlite3
import random
import json
from vkbottle_types.objects import MessagesForward
from config import TOKEN, group_id, hate_photo
import keyb as kb
import functions as fc

bot = Bot(TOKEN)
bot.labeler.vbml_ignore_case = True

connection = sqlite3.connect('data.db')
q = connection.cursor()

q.execute(
	'CREATE TABLE IF NOT EXISTS users (user_id integer, hated text, hatedphoto text);')
connection.commit()

@bot.on.chat_message(rules.ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"]))
async def chat_invite(message: Message):
	message.action.member_id = message.action.member_id or message.from_id
	if message.action.member_id == -message.group_id:
		await message.answer('здарова, я хейт бот, дай мне цель я ее захуярю\nчтобы я не тупил дай мне админку в беседе\n/help - помощь', keyboard=kb.addtochat)


@bot.on.chat_message(text='/help')
async def help(message: Message):
	if message.from_id > 0:
		await message.answer('Вот что я умею:\n+хейт - начать хейтить пользователя\n-хейт - прекратить хейт\n+хейтфото - начать хейтить фотографиями\n-хейтфото - прекратить хейт фотографиями\n\nИспользовать команды могут только администраторы беседы!', keyboard=kb.addtochat)

@bot.on.chat_message(text='+хейт')
async def text_hate_starter(message: Message):
	if message.from_id > 0:
		if message.reply_message is not None or len(message.fwd_messages) != 0:
			if message.reply_message is not None:
				from_id = message.reply_message.from_id
			else:
				from_id = message.fwd_messages[0].from_id
			admins = await fc.admin_check(message.peer_id)
			if message.from_id in admins:
				if from_id == -group_id:
					await message.answer('слыш ты че ахуел, я сам себя хейтить не буду')
				else:
					await message.answer(await fc.add_to_texthate(from_id))
			else:
				await message.answer('нихуя ты не админ беседы')
		else:
			await message.answer('Используй данную команду ответив на сообщение или переслав его')


@bot.on.chat_message(text='-хейт')
async def text_hate_starter(message: Message):
	if message.from_id > 0:
		if message.reply_message is not None or len(message.fwd_messages) != 0:
			if message.reply_message is not None:
				from_id = message.reply_message.from_id
			else:
				from_id = message.fwd_messages[0].from_id
			admins = await fc.admin_check(message.peer_id)
			if message.from_id in admins:
				await message.answer(await fc.delete_from_texthate(from_id))
			else:
				await message.answer('нихуя ты не админ беседы')
		else:
			await message.answer('Используй данную команду ответив на сообщение или переслав его')


@bot.on.chat_message(text='+хейтфото')
async def text_hate_starter(message: Message):
	if message.from_id > 0:
		if message.reply_message is not None or len(message.fwd_messages) != 0:
			if message.reply_message is not None:
				from_id = message.reply_message.from_id
			else:
				from_id = message.fwd_messages[0].from_id
			admins = await fc.admin_check(message.peer_id)
			if message.from_id in admins:
				if from_id == -group_id:
					await message.answer('слыш ты че ахуел, я сам себя хейтить не буду')
				else:
					await message.answer(await fc.add_to_photohate(from_id))
			else:
				await message.answer('нихуя ты не админ беседы')
		else:
			await message.answer('Используй данную команду ответив на сообщение или переслав его')


@bot.on.chat_message(text='-хейтфото')
async def text_hate_starter(message: Message):
	if message.from_id > 0:
		if message.reply_message is not None or len(message.fwd_messages) != 0:
			if message.reply_message is not None:
				from_id = message.reply_message.from_id
			else:
				from_id = message.fwd_messages[0].from_id
			admins = await fc.admin_check(message.peer_id)
			if message.from_id in admins:
				await message.answer(await fc.delete_from_photohate(from_id))
			else:
				await message.answer('нихуя ты не админ беседы')
		else:
			await message.answer('Используй данную команду ответив на сообщение или переслав его')


@bot.on.chat_message()
async def hanbdler(message: Message):
	await fc.set_hate(message.from_id)
	texthate = q.execute('SELECT hated FROM users WHERE user_id = ?', (message.from_id,)).fetchone()[0]
	photohate = q.execute('SELECT hatedphoto FROM users WHERE user_id = ?', (message.from_id,)).fetchone()[0]
	if int(texthate) == 1 or int(photohate) == 1:
		if int(texthate) == 1 and int(photohate) == 0:
			text = await fc.check_texts()
			await message.answer(random.choice(text), forward=MessagesForward(peer_id=message.peer_id, conversation_message_ids=[message.conversation_message_id], is_reply=True).json())
		elif int(photohate) == 1 and int(texthate) == 0:
			await message.answer(attachment=random.choice(hate_photo), forward=MessagesForward(peer_id=message.peer_id, conversation_message_ids=[message.conversation_message_id], is_reply=True).json())
		elif int(photohate) == 1 and int(texthate) == 1:
			text = "[id{}|{}]".format(message.from_id, random.choice(await fc.check_texts()))
			await message.answer(text, attachment=random.choice(hate_photo), forward=MessagesForward(peer_id=message.peer_id, conversation_message_ids=[message.conversation_message_id], is_reply=True).json())

@bot.on.private_message()
async def welcome(message: Message):
	keyboard = await kb.jointogroup(message.from_id)
	await message.answer('здарова, я хейт бот, дай мне цель и я ее захуярю\nРаботаю только в беседах\n\nтыкай по клавиатуре ниже', keyboard=keyboard)


if __name__ == '__main__':
	bot.run_forever()