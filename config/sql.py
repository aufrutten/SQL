__all__ = ['postgresql']

import os
postgresql = {
    'user': os.getenv('USER'),
    'password': 'pass',
    'host': 'localhost',
    'port': 5432,
    'path_db': 'testdb'
}

if __name__ == '__main__':
    print(postgresql)
