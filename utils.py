"""Вспомогательные утилиты: пауза, очистка экрана, ввод."""
import os
import sys
import time

from . import state


def pause(seconds=0.7):
    """Небольшая пауза — добавляет атмосферы."""
    time.sleep(seconds)


def clear():
    """Очистка консоли (кроссплатформенно)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt(options, allow_inventory=True):
    """Показать меню и вернуть номер выбранного пункта (1..N).

    Некорректный ввод не роняет программу — просим повторить.
    """
    while True:
        print()
        for i, opt in enumerate(options, 1):
            print(f'  {i}. {opt}')
        if allow_inventory:
            print('  i — инвентарь')
            print('  q — выйти из игры')
        raw = input('> ').strip().lower()

        if allow_inventory and raw == 'i':
            print('Инвентарь:', ', '.join(state.inventory) or 'пусто')
            continue
        if allow_inventory and raw == 'q':
            print('Вы вышли из игры.')
            sys.exit(0)
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw)

        print(f'Некорректный ввод. Введите число от 1 до {len(options)}.')