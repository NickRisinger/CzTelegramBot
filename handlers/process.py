import os
from io import BytesIO
from aiogram import Bot, Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from pylibdmtx.pylibdmtx import decode
from PIL import Image

from keyboards.support import support_start_keyboard
from middlewares.support import SupportMiddleware
from services.fair_sign import APIService
from utils.scan import parse_chzn_code
from utils.utils import gtins
from database.database import add_code, get_code

router = Router()
router.message.middleware(SupportMiddleware())
cz_api = APIService()

example_path = './data/datamatrix.jpg'
example_check_path = './data/check.jpg'


class ProcessState(StatesGroup):
    scanning = State()


async def error_message(message: Message):
    await message.answer('Система не может провести ваш код, убедитесь что вы совершили покупку!')
    album_builder = MediaGroupBuilder(
        caption='Примеры фото',
    )
    album_builder.add(
        type='photo',
        media=FSInputFile(example_check_path)
    )
    album_builder.add(
        type='photo',
        media=FSInputFile(example_path)
    )
    await message.answer_media_group(
        media=album_builder.build(),
    )
    await message.answer(
        'Если покупка была совершена, а код все равно не регистрируется, нажмите кнопку написать в тех поддержку и загрузите фото чека о покупке и кода с бутылки.',
        reply_markup=support_start_keyboard())


@router.message(F.text == 'Сканировать код')
async def code(message: Message, state: FSMContext):
    if os.path.exists(example_path):
        await message.answer_photo(
            photo=FSInputFile(
                path=example_path
            ),
            caption='Загрузите фотографию с кодом, учтите что код должен занимать более 30% фотографии.'
        )
    else:
        await message.answer('Загрузите фотографию с кодом, учтите что код должен занимать более 30% фотографии.')

    await state.set_state(ProcessState.scanning)


@router.message(F.photo, ProcessState.scanning)
async def process_photo(message: Message, bot: Bot):
    await message.answer('Получил фото , пытаюсь распознать код...')

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path

    # Скачиваем как байты
    file_bytes = await bot.download_file(file_path)
    image = Image.open(BytesIO(file_bytes.read()))
    decoded = decode(image)

    if not decoded:
        await error_message(message)
        return

    raw_data = decoded[0].data.decode('utf-8')
    parsed = parse_chzn_code(raw_data)

    code_exist = await get_code(parsed['CLEAN'])

    if code_exist:
        await error_message(message)
        return

    # Проверка GTIN на участие в акции
    if not parsed['GTIN'] in gtins:
        await message.answer('Данный товар не участвует в акции!')
        return

    try:
        cz_data = await cz_api.get_data(parsed['CLEAN'])

        if cz_data[0]['cisInfo']['status'] == 'RETIRED':
            # начисляем поинты
            await add_code(message.from_user.id, parsed['CLEAN'])
            await message.answer('Данный код успешно зарегистрирован, вам начислен один балл')
        else:
            await error_message(message)

    except Exception as e:
        print(e)
        await message.answer(
            f"Ошибка соединения с сервером, повторите попытку позже\n"
            f"В случае повторной ошибки напишите администратору: @igoree1s\n"
        )
