from fizzbuzz import fizzbuzz
import pytest

def test_returns_fizz_when_divisible_by_three():
    assert fizzbuzz(9) == "fizz"

def test_returns_buzz_when_divisible_by_five():
    assert fizzbuzz(10) == "buzz"

def test_returns_fizzbuzz_when_divisible_by_both():
    assert fizzbuzz(15) == "fizzbuzz"
    
def test_returns_buzzfizz_when_divisible_by_neither():
    assert fizzbuzz(14) == "buzzfizz"