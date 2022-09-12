import os, math
from server.utils.keyboard import build_buttons
from server.utils.keyboard import InlineKeyboard
from config import PATH
from telebot import types


navi = {
    0: {'text': '|<',  'call': '|<'  },
    1: {'text': '<',   'call': '<'   },
    2: {'text': '1/2', 'call': 'none'},
    3: {'text': '>',   'call': '>'   },
    4: {'text': '>|',  'call': '>|'  }
}


max_size = 7

def get_charts_keyboard(offset: int, path: str, call: str, back: str) -> InlineKeyboard:
    all = os.listdir(PATH.DB_STATS+path) # все файлы
    try:
        year = path.split('/')[0]
    except:
        year = '/'
    try:
        month = path.split('/')[1]
        if not month:
            month = '/'
    except:
        month = '/'
    all.sort()
    files = all[offset:]
    count = len(all)
    pages = math.ceil(count / max_size) # сколько страниц
    start = math.ceil((offset + 1) / max_size)
    counter = f'{start}/{pages}'
    items = files
    buttons = []
    for i in range(len(items)): # вывести только 7 кнопок
        if i < max_size:
            button = types.InlineKeyboardButton(text=items[i], callback_data=call+' '+items[i]+' '+year+' '+month)
            buttons.append(button)
        else:
            offset = i + offset # с чего начинать в следующий раз
            break
    keyboard = InlineKeyboard()
    keyboard.add(*buttons, row_width=1)
    b_call = _choose_call(call)
    navi[1]['call'] = f'< {offset - max_size - i} {year} {month} {b_call}'
    navi[2]['text'] = f'{counter}'
    navi[3]['call'] = f'> {offset} {year} {month} {b_call}'
    if count % max_size == 0:
        floor = count - max_size
    else:
        floor = (count//max_size)*max_size
    navi[4]['call'] = f'>| {floor}'
    navi_buttons = build_buttons(navi)
    keyboard.add(*navi_buttons, row_width=5)
    keyboard.add_button('Назад', back)
    return keyboard


def _choose_call(call):
    if 'CHARTS_YEAR' in call:
        return 'CHARTS_YEAR'
    elif 'CHARTS_MONTH' in call:
        return 'CHARTS_MONTH'
    elif 'CHART_DAY_SEE' in call:
        return 'CHART_DAY_SEE'

def translate_b_call(call):
    if 'CHARTS_YEAR' in call:
        return 'годы'
    elif 'CHARTS_MONTH' in call:
        return 'месяцы'
    elif 'CHART_DAY_SEE' in call:
        return 'графики'

def reverse_b_call(call):
    if 'CHARTS_MONTH' in call:
        return 'SEE_CHARTS_DAY'
    elif 'CHART_DAY_SEE' in call:
        return 'CHARTS_YEAR'



def get_years_keyboard(offset: int) -> InlineKeyboard:
    all = os.listdir(PATH.DB_STATS) # все файлы
    all.sort()
    files = all[offset:]
    count = len(all)
    pages = math.ceil(count / max_size) # сколько страниц
    start = math.ceil((offset + 1) / max_size)
    counter = f'{start}/{pages}'
    items = [x[:-3] for x in files] # вывести только названия файлов
    buttons = []
    for i in range(len(items)): # вывести только 7 кнопок
        if i < max_size:
            button = types.InlineKeyboardButton(text=items[i], callback_data='CHARTS_YEAR'+' '+items[i])
            buttons.append(button)
        else:
            offset = i + offset # с чего начинать в следующий раз
            break
    keyboard = InlineKeyboard()
    keyboard.add(*buttons, row_width=1)
    navi[1]['call'] = f'< {offset - max_size - i}'
    navi[2]['text'] = f'{counter}'
    navi[3]['call'] = f'> {offset}'
    if count % max_size == 0:
        floor = count - max_size
    else:
        floor = (count//max_size)*max_size
    navi[4]['call'] = f'>| {floor}'
    navi_buttons = build_buttons(navi)
    keyboard.add(*navi_buttons, row_width=5)
    keyboard.add_button('Назад', 'BACK_FROM_CHARTS')
    return keyboard
