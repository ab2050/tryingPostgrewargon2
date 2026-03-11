import pytest
from passwordAuth import store,verify,passwordstrength

# cd LTU_TERMS/SecureSWDev/argon2withpostgre

pwd = "Abcd!1234"
def test_store():
    testhash = store(pwd)
    assert testhash is not None #checks that the function is returning
    assert testhash !=pwd #checks that password isn't being stored in plain text

def test_verify():
    testhash = store(pwd)
    assert verify(testhash,pwd) is None

def test_pwdStrength_correct():
    assert passwordstrength(pwd) is not None

def test_pwdStrength_7chars():
    assert passwordstrength("Wor123#") is None

def test_pwdStrength_noCaps():
    assert passwordstrength("wwor123#") is None

def test_pwdStrength_noNums():
    assert passwordstrength("Words!@#$") is None

def test_pwdStrength_nolowercase():
    assert passwordstrength("WWOR123#") is None

def test_pwdStrength_noCharacters():
    assert passwordstrength("wwor123A") is None