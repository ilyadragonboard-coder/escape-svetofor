"""Глобальное изменяемое состояние игры.

Здесь хранится всё, что меняется по ходу партии:
инвентарь, найденные предметы, прочитанные записки,
сюжетные флаги и признак завершения игры.

Такой подход (единый модуль состояния) позволяет
любой локации читать и менять мир игры.
"""

# --- изменяемое состояние ---
inventory = []        # список предметов у игрока
taken_items = {}      # что уже подобрано (защита от дублирования)
read_notes = []       # id прочитанных записок
flags = {}            # произвольные сюжетные флаги
game_over = False     # True, когда партия завершена


def reset():
    """Сбросить всё состояние перед новой партией."""
    global game_over
    game_over = False
    inventory.clear()
    taken_items.clear()
    read_notes.clear()
    flags.clear()


def add(item):
    """Положить предмет в инвентарь (если его там ещё нет)."""
    if item not in inventory:
        inventory.append(item)
    taken_items[item] = True


def has(item):
    """Есть ли предмет у игрока."""
    return item in inventory


def take(item):
    """Изъять предмет из инвентаря."""
    if item in inventory:
        inventory.remove(item)
    taken_items.pop(item, None)


def read_note(note_id):
    """Отметить записку как прочитанную.

    Возвращает True, если записка встретилась впервые.
    """
    if note_id in read_notes:
        return False
    read_notes.append(note_id)
    return True


def finish(win=False):
    """Завершить игру: победой или смертью."""
    global game_over
    game_over = True
    print()
    if win:
        print('=' * 60)
        print('  ПОБЕДА! Вы выбрались из Светофора живым!')
        print('=' * 60)
    else:
        print('=' * 60)
        print('  Игра окончена. Вы погибли...')
        print('=' * 60)