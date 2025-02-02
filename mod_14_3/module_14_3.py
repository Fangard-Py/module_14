from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await UserState.weight.set()
    data = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий: {data}')
    await state.finish()


@dp.message_handler(text='Рассчитать')
async def main_meny(message):
    await message.answer('Выберите пункт меню:', reply_markup=kbi)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о нашем боте')


@dp.message_handler(text='Купить')
async def handle_buying(message: types.Message):
    await get_buying_list(message)


async def get_buying_list(message: types.Message):
    for i in range(1, 5):
        with open('pictures/bot1.jpeg', 'rb') as img:
            product_info = f'Название: Продукт {i} | Описание: описание {i} | Цена: {i * 100}'
            await message.answer(product_info)
            await message.answer_photo(img, caption=f'Картинка продукта {i}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kbi2)


@dp.callback_query_handler(lambda c: c.data.startswith('product_buying'))
async def process_callback_button(callback_query: types.CallbackQuery):
    product_number = int(callback_query.data.split('_')[2])
    await callback_query.message.answer(f'Вы успешно купили продукт {product_number}!')


@dp.callback_query_handler(text='formulas')
async def main_meny(call):
    await call.message.answer('10 * вес + 6.25 * рост - 5 * возраст + 5')


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, который помогает поддерживать здоровье.', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button, button2, button3)

kbi = InlineKeyboardMarkup(resize_keyboard=True)
buttonI = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
buttonII = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
kbi.add(buttonI, buttonII)

kbi2 = InlineKeyboardMarkup(resize_keyboard=True)
for i in range(1, 5):
    kbi2.insert(
        InlineKeyboardButton(text=f'Продукт {i}', callback_data=f'product_buying_{i}')
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
