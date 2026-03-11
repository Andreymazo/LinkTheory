from core import LinkTheoryCore

class LinkFS:
    def __init__(self, core: LinkTheoryCore):
        self.core = core
        # Инициализируем системные типы (если их нет)
        # В реальной системе это "зашитые" ID
        self.TYPE_MARKER = self.core.create_point("SYSTEM_TYPE")
        self.FOLDER_TYPE = self.core.create_point("FOLDER")
        self.FILE_TYPE = self.core.create_point("FILE")

    def create_folder(self, name: str, parent_id: int = None):
        """Создает папку как точку со значением имени и связывает с типом FOLDER"""
        folder_id = self.core.create_point(name)
        # Указываем, что это папка
        self.core.create_link(folder_id, self.FOLDER_TYPE)
        # Если есть родитель, связываем с ним
        if parent_id:
            self.core.create_link(folder_id, parent_id)
        return folder_id

    def create_file(self, name: str, content: str, parent_id: int):
        """Создает файл, связывает с FILE_TYPE и родителем"""
        file_id = self.core.create_point(name)
        content_id = self.core.create_point(content)
        
        self.core.create_link(file_id, self.FILE_TYPE) # Это файл
        self.core.create_link(file_id, content_id)    # У него такое содержимое
        self.core.create_link(file_id, parent_id)     # Он в этой папке
        return file_id

    def list_assets(self, parent_id: int):
        """
        Тут начинается магия связей: 
        нужно найти все ID, которые ссылаются на parent_id
        """
        # Пока упростим: заберем все связи из БД, где target = parent_id
        self.core.cursor.execute("SELECT source FROM links WHERE target = ?", (parent_id,))
        children = self.core.cursor.fetchall()
        
        print(f"\n--- Содержимое ID {parent_id} ---")
        for (child_id,) in children:
            val = self.core.get_value(child_id)
            print(f"[{child_id}] {val[0] if val else 'Без названия'}")

# Тест драйв нашей ФС
if __name__ == "__main__":
    core_engine = LinkTheoryCore()
    my_fs = LinkFS(core_engine)

    # 1. Создаем корневую папку
    root = my_fs.create_folder("ROOT_DISK")

    # 2. Создаем внутри папку PROJECTS
    projects = my_fs.create_folder("PROJECTS", root)

    # 3. Кладем файл в PROJECTS
    my_fs.create_file("plan.txt", "Купить молоко и захватить мир", projects)

    # 4. Смотрим что в PROJECTS
    my_fs.list_assets(projects)
