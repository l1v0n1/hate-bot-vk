import bot
import sqlite3
from config import dir_to_texts, err

connection = sqlite3.connect('data.db')
q = connection.cursor()

async def add_to_texthate(chat_id):
	q.execute(f"SELECT * FROM users WHERE user_id = {chat_id}")
	users = q.fetchall()
	if len(users) == 0:
		q.execute('INSERT INTO USERS (user_id, hated) VALUES (?,?)', (chat_id, 1))
		connection.commit()
		return 'Пользователь успешно добавлен в хейт-лист'
	else:
		request = q.execute('SELECT hated FROM users WHERE user_id = ?', (chat_id,)).fetchone()
		if int(request[0]) == 0:
			q.execute('UPDATE users SET hated = 1 WHERE user_id = ?', (chat_id,))
			connection.commit()
			return 'Пользователь успешно добавлен в хейт-лист'
		else:
			return 'Пользователь уже находится в хейт-листе'

async def delete_from_texthate(chat_id):
	request = q.execute('SELECT hated FROM users WHERE user_id = ?', (chat_id,)).fetchone()
	if int(request[0]) == 1:
		q.execute('UPDATE users SET hated = 0 WHERE user_id = ?', (chat_id,))
		connection.commit()
		return 'Пользователь больше не в хейт-листе'
	else:
		return 'Пользователя и так нет в хейт-листе'

async def add_to_photohate(chat_id):
	q.execute(f"SELECT * FROM users WHERE user_id = {chat_id}")
	users = q.fetchall()
	if len(users) == 0:
		q.execute('INSERT INTO USERS (user_id, hatedphoto) VALUES (?,?)', (chat_id, 1))
		connection.commit()
		return 'Пользователь успешно добавлен в хейт-лист'
	else:
		request = q.execute('SELECT hatedphoto FROM users WHERE user_id = ?', (chat_id,)).fetchone()
		if int(request[0]) == 0:
			q.execute('UPDATE users SET hatedphoto = 1 WHERE user_id = ?', (chat_id,))
			connection.commit()
			return 'Пользователь успешно добавлен в хейт-лист'
		else:
			return 'Пользователь уже находится в хейт-листе'

async def delete_from_photohate(chat_id):
	request = q.execute('SELECT hatedphoto FROM users WHERE user_id = ?', (chat_id,)).fetchone()
	if int(request[0]) == 1:
		q.execute('UPDATE users SET hatedphoto = 0 WHERE user_id = ?', (chat_id,))
		connection.commit()
		return 'Пользователь больше не в хейт-листе'
	else:
		return 'Пользователя и так нет в хейт-листе'

async def admin_check(peer_id):
	members = await bot.bot.api.messages.get_conversation_members(
				peer_id=peer_id
		)

	admins = [member.member_id for member in members.items if member.is_admin]
	return admins

async def set_hate(chat_id):
	q.execute(f"SELECT * FROM users WHERE user_id = {chat_id}")
	users = q.fetchall()
	if len(users) == 0:
		q.execute('INSERT INTO USERS (user_id, hated, hatedphoto) VALUES (?,?,?)', (chat_id, 0, 0))
		connection.commit()
	else:
		hated = q.execute('SELECT hated FROM users WHERE user_id = ?', (chat_id,)).fetchone()
		hatedphoto = q.execute('SELECT hatedphoto FROM users WHERE user_id = ?', (chat_id,)).fetchone()
		if hatedphoto[0] is None:
			q.execute('UPDATE users SET hatedphoto = 0 WHERE user_id = ?', (chat_id,))
			connection.commit()
		elif hated[0] is None:
			q.execute('UPDATE users SET hated = 0 WHERE user_id = ?', (chat_id,))
			connection.commit()
		elif hated[0] is None and hatedphoto[0] is None:
			q.execute('UPDATE users SET hatedphoto = 0 WHERE user_id = ?', (chat_id,))
			connection.commit()
			q.execute('UPDATE users SET hated = 0 WHERE user_id = ?', (chat_id,))
			connection.commit()

async def check_texts():
	import os
	texts = []
	if not os.listdir(dir_to_texts):
		for i in err:
			texts.append(i)
		return texts
	else:
		for filename in os.listdir(dir_to_texts):
			with open("{}{}".format(dir_to_texts, filename), 'r') as f:
				for str in f:
					texts.append(str)
		return texts