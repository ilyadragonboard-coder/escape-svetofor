"""Локации квеста: одна функция на локацию.

Каждая локация:
  1) рисует сцену и меню,
  2) считывает выбор игрока,
  3) передаёт управление другой локации (или завершает игру).

Переходы делают функции локаций взаимно рекурсивными:
canned -> toys -> dairy -> toys -> ... — это косвенная рекурсия.

Все переходы выполняются через `return some_location()`,
чтобы после завершения игры (`state.game_over == True`) стек
разматывался чисто, без «висящих» кадров и лишних действий.

Звуки (модуль sounds) играются в фоне — они не блокируют сюжет.
"""
import random

from . import state, art, sounds
from .utils import prompt, pause, clear


# ============================================================
#                       ВСПОМОГАТЕЛЬНОЕ
# ============================================================

def _room(key, title, description):
    """Отрисовка локации: ASCII-арт, заголовок, описание, статус."""
    clear()
    print(art.ROOMS.get(key, ''))
    print(f'─── {title} ───')
    print(description)
    sounds.ambient_shop()          # мрачный гул при входе
    pause(0.6)
    print()
    print('  Инвентарь:', ', '.join(state.inventory) or 'пусто')
    pause(0.4)


def _die(message):
    """Смерть игрока — завершает партию поражением."""
    print(message)
    sounds.death()                 # нисходящий тон
    pause(0.9)
    print(art.GAMEOVER)
    state.finish(win=False)


def _note(note_id, text):
    """Показать записку, если она ещё не читалась."""
    if state.read_note(note_id):
        sounds.note_found()        # тихий «дзинь»
        print()
        print('  Вы нашли записку:')
        for line in text.splitlines():
            print(f'    {line}')
        pause(1.4)


def _go(next_location):
    """Переход: короткий звук шага + вызов следующей локации."""
    sounds.step()
    return next_location()


# ============================================================
#                          ЛОКАЦИИ
# ============================================================

def canned():
    """Консервный отдел — стартовая локация."""
    if state.game_over:
        return
    _room('canned', 'Консервный отдел',
          'Полки забиты банками с надписью «МЯСО». '
          'Пахнет железом и чем-то живым.')

    c = prompt([
        'Съесть банку консервов',
        'Идти в отдел игрушек',
        'Идти на кассу',
        'Идти в туалет',
    ])
    if c == 1:
        return _eat_can()
    if c == 2:
        return _go(toys)
    if c == 3:
        return _go(cashier)
    if c == 4:
        return _go(toilet)


def _eat_can():
    """Съесть банку — высокий шанс смерти."""
    sounds.eat_can()               # чавканье
    print('Вы открыли банку и съели содержимое...')
    pause(1.0)
    if random.random() < 0.8:
        return _die('Вы умерли от хантавируса. Банки были не зря закрыты.')
    print('Вам повезло. Вы живы.')
    pause(0.5)
    return _go(toys)


def toys():
    """Отдел игрушек — встреча с Татата Сауром."""
    if state.game_over:
        return
    _room('toys', 'Отдел игрушек',
          'На полке сидят три плюшевые фигуры. Одна из них — '
          'Татата Саур. Он уже заметил вас.')

    _note('toy_note',
          'Дневник Черемши, запись №7:\n'
          'Саур снова не спал ночью. Он смотрит на банки так,\n'
          'будто они ему что-то говорят. Я боюсь его.')

    c = prompt([
        'Сбежать в кисломолочный отдел',
        'Попытаться отбиться',
        'Спрятаться в плюшевых игрушках',
        'Вернуться в консервный отдел',
    ])
    if c == 1:
        return _go(dairy)
    if c == 2:
        return _fight()
    if c == 3:
        return _hide_toys()
    if c == 4:
        return _go(canned)


def _fight():
    """Бой с Сауром. Пистолет повышает шансы, но не гарантирует."""
    print('Вы пытаетесь отбиться от Татата Саура...')
    sounds.fight_hit()             # резкие удары
    pause(0.8)
    if state.has('pistol'):
        print('Вы стреляете из пистолета!')
        sounds.fight_hit()
        pause(0.6)
        if random.random() < 0.7:
            return _die('Саур ранен, но в последнем рывке он достал вас.')
        print('Вы отбились!')
        return _go(dairy)
    if random.random() < 0.9:
        return _die('Саур забил вас до смерти. Он не любит гостей.')
    print('Каким-то чудом вы отбились!')
    return _go(dairy)


