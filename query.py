import time
from core import LinkTheoryCore

def find_rows_by_value(value_to_find: str):
    core = LinkTheoryCore()
    start_time = time.perf_counter()

    # 1. Находим ID узла, который содержит искомое значение
    core.cursor.execute("SELECT link_id FROM values_store WHERE val = ?", (value_to_find,))
    result = core.cursor.fetchone()
    
    if not result:
        print(f"Значение '{value_to_find}' не найдено в базе.")
        return

    target_id = result[0]
    print(f"Найдена точка значения '{value_to_find}' с ID: {target_id}")

    # 2. Находим все связи, указывающие на этот узел (наши строки в CSV)
    # В ассоциативной модели это мгновенная операция по индексу
    core.cursor.execute("SELECT source FROM links WHERE target = ?", (target_id,))
    rows = core.cursor.fetchall()

    end_time = time.perf_counter()
    
    print(f"Найдено связей: {len(rows)}")
    print(f"Время поиска: {end_time - start_time:.6f} сек.")

    # Выведем первые 5 для примера
    print("\nПервые 5 найденных строк (их ID в системе):")
    for (r_id,) in rows[:5]:
        # Можем даже посмотреть "соседей" этой строки (другие колонки)
        core.cursor.execute("""
            SELECT v.val FROM links l 
            JOIN values_store v ON l.target = v.link_id 
            WHERE l.source = ? AND l.target != ?
        """, (r_id, target_id))
        details = core.cursor.fetchall()
        print(f"Строка {r_id}: {[d[0] for d in details]}")

if __name__ == "__main__":
    # Ищем все записи категории Electronics
    find_rows_by_value("Electronics")
