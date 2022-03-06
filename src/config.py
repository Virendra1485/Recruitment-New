import os


class Config:
    SECRET_KEY = '6a7645989121887a3e9162454089857b'

    PORT = os.environ.get('PORT', 5000)
    print("PORT : ", PORT)
    if not PORT:
        print("PORT Is Not Set")
        exit(1)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
    print('DB_URL  : ', SQLALCHEMY_DATABASE_URI)
    # mysql+pymysql://root:root@127.0.0.1/vrecruit
    if not SQLALCHEMY_DATABASE_URI:
        print("DB_URL not set . Quiting")
        exit(1)

    THREAD_COUNT = int(os.environ.get('THREAD_COUNT', 2))
    print("THREAD_COUNT : ", THREAD_COUNT)
    if not PORT:
        print("THREAD_COUNT Is Not Set")
        exit(1)

    PASSWORD = os.environ.get('PASSWORD', 'Python@123')
    print("PASSWORD : ", PASSWORD)
    if not PASSWORD:
        print("PASSWORD Is Not Set")
        exit(1)

    TEST_DIFFICULTY_LEVEL = os.environ.get('TEST_DIFFICULTY_LEVEL', 2)
    print("TEST_DIFFICULTY_LEVEL : ", TEST_DIFFICULTY_LEVEL)

    NO_OF_QUESTION = os.environ.get('NO_OF_QUESTION', 10)
    print("NO_OF_QUESTION : ", NO_OF_QUESTION)