import os

config = {
    'database_url': os.environ['DATABASE_URL']
}

def test():
    import test.config_test
    config.update(test.config_test.config)