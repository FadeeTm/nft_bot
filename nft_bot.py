from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import Helper, HelperMode, ListItem

from config import BOT_TOKEN

GREETINGS = ('Здравствуй, пользователь {user} !\n'
             ' Основные команды:\n'
             ' "/команда 1" - команда передачи NFT токена\n'
             ' "/команда 2" - команда продажи NFT токена\n'
             ' "/команда 3" - команда покупки NFT токена'
            )

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class States(Helper):
    mode = HelperMode.snake_case

    STATE_0 = ListItem()
    STATE_1 = ListItem()
    STATE_2 = ListItem()
    STATE_3 = ListItem()


@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    '''Метод вызова сообщения командой /start.'''
    username = message.from_user.first_name
    await message.reply(GREETINGS.format(user = username))

@dp.message_handler(state='*', commands = ['команда'])
async def start_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if (not argument):
        await state.reset_state()
    elif int(argument) == 1:
        await state.set_state(States.all()[int(argument)])
        await message.reply('Введите адрес получателя:', reply=False)
    elif int(argument) == 2:
        await state.set_state(States.all()[int(argument)])
        await message.reply('Отправьте NFT токен:', reply=False)
    elif int(argument) == 3:
        await state.set_state(States.all()[int(argument)])
        await message.reply('Выберите NFT токен:', reply=False)

@dp.message_handler(state=States.STATE_1)
async def dispatch_step1(message: types.Message):
    await message.reply('Введите id NFT токена:', reply=False)

@dp.message_handler(state=States.STATE_2)
async def first_test_state_case_met(message: types.Message):
    await message.reply('Выберите NFT токен:', reply=False)

@dp.message_handler(state=States.STATE_3)
async def first_test_state_case_met(message: types.Message):
    await message.reply('NFT токен выбран !', reply=False)

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
