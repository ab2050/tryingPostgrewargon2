import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #will break if path isn't mentioned
from mainpage import app #won't find mainpage otherwise
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"]=False

    with app.test_client() as client:
        yield client