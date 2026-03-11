import sqlite3

class LinkTheoryCore:
    def __init__(self, db_path="links.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        # Таблица связей (структура L -> L^2)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source INTEGER NOT NULL,
                target INTEGER NOT NULL
            )
        ''')
        # Таблица значений (храним "мясо" данных)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS values_store (
                link_id INTEGER PRIMARY KEY,
                val TEXT,
                FOREIGN KEY(link_id) REFERENCES links(id)
            )
        ''')
        self.conn.commit()

    def create_point(self, value=None) -> int:
        """Создает точку и опционально привязывает к ней значение (строку/число)"""
        self.cursor.execute("INSERT INTO links (source, target) VALUES (0, 0)")
        new_id = self.cursor.lastrowid
        self.cursor.execute("UPDATE links SET source = ?, target = ? WHERE id = ?", (new_id, new_id, new_id))
        
        if value is not None:
            self.cursor.execute("INSERT INTO values_store (link_id, val) VALUES (?, ?)", (new_id, str(value)))
        
        self.conn.commit()
        return new_id

    def create_link(self, source: int, target: int) -> int:
        self.cursor.execute("INSERT INTO links (source, target) VALUES (?, ?)", (source, target))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_value(self, link_id: int):
        self.cursor.execute("SELECT val FROM values_store WHERE link_id = ?", (link_id,))
        res = self.cursor.fetchone()
        return res[0] if res else None

# Тест новых возможностей
if __name__ == "__main__":
    core = LinkTheoryCore()
    
    # Создаем объект "Файл" со значением "my_photo.jpg"
    file_name_link = core.create_point("my_photo.jpg")
    
    # Создаем объект "Папка" со значением "Documents"
    folder_link = core.create_point("Documents")
    
    # Связываем их: Файл "находится в" Папке
    relation = core.create_link(file_name_link, folder_link)
    
    print(f"Имя файла (ID {file_name_link}): {core.get_value(file_name_link)}")
    print(f"Папка (ID {folder_link}): {core.get_value(folder_link)}")
    print(f"Связь создана (ID {relation})")


# import sqlite3

# class LinkTheoryCore:
#     def __init__(self, db_path="links.db"):
#         self.conn = sqlite3.connect(db_path)
#         self.cursor = self.conn.cursor()
#         self._setup_db()

#     def _setup_db(self):
#         # Создаем единственную таблицу, которая нам нужна
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS links (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 source INTEGER NOT NULL,
#                 target INTEGER NOT NULL
#             )
#         ''')
#         self.conn.commit()

#     def create_link(self, source: int, target: int) -> int:
#         """Создает новую связь между двумя ID"""
#         self.cursor.execute(
#             "INSERT INTO links (source, target) VALUES (?, ?)", 
#             (source, target)
#         )
#         self.conn.commit()
#         return self.cursor.lastrowid

#     def create_point(self) -> int:
#         """
#         Создает 'точку' (вершину). 
#         В теории связей это связь, указывающая на саму себя.
#         Сначала создаем пустую запись, затем фиксируем её ID на себя.
#         """
#         self.cursor.execute("INSERT INTO links (source, target) VALUES (0, 0)")
#         new_id = self.cursor.lastrowid
#         self.cursor.execute(
#             "UPDATE links SET source = ?, target = ? WHERE id = ?", 
#             (new_id, new_id, new_id)
#         )
#         self.conn.commit()
#         return new_id

#     def get_link(self, link_id: int):
#         self.cursor.execute("SELECT source, target FROM links WHERE id = ?", (link_id,))
#         return self.cursor.fetchone()

# # Тестовый запуск
# if __name__ == "__main__":
#     core = LinkTheoryCore()
    
#     # Создаем две "точки" (аналог объектов или папок)
#     point_a = core.create_point()
#     point_b = core.create_point()
    
#     # Создаем связь между ними (дуплет)
#     connection = core.create_link(point_a, point_b)
    
#     print(f"Точка А: {point_a}")
#     print(f"Точка Б: {point_b}")
#     print(f"Связь А->Б: {connection} (состав: {core.get_link(connection)})")