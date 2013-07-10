from datetime import date

import db

def index(params):
    result = {
        'data_min': 150,
        'data_max': 199,
        'data_columns': 10
    }

    return result

def data(params):
    if params.get('post'):
        db.insert('data', {
            'type': 'weight',
            'value': params['post']['value'],
            'user_id': 1,
            'date': date.isoformat(date.today())
        })

        return
    elif len(params['path']) > 1:
        dt = params['path'][1]
        if dt == 'today':
            dt = date.isoformat(date.today())
        return db.row('select type, date, value from data where user_id=%s and type=%s and date=%s',
            (1, 'weight', dt))
    else:
        # The whole data set
        return db.rows('select type, date, value from data where user_id=%s and type=%s',
            (1, 'weight'))