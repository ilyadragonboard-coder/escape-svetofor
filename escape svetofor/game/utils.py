"""Вспомогательные утилиты: пауза, очистка экрана, ввод игрока."""
import os
import sys
import time

from . import state, sounds


def pause(seconds=0.7):
    """Небольшая пауза — добавляет атмосферы."""
    time.sleep(seconds)


def clear():
    """Очистка консоли (кроссплатформенно)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_inventory():
    """Показать инвентарь игрока."""
    if state.inventory:
        print('  Инвентарь: ' + ', '.join(state.inventory))
    else:
        print('  Инвентарь пуст.')


def show_journal():
    """Показать журнал — сколько записок найдено."""
    total = 6
    found = len(state.read_notes)
    print(f'  Журнал: найдено {found} из {total} записок.')


def prompt(options, allow_inventory=True):
    """Показать меню и вернуть номер выбранного пункта (1..N).

    Некорректный ввод не роняет программу — просим повторить.
    Команды: i — инвентарь, j — журнал, s — звук, h — помощь, q — выход.
    """
    while True:
        print()
        for i, opt in enumerate(options, 1):
            print(f'  {i}. {opt}')

        if allow_inventory:
            print('  ───')
            print('  i — инвентарь, j — журнал, s — звук, '
                  'h — помощь, q — выход')

        raw = input('> ').strip().lower()

        if allow_inventory and raw == 'i':
            show_inventory()
            continue
        if allow_inventory and raw == 'j':
            show_journal()
            continue
        if allow_inventory and raw == 's':
            sounds.toggle()
            print('  ' + sounds.status_text())
            continue
        if allow_inventory and raw == 'h':
            print('  Введите номер действия из списка и нажмите Enter.')
            print('  Звук включается/выключается клавишей s.')
            continue
        if allow_inventory and raw == 'q':
            print('Вы вышли из игры.')
            sys.exit(0)
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw)

        sounds.error()
        print(f'  Некорректный ввод. Введите число от 1 до {len(options)}.')