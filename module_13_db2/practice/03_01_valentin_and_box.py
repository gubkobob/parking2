import sqlite3

defeated_enemies = [
    "Иванов Э.",
    "Петров Г.",
    "Левченко Л.",
    "Михайлов М.",
    "Яковлев Я",
    "Кузнецов К.",
]


def remove_all_defeated_enemies(
        c: sqlite3.Cursor,
        defeated_enemies: list[str]
) -> None:
    ...


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        remove_all_defeated_enemies(cursor, defeated_enemies)
        conn.commit()
