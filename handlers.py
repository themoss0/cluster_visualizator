import tempfile
import os
from aiogram import types, Dispatcher
from aiogram.types import BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from cluster_manager import process_file
from plot_generator import generate_overview_plot, generate_cluster_zoom

# Хранилище данных пользователей (в памяти)
_user_data = {}

async def cmd_start(message: types.Message):
    await message.answer(
        "💬 Пришлите текстовый файл с координатами точек (x y) или (x y планета).\n"
        "📂 Файл должен быть в кодировке UTF-8, числа с точкой или запятой."
    )

async def handle_document(message: types.Message):
    document = message.document
    if not document.file_name.endswith('.txt'):
        await message.answer("❌ Пожалуйста, отправьте файл в формате .txt")
        return

    tmp_path = None
    try:
        # Скачиваем файл
        file = await message.bot.get_file(document.file_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            await message.bot.download_file(file.file_path, tmp.name)
            tmp_path = tmp.name

        await message.answer("Обработка файла... Это может занять некоторое время.")
        points, labels, stats_list, has_planets = process_file(tmp_path, eps=1.4)

        # Сохраняем данные
        user_id = message.from_user.id
        _user_data[user_id] = {
            'points': points,
            'labels': labels,
            'stats_list': stats_list,
            'has_planets': has_planets
        }

        # Общий график
        overview_img = generate_overview_plot(points, labels, has_planets, stats_list)
        await message.answer_photo(
            photo=BufferedInputFile(overview_img.getvalue(), filename='overview.png'),
            caption=f"Найдено кластеров: {len(stats_list)}, всего точек: {len(points)}"
        )

        # Клавиатура выбора кластера
        keyboard = []
        for stat in stats_list:
            cid = stat['cluster_id']
            size = stat['size']
            keyboard.append([InlineKeyboardButton(text=f"Кластер {cid} ({size} точек)", callback_data=f"zoom:{cid}")])

        if stats_list:
            min_diam = min(stat['diameter'] for stat in stats_list)
            compact_cluster = next(stat for stat in stats_list if stat['diameter'] == min_diam)['cluster_id']
            keyboard.append([InlineKeyboardButton(text=f"🔍 Самый компактный (кластер {compact_cluster})", callback_data=f"zoom:{compact_cluster}")])

        # keyboard.append([InlineKeyboardButton(text="🔄 Общий вид", callback_data="overview")])
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer("Выберите кластер для приближения:", reply_markup=reply_markup)

    except Exception as e:
        import traceback
        await message.answer(f"❌ Ошибка: {e}\n{traceback.format_exc()}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

async def button_callback(callback: types.CallbackQuery):
    await callback.answer()
    data = callback.data
    user_id = callback.from_user.id
    user_data = _user_data.get(user_id)
    if not user_data:
        await callback.message.answer("Данные не найдены. Отправьте файл заново.")
        return

    points = user_data['points']
    labels = user_data['labels']
    stats_list = user_data['stats_list']
    has_planets = user_data['has_planets']

    # Общий вид (отправляем новое фото)
    if data == "overview":
        img = generate_overview_plot(points, labels, has_planets, stats_list)
        await callback.message.answer_photo(
            photo=BufferedInputFile(img.getvalue(), filename='overview.png'),
            caption="Общий вид кластеров"
        )
        # Можно отправить клавиатуру заново (опционально)
        keyboard = []
        for stat in stats_list:
            cid = stat['cluster_id']
            size = stat['size']
            keyboard.append([InlineKeyboardButton(text=f"Кластер {cid} ({size} точек)", callback_data=f"zoom:{cid}")])
        if stats_list:
            min_diam = min(stat['diameter'] for stat in stats_list)
            compact_cluster = next(stat for stat in stats_list if stat['diameter'] == min_diam)['cluster_id']
            keyboard.append([InlineKeyboardButton(text=f"🔍 Самый компактный (кластер {compact_cluster})", callback_data=f"zoom:{compact_cluster}")])
        # keyboard.append([InlineKeyboardButton(text="🔄 Общий вид", callback_data="overview")])
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await callback.message.answer("Выберите кластер для приближения:", reply_markup=reply_markup)
        return

    # Возврат к списку кластеров (просто удаляем сообщение с увеличенным кластером)
    if data == "back_to_list":
        await callback.message.delete()
        return

    # Приближение к кластеру
    if data.startswith("zoom:"):
        try:
            cluster_id = int(data.split(":")[1])
        except:
            await callback.answer("Неверный формат")
            return
        stat = next((s for s in stats_list if s['cluster_id'] == cluster_id), None)
        if stat is None:
            await callback.answer("Кластер не найден")
            return
        img = generate_cluster_zoom(points, labels, cluster_id, has_planets, stat)
        if img:
            # Получаем центроиды (они у вас списки [x, y])
            cent_min = stat['centroid_min_dist_sum']
            cent_am = stat['centroid_arithmetic_mean']
            anti = stat['anticentroid_max_dist_sum']

            caption = (f"Кластер {cluster_id}\n"
           f"Точек: {stat['size']}\n"
           f"Центроид (мин. сумма): ({cent_min[0]:.2f}, {cent_min[1]:.2f})\n"
           f"Центроид (ср.ар.): ({cent_am[0]:.2f}, {cent_am[1]:.2f})\n"
           f"Антицентроид (макс. сумма): ({anti[0]:.2f}, {anti[1]:.2f})")
            if has_planets:
                unique_planets = set(stat['extras'])
                caption += f"\nПланеты: {', '.join(sorted(unique_planets)[:5])}"
                if len(unique_planets) > 5:
                    caption += f" и ещё {len(unique_planets)-5}"
            back_button = InlineKeyboardButton(text="◀ Назад к списку кластеров", callback_data="back_to_list")
            markup = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
            await callback.message.answer_photo(
                photo=BufferedInputFile(img.getvalue(), filename=f'cluster_{cluster_id}.png'),
                caption=caption,
                reply_markup=markup
            )
        else:
            await callback.answer("🖼️ Не удалось сгенерировать изображение")
        return

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(handle_document, lambda message: message.document is not None)
    dp.callback_query.register(button_callback)