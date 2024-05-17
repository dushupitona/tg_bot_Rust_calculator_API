from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from filters import NumberFilter
from api import get_valid_objects, get_valid_tools, calculate


router = Router()

try:
    valid_objects = [obj['obj_name'] for obj in get_valid_objects()]
    valid_tools = [obj['tool_name'] for obj in get_valid_tools()]
except:
    valid_objects = []
    valid_tools = []


class CalcValues(StatesGroup):
    choosing_object = State()
    choosing_tool = State()
    choosing_quan = State()


# --------------OBJECTS---------------------------------

@router.message(Command("start"))
async def choose_object(message: Message, state: FSMContext):
        if valid_objects:
            builder = ReplyKeyboardBuilder()
            for _ in valid_objects:
                builder.add(KeyboardButton(text=_))
            builder.adjust(2)

            await message.answer(
                text='What will you raid?',
                reply_markup=builder.as_markup()
            )
            await state.set_state(CalcValues.choosing_object)


@router.message(CalcValues.choosing_object, F.text.in_(valid_objects))
async def object_chosen(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='/tool'))

    await state.update_data(chosen_object=message.text.lower())
    await message.answer(
        text='What will you raid with (/tool):',
        reply_markup=builder.as_markup()
    )
    await state.set_state(CalcValues.choosing_tool)


@router.message(CalcValues.choosing_object)
async def object_chosen_incorrectly(message: Message):
    await message.answer(
        text='Incorrect value',
    )


# --------------TOOLS---------------------------------

@router.message(Command("tool"))
async def choose_tool(message: Message, state: FSMContext):
    state_dict = await state.get_data()
    if state_dict:
        builder = ReplyKeyboardBuilder()
        for _ in valid_tools:
            builder.add(KeyboardButton(text=_))
        builder.adjust(2)
        await message.answer(
            text='Select:',
            reply_markup = builder.as_markup()
        )
        await state.set_state(CalcValues.choosing_tool)


@router.message(CalcValues.choosing_tool, F.text.in_(valid_tools))
async def tool_chosen(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='/quantity'))

    await state.update_data(chosen_tool=message.text.lower())
    await message.answer(
        text='Number of objects (/quantity):',
        reply_markup = builder.as_markup()
    )
    await state.set_state(CalcValues.choosing_quan)


@router.message(CalcValues.choosing_tool)
async def tool_chosen_incorrectly(message: Message):
    await message.answer(
        text='Incorrect value',
    )


# --------------QUANTITY-----------------------------------

@router.message(Command("quantity"))
async def choose_quan(message: Message, state: FSMContext):
    state_dict = await state.get_data()
    if state_dict.get('chosen_object') and state_dict.get('chosen_tool'):
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text='1'))
        await message.answer(
            text = 'Choose or set it yourself from 1 to 50:',
            reply_markup=builder.as_markup()
        )
        await state.set_state(CalcValues.choosing_quan)


@router.message(CalcValues.choosing_quan, NumberFilter(1, 50))
async def quan_chosen(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='/start'))

    await state.update_data(chosen_quan=message.text.lower())
    user_data = await state.get_data()
    responce = calculate(data=user_data)
    if responce:
        await message.answer(
            text=f'You will need:\n',
            reply_markup=builder.as_markup()
        )
        await message.answer(
            text=f'{responce['tool']}: {responce['quantity']}',
            reply_markup=builder.as_markup()
        )
        await message.answer(
            text=f'Resources:\n',
            reply_markup=builder.as_markup()
        )
        for res in responce['resources']:
            await message.answer(
                text=f'{res['name']}: {res['values']}\n',
                reply_markup=builder.as_markup()
            )
    else:
        await message.answer(
        text='Im not working yet',
    )

    await state.clear()


@router.message(CalcValues.choosing_quan)
async def quan_chosen_incorrectly(message: Message):
    await message.answer(
        text='Incorrect value',
    )






