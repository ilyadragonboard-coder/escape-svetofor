"""Запуск и стартовый экран игры."""
import sys

from . import state, art
from .utils import pause, clear
from .locations import canned

# На всякий случай поднимем лимит рекурсии —
# локации вызывают друг друга косвенно.
sys.setrecursionlimit(10000)


def start_game():
    """Точка входа игры."""
    clear()
    print(art.LOGO)
    print('Добро пожаловать в текстовый квест «Побег из Светофора»!')
    print('Цель: выбраться из магазина живым.')
    print('Подсказка: исследуйте локации, собирайте предметы,')
    print('а инвентарь можно посмотреть по клавише "i".')
    pause(1.2)
    input('\nНажмите Enter, чтобы начать...')

    state.reset()
    canned()

    print('\nИгра завершена.')