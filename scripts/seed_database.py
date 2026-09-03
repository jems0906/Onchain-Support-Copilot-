from app.database import init_db


if __name__ == '__main__':
    init_db()
    print('Database schema initialized when DATABASE_URL is configured.')