def _hide_toys():
    """Спрятаться среди игрушек — рискованно."""
    print('Вы прячетесь среди плюшевых игрушек...')
    sounds.step()
    pause(0.9)
    if random.random() < 0.7:
        return _die('Черемша и Лабубу съели вас заживо.')
    print('Вам удалось спрятаться.')
    pause(0.5)
    return toys()


def dairy():
    """Кисломолочный отдел."""
    if state.game_over:
        return
    _room('dairy', 'Кисломолочный отдел',
          'На полке — йогурты «Тёма» и «Чудо». Даты просрочки '
          'выглядят... неправильно.')

    c = prompt([
        'Выпить Тёму',
        'Выпить Чудо',
        'Пойти в подсобку',
        'Вернуться в отдел игрушек',
    ])
    if c == 1:
        return _drink_tema()
    if c == 2:
        return _drink_chudo()
    if c == 3:
        return _go(staff)
    if c == 4:
        return _go(toys)


def _drink_tema():
    """Просроченный йогурт — почти верная смерть."""
    print('Вы пьёте Тёму...')
    sounds.hurt()
    pause(0.8)
    if random.random() < 0.9:
        return _die('Он был просрочен 67 лет назад. Вы умерли.')
    print('Чудесным образом вы выжили.')
    return dairy()


def _drink_chudo():
    """«Чудо» — маленький шанс на «шутливую» победу."""
    print('Вы пьёте Чудо...')
    sounds.step()
    pause(1.2)
    if random.random() < 0.25:
        sounds.chudo_magic()
        print('Произошло чудо! Вы проснулись в своей кровати. Это был сон.')
        pause(0.6)
        print(art.WIN)
        sounds.win()
        state.finish(win=True)
        return
    print('Чуда не случилось, но стало легче.')
    pause(0.5)
    return dairy()


def staff():
    """Подсобка персонала — здесь лежит ключ."""
    if state.game_over:
        return
    _room('staff', 'Подсобка персонала',
          'Пыльно, темно, пахнет картоном и старой рыбой.')

    _note('staff_note',
          'Приказ №404:\n'
          'Всем сотрудникам — не кормите Татата Саура после полуночи.\n'
          'Он становится... другим.')

    c = prompt([
        'Поискать что-нибудь',
        'Пойти в молочный отдел',
        'Пойти на склад',
    ])
    if c == 1:
        return _search_staff()
    if c == 2:
        return _go(dairy)
    if c == 3:
        return _go(warehouse)


def _search_staff():
    """Найти ключ от выхода (одноразово)."""
    if 'key' not in state.taken_items:
        state.add('key')
        sounds.item_found()
        print('Под коробкой вы нашли ключ от выхода!')
    else:
        print('Здесь больше ничего нет.')
    pause(0.6)
    return staff()


def cashier():
    """Касса и кассирша."""
    if state.game_over:
        return
    _room('cashier', 'Касса',
          'За кассой стоит женщина с очень уставшим лицом. '
          'Она смотрит прямо на вас.')

    c = prompt([
        'Поговорить с кассиршей',
        'Нагрубить кассирше',
        'Пойти в отдел игрушек',
        'Идти в туалет',
    ])
    if c == 1:
        return _talk_cashier()
    if c == 2:
        return _rude_cashier()
    if c == 3:
        return _go(toys)
    if c == 4:
        return _go(toilet)


def _talk_cashier():
    """Диалог с кассиршей: либо победа (с деньгами), либо продолжение."""
    print('Кассирша: «Дверь откроется, если найдёшь потерянную наличку».')
    sounds.step()
    pause(0.8)
    if state.has('money'):
        print('Вы отдаёте деньги. Кассирша молча открывает дверь.')
        pause(0.7)
        print(art.WIN)
        sounds.win()
        state.finish(win=True)
        return
    print('Она ждёт деньги. И, кажется, у неё мало терпения.')
    pause(0.6)
    return cashier()


def _rude_cashier():
    """Нагрубить кассирше — почти всегда смерть."""
    print('Вы грубите кассирше...')
    sounds.fight_hit()
    pause(0.7)
    if random.random() < 0.8:
        return _die('Под прилавком у неё был пистолет. Она выстрелила.')
    print('Кассирша удивлена и отступает.')
    pause(0.5)
    return cashier()


def toilet():
    """Туалет — темно и страшно."""
    if state.game_over:
        return
    _room('toilet', 'Туалет',
          'Три кабинки. Свет мигает. Из третьей доносится '
          'странный звук, похожий на дыхание.')

    _note('toilet_note',
          'Нацарапано на стене:\n'
          'Я сижу здесь три дня. ОНО не уходит.\n'
          'В кабинке №3 не прячься. Никогда.')

    c = prompt([
        'Поискать что-нибудь',
        'Вернуться в консервный отдел',
        'Спрятаться в кабинке',
    ])
    if c == 1:
        return _search_toilet()
    if c == 2:
        return _go(canned)
    if c == 3:
        return _hide_toilet()


