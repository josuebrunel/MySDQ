import json
import os

import pytest


@pytest.fixture
def data(request):
    filepath = os.path.join(os.path.dirname(__file__), 'users.json')
    return json.load(open(filepath))
