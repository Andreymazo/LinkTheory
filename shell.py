import sys
from core import LinkTheoryCore

class LinkShell:
    def __init__(self):
        self.core = LinkTheoryCore()
        self.current_id = 1  # Начинаем с первой точки (обычно это корень)
        self.history = []

    def get_info(self, l_id):
        val = self.core.get_value(l_id)
        data = self.core.get_link(l_id)
        # Убираем [0], так как val уже строка!
        return f"ID: {l_id} | Val: '{val if val else 'None'}' | Link: {data}"

    
    def resolve_name_to_id(self, name: str):
        """Ищет ID узла по его текстовому значению через курсор ядра"""
        self.core.cursor.execute("SELECT link_id FROM values_store WHERE val = ?", (name,))
        results = self.core.cursor.fetchall()  # Исправлено: обращаемся к курсору
        
        if not results:
            return None
        
        # Если найдено несколько, выводим список и берем первый
        if len(results) > 1:
            ids = [r[0] for r in results]
            print(f"Найдено несколько узлов '{name}': {ids}. Выбираю первый: {ids[0]}")
            return ids[0]
            
        return results[0][0] # Возвращаем ID (первый элемент первого кортежа)

    def run(self):
        print("--- LinkTheory Shell v0.1 ---")
        print("Команды: ls, cd <id>, info <id>, back, exit")
        
        while True:
            prompt = f"\n[Current ID: {self.current_id}] > "
            cmd_input = input(prompt).strip().split()
            
            if not cmd_input: continue
            cmd = cmd_input[0].lower()
            args = cmd_input[1:]

            if cmd == "exit": break
            
            elif cmd == "ls":
                # Показываем все связи, где текущий узел является целью (входящие)
                # и источником (исходящие)
                print(f"Связи для {self.current_id}:")
                
                self.core.cursor.execute("SELECT id, source FROM links WHERE target = ? AND id != ?", (self.current_id, self.current_id))
                inbound = self.core.cursor.fetchall()
                for lid, src in inbound:
                    val = self.core.get_value(src)
                    print(f"  <-- [ID {src}] {val if val else '??'}")

                self.core.cursor.execute("SELECT id, target FROM links WHERE source = ? AND id != ?", (self.current_id, self.current_id))
                outbound = self.core.cursor.fetchall()
                for lid, tgt in outbound:
                    val = self.core.get_value(tgt)
                    print(f"  --> [ID {tgt}] {val if val else '??'}")

            elif cmd == "cd":
                if args:
                    target = args[0]
                    # Пытаемся понять: это число (ID) или имя (строка)?
                    if target.isdigit():
                        new_id = int(target)
                    else:
                        new_id = self.resolve_name_to_id(target)
                    
                    if new_id:
                        self.history.append(self.current_id)
                        self.current_id = new_id
                        print(f"Переход в {self.get_info(new_id)}")
                    else:
                        print(f"Узел '{target}' не найден.")

            elif cmd == "back":
                if self.history:
                    self.current_id = self.history.pop()
                else:
                    print("История пуста")

            elif cmd == "info":
                target = int(args[0]) if args else self.current_id
                print(self.get_info(target))

            else:
                print("Неизвестная команда")

if __name__ == "__main__":
    shell = LinkShell()
    shell.run()