def _search_toilet():
    """Найти фонарик (одноразово)."""
    if 'flashlight' not in state.taken_items:
        state.add('flashlight')
        sounds.item_found()
        print('Под раковиной вы нашли фонарик!')
    else:
        print('В туалете больше ничего нет.')
    pause(0.6)
    return toilet()


def _hide_toilet():
    """Спрятаться в кабинке — высокий риск."""
    print('Вы спрятались в кабинке...')
    sounds.step()
    pause(0.8)
    if random.random() < 0.8:
        return _die('Из унитаза к вам потянулось что-то живое.')
    print('Вы быстро выбежали.')
    return toilet()


def warehouse():
    """Склад — коробки и наличка."""
    if state.game_over:
        return
    _room('warehouse', 'Склад',
          'Бесконечные ряды коробок. Пахнет пылью и плесенью.')

    _note('warehouse_note',
          'Записка завхоза:\n'
          '«Наличку потерял. Ключ в подсобке, под коробкой.\n'
          'Кассирше не говорите — она убьёт».')

    c = prompt([
        'Поискать что-нибудь',
        'Пойти в комнату охраны',
        'Вернуться в подсобку',
    ])
    if c == 1:
        return _search_warehouse()
    if c == 2:
        return _go(security)
    if c == 3:
        return _go(staff)


def _search_warehouse():
    """Найти деньги, потом аптечку (одноразово)."""
    if 'money' not in state.taken_items:
        state.add('money')
        sounds.item_found()
        print('В мешке с мукой вы нашли потерянную наличку!')
    elif 'medkit' not in state.taken_items:
        state.add('medkit')
        sounds.item_found()
        print('На полке лежала аптечка. Наверное, бесполезная...')
    else:
        print('На складе больше ничего полезного.')
    pause(0.6)
    return warehouse()


def security():
    """Комната охраны — шкаф с возможным пистолетом."""
    if state.game_over:
        return
    _room('security', 'Комната охраны',
          'Мониторы показывают пустые залы. В углу — железный шкаф.')

    _note('security_note',
          'Отчёт охраны:\n'
          '«Камеры в отделе игрушек выключились сами в 3:33.\n'
          'Проверяющий пошёл туда — и не вернулся. Мы слышали смех».')

    c = prompt([
        'Попытаться открыть шкаф',
        'Пойти на склад',
        'Пойти к выходу',
    ])
    if c == 1:
        return _open_locker()
    if c == 2:
        return _go(warehouse)
    if c == 3:
        return _go(exit_room)


def _open_locker():
    """Открыть шкаф. Нужен ключ, может быть пистолет, может быть смерть."""
    print('Шкаф заперт.')
    sounds.error()
    pause(0.5)
    if not state.has('key'):
        print('Нужен ключ.')
        pause(0.5)
        return security()

    print('Вы открываете шкаф ключом...')
    sounds.step()
    pause(0.8)
    state.take('key')

    if 'pistol' in state.taken_items:
        print('Шкаф пуст — вы уже забрали всё.')
    elif random.random() < 0.6:
        sounds.item_found()
        print('Внутри пистолет! Вы забираете его.')
        state.add('pistol')
    else:
        sounds.alarm()
        return _die('Шкаф пуст. Сработала сигнализация, вас окружили.')
    pause(0.6)
    return security()


def exit_room():
    """Выход — финальная точка квеста."""
    if state.game_over:
        return
    _room('exit', 'Выход',
          'Большая дверь на улицу. Заперта. Сквозь щель видно '
          'ночное небо — оно зелёного цвета.')

    c = prompt([
        'Попытаться открыть дверь',
        'Вернуться в магазин',
    ])
    if c == 1:
        return _try_exit()
    if c == 2:
        return _go(canned)


def _try_exit():
    """Попытка выйти. Победа только с ключом."""
    print('Дверь заперта...')
    sounds.error()
    pause(0.6)
    if state.has('key'):
        print('Вы вставляете ключ и поворачиваете его. Дверь открывается!')
        pause(0.9)
        print(art.WIN)
        sounds.win()
        state.finish(win=True)
    else:
        print('Вам нужен ключ. Без него дверь не открыть.')
        pause(0.5)
        return exit_room()