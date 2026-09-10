"""Локации квеста: одна функция на локацию.

Функции локаций вызывают друг друга напрямую — это и есть
косвенная (mutual) рекурсия: canned -> toys -> dairy -> toys -> ...
"""
import random

from . import state, art
from .utils import prompt, pause, clear


# ----------------------- вспомогательное -----------------------

def _room(key, title, description):
    """Отрисовка локации."""
    clear()
    print(art.ROOMS.get(key, ''))
    print(f'--- {title} ---')
    print(description)
    pause(0.6)
    print('Инвентарь:', ', '.join(state.inventory) or 'пусто')


def _die(message):
    """Смерть игрока."""
    print(message)
    pause(0.8)
    print(art.GAMEOVER)
    state.finish(win=False)


# --------------------------- локации ---------------------------

def canned():
    """Консервный отдел — стартовая локация."""
    _room('canned', 'Консервный отдел',
          'Вокруг банки с человечиной. Пахнет странно.')
    c = prompt([
        'Съесть банку консервов',
        'Идти в отдел игрушек',
        'Идти на кассу',
        'Идти в туалет',
    ])
    if c == 1:
        _eat_can()
    elif c == 2:
        toys()
    elif c == 3:
        cashier()
    elif c == 4:
        toilet()


def _eat_can():
    print('Вы открыли банку и съели содержимое...')
    pause(1.0)
    if random.random() < 0.8:
        _die('Вы умерли от хантавируса!')
    else:
        print('Вам повезло. Вы живы.')
        pause(0.5)
        toys()


def toys():
    """Отдел игрушек — встреча с Татата Сауром."""
    _room('toys', 'Отдел игрушек',
          'Вас заметил Татата Саур! Он очень голоден.')
    c = prompt([
        'Сбежать в кисломолочку',
        'Попытаться отбиться',
        'Спрятаться в плюшевых игрушках',
        'Вернуться в консервный отдел',
    ])
    if c == 1:
        dairy()
    elif c == 2:
        _fight()
    elif c == 3:
        _hide_toys()
    elif c == 4:
        canned()


def _fight():
    print('Вы пытаетесь отбиться от Татата Саура...')
    pause(0.8)
    if state.has('pistol'):
        print('Вы стреляете из пистолета!')
        pause(0.6)
        if random.random() < 0.7:
            _die('Саур ранен, но вы всё равно погибаете в схватке.')
        else:
            print('Вы отбились!')
            dairy()
    else:
        if random.random() < 0.9:
            _die('Саур забил вас до смерти.')
        else:
            print('Каким-то чудом вы отбились!')
            dairy()


def _hide_toys():
    print('Вы прячетесь среди плюшевых игрушек...')
    pause(0.9)
    if random.random() < 0.7:
        _die('Черемша и Лабубу съели вас заживо!')
    else:
        print('Вам удалось спрятаться.')
        pause(0.5)
        toys()


def dairy():
    """Кисломолочный отдел."""
    _room('dairy', 'Кисломолочный отдел',
          'На полках стоят йогурты Тёма и Чудо.')
    c = prompt([
        'Выпить Тёму',
        'Выпить Чудо',
        'Пойти в подсобку',
        'Вернуться в отдел игрушек',
    ])
    if c == 1:
        _drink_tema()
    elif c == 2:
        _drink_chudo()
    elif c == 3:
        staff()
    elif c == 4:
        toys()


def _drink_tema():
    print('Вы пьёте Тёму...')
    pause(0.8)
    if random.random() < 0.9:
        _die('Он был просрочен 67 лет назад. Вы умерли.')
    else:
        print('Чудесным образом вы выжили.')
        dairy()


def _drink_chudo():
    print('Вы пьёте Чудо...')
    pause(1.2)
    if random.random() < 0.25:
        print('Произошло чудо! Вы проснулись в своей кровати. Это был сон.')
        state.finish(win=True)
    else:
        print('Чуда не случилось, но стало легче.')
        pause(0.5)
        dairy()


def staff():
    """Подсобка персонала."""
    _room('staff', 'Подсобка персонала',
          'Пыльно, темно, пахнет картоном.')
    c = prompt([
        'Поискать что-нибудь',
        'Пойти в молочный отдел',
        'Пойти на склад',
    ])
    if c == 1:
        _search_staff()
    elif c == 2:
        dairy()
    elif c == 3:
        warehouse()


