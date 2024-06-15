from datetime import datetime
from typing import Tuple

import uvicorn
from pydantic import BaseModel, ValidationError, PositiveInt


class Delivery(BaseModel):
    timestamp: datetime
    dimensions: Tuple[int, int]

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime
    tastes: dict[str, PositiveInt]


if __name__ == '__main__':
    print('Hello world')

    try:
        m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
        print(repr(m.timestamp))
        print(m.dimensions)
        print(f'SCHEMA {Delivery.model_json_schema()}')

        external_data = {
            'id': 123,
            'signup_ts': '2019-06-01 12:22',
            'tastes': {
                'wine': 9,
                b'cheese': 7,
                'cabbage': '1',
            },
        }

        user = User(**external_data)
        print(f'USER: {user}')
        print(f'USER: {user.name}')
    except ValidationError as e:
        print(f'PROBLEM: {e.errors()}')

    uvicorn.run('api.v1.nmap_api:app', port=5000, log_level='info')
