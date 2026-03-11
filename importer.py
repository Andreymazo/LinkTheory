import csv
from core import LinkTheoryCore

def import_csv_to_links(file_path):
    core = LinkTheoryCore()
    
    # Создаем маркеры типов для структуры CSV
    row_type = core.create_point("CSV_ROW")
    col_type = core.create_point("COLUMN_VAL")

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # Создаем точку для всей строки
            row_id = core.create_point(f"row_{i}")
            core.create_link(row_id, row_type) # Помечаем что это строка
            
            for column, value in row.items():
                # Создаем (или находим) точку для значения
                # В идеале тут нужна проверка на уникальность (Deduplication)
                val_id = core.create_point(value)
                
                # Связываем строку со значением
                core.create_link(row_id, val_id)
            
            if i % 100 == 0:
                print(f"Импортировано {i} строк...")

# Давай создадим тестовый файл, если его нет
def create_test_csv():
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "item", "category"])
        for i in range(1000):
            cat = "Electronics" if i % 2 == 0 else "Books"
            writer.writerow([f"2024-03-{i%30+1}", f"Item_{i}", cat])

if __name__ == "__main__":
    create_test_csv()
    import_csv_to_links('data.csv')
