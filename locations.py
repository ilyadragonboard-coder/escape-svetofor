"""Запуск игры: стартовый экран и вход в первую локацию."""
import sys

from . import state, art
from .utils import pause, clear
from .locations import canned

# Локации вызывают друг друга взаимно (косвенная рекурсия),
# поэтому поднимаем лимит рекурсии с запасом.
sys.setrecursionlimit(10000)


def start_game():
    """Главная точка входа игры."""
    clear()
    print(art.LOGO)

    print('Цель: выбраться из магазина живым.')
    print('Подсказки:')
    print('  • номер + Enter — выбрать действие;')
    print('  • i — посмотреть инвентарь;')
    print('  • j — журнал найденных записок;')
    print('  • h — помощь;  q — выход.')
    pause(1.4)

    input('\nНажмите Enter, чтобы начать...')

    state.reset()
    canned()  # стартовая локация

    # Сюда управление вернётся только после завершения партии.
    pause(0.8)