"""Запуск игры: стартовый экран и вход в первую локацию."""
import sys

from . import state, art, sounds
from .utils import pause, clear
from .locations import canned

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
    print('  • s — включить/выключить звук;')
    print('  • h — помощь;  q — выход.')
    print()
    print('  ' + sounds.status_text())
    pause(1.4)

    input('\nНажмите Enter, чтобы начать...')

    state.reset()
    sounds.step()
    canned()

    pause(0.8)