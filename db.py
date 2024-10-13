import aiosqlite
from models import log_entry

async def create_table(DB_NAME):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS log_table 
        (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            user_text TEXT,
            utc_date TEXT,
            bot_text TEXT
        )''')
        await db.commit()

async def log_event(DB_NAME, log_entry):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO log_table (user_id, user_text, utc_date, bot_text) VALUES (?, ?, ?, ?)',
                          (log_entry.user_id, log_entry.user_text, log_entry.utc_date, log_entry.bot_text))
        await db.commit()

async def get_record_count(DB_NAME, user_id = 0, date_from = "", date_to = ""):
    count = 0
    query = ""
    parameters = None
    query = "SELECT count(*) FROM log_table"
    where = "WHERE"
    parameters = []
    if(user_id != 0):
        where += " user_id = (?)  and"
        parameters.append(user_id)
    if(date_from != ""):
        where += " utc_date >= (?)  and"
        parameters.append(date_from)
    if(date_to != ""):
        where += " utc_date <= (?)  and"
        parameters.append(date_to)
    where = where[0:-5]
    query = query + " " + where
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(query, parameters) as cursor:
            row = await cursor.fetchone()
            count = row[0]
    return count

async def get_logs(DB_NAME, user_id = 0, page = 1, page_size = 5, date_from = "", date_to = ""):
    logs = []
    query = ""
    query = "SELECT user_id, user_text, utc_date, bot_text FROM log_table"
    where = "WHERE"
    parameters = []
    if(user_id != 0):
        where += " user_id = (?)  and"
        parameters.append(user_id)
    if(date_from != ""):
        where += " utc_date >= (?)  and"
        parameters.append(date_from)
    if(date_to != ""):
        where += " utc_date <= (?)  and"
        parameters.append(date_to)
    where = where[0:-5]
    query = query + " " + where
    query += " limit " + str(page_size)
    query += " offset " + str((page - 1) * page_size)
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(query, parameters) as cursor:
            async for row in cursor:
                logs.append(log_entry(row[0], row[1], row[2], row[3]))
    return logs
