import aiosqlite

async def create_database():
    async with aiosqlite.connect("mydatabase.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    num INTEGER PRIMARY KEY AUTOINCREMENT,
                    id INTEGER UNIQUE,
                    fullname TEXT,
                    username TEXT
                )
            ''')
            await db.commit()

async def insert_account(id, fullname, username):
    async with aiosqlite.connect("mydatabase.db") as db:
        async with db.cursor() as cursor:
            try:
                await cursor.execute('''
                    INSERT INTO accounts (id, fullname, username) VALUES (?, ?, ?)
                ''', (id, fullname, username))
                await db.commit()
                return True
            except Exception as e:
                    return False

# Пример использования:
async def main():
    await create_database()

    # Пример добавления записей
    await insert_account(123, "John Doe", "username123")
    await insert_account(456, "Jane Doe", "username456")

    # Получение последней записи
    last_account = await 
    print("Last Account:", last_account)

    # Пример добавления новой записи с автоматическим увеличением num
    await insert_account(789, "Bob Smith", "username789")

    # Получение обновленной последней записи

# Запуск цикла событий
