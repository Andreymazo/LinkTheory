from core import LinkTheoryCore

core = LinkTheoryCore()

# 1. Создаем узел-тег (благодаря дедупликации он создастся один раз)
fav_id = core.create_point("Favorites")

# 2. Связываем нашу строку row_0 (ID 3) с этим тегом
# Мы создаем НОВУЮ связь, где источником будет строка, а целью - тег
relation = core.create_link(3, fav_id)

print(f"Готово! Строка ID 3 (row_0) теперь связана с 'Favorites' (ID {fav_id})")
print(f"ID новой связи: {relation}")
