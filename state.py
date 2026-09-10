"""Глобальное состояние игры: инвентарь, взятые предметы, флаг конца."""

inventory = []
taken_items = {}
game_over = False


def reset():
    """Сбросить состояние перед новой партией."""
    global game_over
    game_over = False
    inventory.clear()
    taken_items.clear()


def add(item):
    """Положить предмет в инвентарь."""
    if item not in inventory:
        inventory.append(item)
    taken_items[item] = True


def has(item):
    """Есть ли предмет в инвентаре."""
    return item in inventory


def take(item):
    """Изъять предмет из инвентаря."""
    if item in inventory:
        inventory.remove(item)
    taken_items.pop(item, None)


def finish(win=False):
    """Завершить игру (победой или смертью)."""
    global game_over
    game_over = True
    if win:
        print('\n*** ПОБЕДА! Вы выбрались из Светофора! ***')
    else:
        print('\n*** Игра окончена. Вы погибли. ***')