from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

GREETINGS = ('Nice to see you, {name}')

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

all_commands = ['/sell', '/buy']
all_tokens = ['token1', 'token2']

class ChooseCommand(StatesGroup):
    private_key = State()
    token = State()
    user_token = State()
    yes = State()
    no = State()

@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    username = message.from_user.first_name
    await message.reply(GREETINGS.format(name = username))
    await message.reply('Authorization ! Accept your readiness /auth !', reply=False)

@dp.message_handler(commands = ['auth'])
async def authorisation_pk(message: types.Message):
    await message.reply('Type your private key', reply=False)
    await ChooseCommand.private_key.set()

async def authorisation_accepted(message: types.Message, state: FSMContext):
    await state.update_data(private_key=message.text)
    await message.reply('Done ! Type /list to choose your token !', reply=False)
    await state.finish()

@dp.message_handler(commands = ['list'])
async def tokens_all(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for token in all_tokens:
        keyboard.add(token)
    await message.reply(f'Choose your token !', reply_markup=keyboard, reply=False)
    await ChooseCommand.token.set()

async def token_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in all_tokens:
            await message.answer('Invalid token !')
            return
    await state.update_data(token=message.text)
    get_token = await state.get_data()
    await message.reply(('Your token: {data} !').format(data=get_token['token']), reply=False, reply_markup=types.ReplyKeyboardRemove())
    await message.reply('Type /send to choose user address!', reply=False)
    await state.finish()

@dp.message_handler(commands = ['send'])
async def token_user(message: types.Message):
    await message.reply('Type user`s address !', reply=False)
    await ChooseCommand.user_token.set()

async def user_accepted(message: types.Message, state: FSMContext):
    await state.update_data(user_token=message.text)
    get_user_data = await state.get_data()
    await message.reply(('Done ! User address: {boy}. Do you want to send your token /yes or /no ?').format(boy=get_user_data['user_token']), reply=False)
    await state.finish()

@dp.message_handler(commands = ['yes'])
async def acception(message: types.Message):
    await message.reply('Ok', reply=False)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for command in all_commands:
        keyboard.add(command)
    await message.reply('Choose command /sell or /buy !', reply_markup=keyboard, reply=False)

@dp.message_handler(commands = ['sell'])
async def sell(message: types.Message):
    await message.reply('Ok', reply=False, reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands = ['buy'])
async def buy(message: types.Message):
    await message.reply('Ok', reply=False, reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands = ['no'])
async def acception(message: types.Message, state: FSMContext):
    await message.reply('Ok. Type /cancel to exit', reply=False)

async def close(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')

def handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(authorisation_accepted, state=ChooseCommand.private_key)
    dispatcher.register_message_handler(token_chosen, state=ChooseCommand.token)
    dispatcher.register_message_handler(user_accepted, state=ChooseCommand.user_token)
    dispatcher.register_message_handler(close, commands='cancel', state='*')

if __name__ == '__main__':
    handlers(dp)
    executor.start_polling(dp, skip_updates=True)
