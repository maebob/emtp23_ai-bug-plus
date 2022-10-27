import json
import random
import sys

#Needed otherwise module will not be found
sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/')
from src.engine import eval

#Non-Nested
INCREMENTOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/incrementor.json"
DECREMENTOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/decrementor.json"
IS_ZERO_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/isZero.json"
INCREMENTOR_ITERATOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/incrementIterator.json"

#Nested
NESTED_INCREMENTOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/nestedIncrementor.json"



def test_incrementor():
    """Test the incrementor function."""
    example_file = open(INCREMENTOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(100):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        assert eval.main(example).get("0_dataOut") == random_number_1 + 1

def test_decrementor():
    """Test the decrementor function."""
    DECREMENTOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/decrementor.json"
    example_file = open(DECREMENTOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(100):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = 4
        print(eval.main(example).get("0_dataOut") == random_number_1 - 1)
        assert eval.main(example).get("0_dataOut") == random_number_1 - 1

def test_is_zero():
    """Test the is_zero function."""
    example_file = open(IS_ZERO_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(100):
        random_number_1 = random.randint(-10, 10)
        random_number_2 = random.randint(-10, 10)
        example["xValue"] = random_number_1
        example["yValue"] = random_number_2
        result = eval.main(example)
        if random_number_1 + random_number_2 == 0:
            assert result.get("0_controlOutL") == 0
            assert result.get("0_controlOutR") == 1
        else:
            assert result.get("0_controlOutL") == 1
            assert result.get("0_controlOutR") == 0

def test_incrementor_iterator():
    """Test the incrementor iterator function."""
    example_file = open(INCREMENTOR_ITERATOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(100):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        assert eval.main(example).get("0_dataOut") == random_number_1 + 1

def test_nested_incrementor():
    """Test the nested incrementor function."""
    example_file = open(NESTED_INCREMENTOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(100):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        assert eval.main(example).get("0_dataOut") == random_number_1 + 1