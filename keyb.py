import bot
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, VKApps
from config import group_id

async def jointogroup(from_id):
	keyboard = Keyboard(inline=True)
	keyboard.add(VKApps(app_id=6441755, owner_id=-group_id, label='Добавить в беседу'))
	check = await bot.bot.api.request("groups.isMember", {"group_id": group_id, "user_id": from_id, "extended": "0"})
	if check['response'] != 1:
		keyboard.add(OpenLink(link='https://vk.com/club{}'.format(group_id), label='Подписаться'))
	return keyboard

addtochat = Keyboard(inline=True)
addtochat.add(VKApps(app_id=6441755, owner_id=-group_id, label='Добавить в беседу'))