def _search_staff():
    if 'key' not in state.taken_items:
        state.add('key')
        print('Вы нашли ключ от выхода!')
    else:
        print('Здесь больше ничего нет.')
    pause(0.6)
    staff()


def cashier():
    """Касса."""
    _room('cashier', 'Касса',
          'Здесь стоит кассирша и внимательно смотрит на вас.')
    c = prompt([
        'Поговорить с кассиршей',
        'Нагрубить кассирше',
        'Пойти в отдел игрушек',
        'Пойти в туалет',
    ])
    if c == 1:
        _talk_cashier()
    elif c == 2:
        _rude_cashier()
    elif c == 3:
        toys()
    elif c == 4:
        toilet()


def _talk_cashier():
    print('Кассирша: «Дверь откроется, если найдёшь потерянную наличку».')
    pause(0.8)
    if state.has('money'):
        print('Вы отдаёте деньги. Кассирша открывает дверь!')
        pause(0.6)
        state.finish(win=True)
    else:
        print('Она ждёт деньги.')
        pause(0.5)
        cashier()


def _rude_cashier():
    print('Вы грубите кассирше...')
    pause(0.7)
    if random.random() < 0.8:
        _die('У неё пистолет. Она вас застрелила.')
    else:
        print('Кассирша удивлена и отступает.')
        pause(0.5)
        cashier()


def toilet():
    """Туалет."""
    _room('toilet', 'Туалет', 'Темно и воняет.')
    c = prompt([
        'Поискать что-нибудь',
        'Вернуться в консервный отдел',
        'Спрятаться в кабинке',
    ])
    if c == 1:
        _search_toilet()
    elif c == 2:
        canned()
    elif c == 3:
        _hide_toilet()


def _search_toilet():
    if 'flashlight' not in state.taken_items:
        state.add('flashlight')
        print('Вы нашли фонарик!')
    else:
        print('В туалете пусто.')
    pause(0.6)
    toilet()


def _hide_toilet():
    print('Вы спрятались в кабинке...')
    pause(0.8)
    if random.random() < 0.8:
        _die('Нечто напало на вас из унитаза!')
    else:
        print('Вы быстро выбежали.')
        toilet()


def warehouse():
    """Склад."""
    _room('warehouse', 'Склад', 'Много коробок, повсюду пыль.')
    c = prompt([
        'Поискать что-нибудь',
        'Пойти в комнату охраны',
        'Вернуться в подсобку',
    ])
    if c == 1:
        _search_warehouse()
    elif c == 2:
        security()
    elif c == 3:
        staff()


def _search_warehouse():
    if 'money' not in state.taken_items:
        state.add('money')
        print('Вы нашли потерянную наличку!')
    elif 'medkit' not in state.taken_items:
        state.add('medkit')
        print('Вы нашли аптечку (бесполезную).')
    else:
        print('На складе больше ничего полезного.')
    pause(0.6)
    warehouse()


def security():
    """Комната охраны."""
    _room('security', 'Комната охраны',
          'Мониторы показывают пустые залы. В углу — шкаф.')
    c = prompt([
        'Попытаться открыть шкаф',
        'Пойти на склад',
        'Пойти к выходу',
    ])
    if c == 1:
        _open_locker()
    elif c == 2:
        warehouse()
    elif c == 3:
        exit_room()


def _open_locker():
    print('Шкаф заперт.')
    pause(0.5)
    if state.has('key'):
        print('Вы открываете шкаф ключом...')
        pause(0.8)
        if 'pistol' in state.taken_items:
            print('Шкаф пуст.')
        elif random.random() < 0.6:
            print('Внутри пистолет! Вы забираете его.')
            state.add('pistol')
        else:
            _die('Шкаф пуст. Сработала сигнализация, вас окружили.')
            return
    else:
        print('Нужен ключ.')
    pause(0.6)
    security()


def exit_room():
    """Выход из магазина."""
    _room('exit', 'Выход', 'Дверь на улицу. Она заперта.')
    c = prompt([
        'Попытаться открыть дверь',
        'Вернуться в магазин',
    ])
    if c == 1:
        _try_exit()
    elif c == 2:
        canned()


def _try_exit():
    print('Дверь заперта...')
    pause(0.6)
    if state.has('key'):
        print('Вы вставляете ключ и поворачиваете его. Дверь открывается!')
        pause(0.8)
        state.finish(win=True)
    else:
        print('Вам нужен ключ.')
        pause(0.5)
        exit_room()