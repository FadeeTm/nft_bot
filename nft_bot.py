from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

GREETINGS = ('Здравствуй, пользователь {name} !\n'
             ' Основные команды:\n'
             ' /команда'
            )

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

all_commands = ['передать', 'продать', 'купить']

class ChooseCommand(StatesGroup):
    main_command = State()
    token_nft = State()
    to_user = State()
    price = State()

@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    '''Метод вызова сообщения командой /start.'''
    username = message.from_user.first_name
    await message.reply(GREETINGS.format(name = username))

async def choose_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for command in all_commands:
        keyboard.add(command)
    await message.reply('Что вы хотите сделать?', reply_markup=keyboard, reply=False)
    await ChooseCommand.main_command.set()

async def activity(message: types.Message, state: FSMContext):
    if message.text.lower() not in all_commands:
        await message.answer('Такой команды, нет. Выберите существующую')
        return
    await state.update_data(action=message.text.lower())
    get_command = await state.get_data()
    if get_command['action'] == 'купить':
        await state.finish()
        await ChooseCommand.token_nft.set()
        await message.reply(f'Введите id токена', reply=False, reply_markup=types.ReplyKeyboardRemove())

    elif get_command['action'] == 'передать':
        await state.finish()
        await ChooseCommand.to_user.set()
        await message.reply('Введите кошелек пользовтеля, кому вы хотите перевести:',
                            reply_markup=types.ReplyKeyboardRemove(),
                            reply=False)
    elif get_command['action'] == 'продать':
        await state.finish()
        await ChooseCommand.price.set()
        await message.reply('Введите цену, за которую хотите продать NFT-токен:',
                            reply_markup=types.ReplyKeyboardRemove(),
                            reply=False)

async def token_choose(message: types.Message, state: FSMContext):
    await state.update_data(token_nft=message.text)
    get_token = await state.get_data()
    await message.reply('Введен токен: {token}'.format(token = get_token['token_nft']))

async def to_user(message: types.Message, state: FSMContext):
    await state.update_data(person=message.text)
    get_user = await state.get_data()
    await message.reply(('Введен кошелек пользователя: {set_person}').format(set_person = get_user['person']))

async def set_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    get_price = await state.get_data()
    await message.reply(('Введена цена: {price}').format(price = get_price['price']))

async def close(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')

def handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(close, commands='выйти', state='*')
    dispatcher.register_message_handler(choose_command, commands='команда', state='*')
    dispatcher.register_message_handler(activity, state=ChooseCommand.main_command)
    dispatcher.register_message_handler(token_choose, state=ChooseCommand.token_nft)
    dispatcher.register_message_handler(to_user, state=ChooseCommand.to_user)
    dispatcher.register_message_handler(set_price, state=ChooseCommand.price)

if __name__ == '__main__':
    handlers(dp)
    executor.start_polling(dp, skip_updates=True)
