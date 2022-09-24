# User levels (in chat too)

from header import userDB, bot
from server.user.user_utils.achievements.achievements import Achievements
from server.user.user_utils.achievements.medals import Medals
from server.user.user_utils.premium import PremiumMenu


ZETA = 'Кабаняшка'
EPSILON = 'Кабан-падаван'
DELTA = 'Кабанчик'
GAMMA = 'Вепрь'
BETA = 'Убер-кабан'
ALPHA = 'Премиальный'


def user_set_status(message):
    pass


def user_give_status(message):
    pass


def user_get_status(message):
    user_id = message.from_user.id
    level = userDB.get_level(user_id)
    boars = Achievements(user_id).opened_boars
    medals = Medals(user_id).medals
    premium_status = PremiumMenu(user_id).status

    tab = '   '
    user_medals = 'Медали: /n' + str(map(lambda medal: tab + medal + '/n', medals))

    text = (f'<b>{level}</b> /n' +
            f'Всего открыто {boars} кабанов /n' +
            user_medals +
            f'Премиум: {premium_status} /n'
    )

    bot.send_message(message.chat.id, text, 'html')