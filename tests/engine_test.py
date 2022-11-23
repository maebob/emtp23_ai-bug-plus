import json
import random
import sys
from engine import eval
# Non-Nested
INCREMENTOR_PATH = "Configurations/incrementor.json"
DECREMENTOR_PATH = "Configurations/decrementor.json"
IS_ZERO_PATH = "Configurations/isZero.json"
INCREMENTOR_ITERATOR_PATH = "Configurations/incrementIterator.json"
DECREMENTOR_ITERATOR_PATH = "Configurations/decrementIterator.json"
ASIGNMENT = "Configurations/asignment.json"

# Nested
NESTED_INCREMENTOR_PATH = "Configurations/nestedIncrementor.json"
PSEUDO_PARALLEL = "Configurations/pseudoParallel.json"
IS_POSITIVE_PATH = "Configurations/isPositive.json"
CHANGE_SIGN_PATH = "Configurations/changeSign.json"
MINUS_PATH = "Configurations/minus.json"
EQUAL_PATH = "Configurations/equalOperation.json"
IS_LARGER_Path = "Configurations/isLarger.json"
MULTIPLY_PATH = "Configurations/multiply.json"


def test_incrementor():
    """Test the incrementor function."""
    example_file = open(INCREMENTOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(10000):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        result = eval.main(example)
        assert result.get("0_Out") == random_number_1 + 1
        if result.get("0_Out") == 0:
            assert result.get("0_Left") == 1
            assert result.get("0_Right") == 0
        else:
            assert result.get("0_Left") == 0
            assert result.get("0_Right") == 1


def test_decrementor():
    """Test the decrementor function."""
    DECREMENTOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/Configurations/decrementor.json"
    example_file = open(DECREMENTOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(10000):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = 4
        assert eval.main(example).get("0_Out") == random_number_1 - 1


def test_is_zero():
    """Test the is_zero function."""
    example_file = open(IS_ZERO_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(10000):
        random_number_1 = random.randint(-10, 10)
        random_number_2 = random.randint(-10, 10)
        example["xValue"] = random_number_1
        example["yValue"] = random_number_2
        result = eval.main(example)
        if random_number_1 + random_number_2 == 0:
            assert result.get("0_Left") == 0
            assert result.get("0_Right") == 1
            assert result.get("0_Out") == 0
        else:
            assert result.get("0_Left") == 1
            assert result.get("0_Right") == 0
    


def test_incrementor_iterator():
    """Test the incrementor iterator function."""
    example_file = open(INCREMENTOR_ITERATOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(10000):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        assert eval.main(example).get("0_Out") == random_number_1 + 2


def test_decrementor_iterator():
    """Test the decrementor iterator function."""
    example_file = open(DECREMENTOR_ITERATOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(10000):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        assert eval.main(example).get("0_Out") == random_number_1 - 2


def test_asignment():
    """Test the asignment function."""
    example_file = open(ASIGNMENT, "r").read()
    example = json.loads(example_file)
    for i in range(10000):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        result = eval.main(example)
        assert result.get("0_Out") == random_number_1
        assert result.get("0_Left") == 1


def test_nested_incrementor():
    """Test the nested incrementor function."""
    example_file = open(NESTED_INCREMENTOR_PATH, "r").read()
    example = json.loads(example_file)
    for i in range(10000):
        random_number_1 = random.randint(-1000, 1000)
        example["xValue"] = random_number_1
        example["yValue"] = None
        assert eval.main(example).get("0_Out") == random_number_1 + 1


def test_pseudo_parallel():
    """Test the pseudo parallel function."""
    example_file = open(PSEUDO_PARALLEL, "r").read()
    example = json.loads(example_file)
    assert eval.main(example).get("0_Left") == 1
    assert eval.main(example).get("0_Right") == None


def test_is_positive():
    """Test the is_positive function."""
    example_file = open(IS_POSITIVE_PATH, "r").read()
    example = json.loads(example_file)

    # Test zero
    example["xValue"] = 0
    example["yValue"] = None
    result = eval.main(example)
    assert result.get("0_Left") == 1
    assert result.get("0_Right") == None

    # Test other numbers
    for i in range(100):
        random_number_1 = random.randint(-20, 20)
        example["xValue"] = random_number_1
        example["yValue"] = None
        result = eval.main(example)
        if random_number_1 > 0:
            assert result.get("0_Left") == None
            assert result.get("0_Right") == 1
        else:
            assert result.get("0_Left") == 1
            assert result.get("0_Right") == None

def test_change_sign():
    """Test change sign config"""
    example_file = open(CHANGE_SIGN_PATH, "r").read()
    example = json.loads(example_file)

    for i in range(100):
        random_number_1 = random.randint(-20, 20)
        example["xValue"] = random_number_1
        example["yValue"] = None
        result = eval.main(example)
        assert result.get("0_Out") == random_number_1 * -1
    
def test_minus():
    """Test minus operation"""
    example_file = open(MINUS_PATH, "r").read()
    example = json.loads(example_file)

    for i in range(100):
        random_number_1 = random.randint(-20, 20)
        random_number_2 = random.randint(-20, 20)
        example["xValue"] = random_number_1
        example["yValue"] = random_number_2
        result = eval.main(example)
        assert result.get("0_Out") == random_number_1 - random_number_2


def test_equal_operation():
    """Test equal operation"""
    example_file = open(EQUAL_PATH, "r").read()
    example = json.loads(example_file)

    for i in range(100):
        random_number_1 = random.randint(-20, 20)
        random_number_2 = random.randint(-20, 20)
        example["xValue"] = random_number_1
        example["yValue"] = random_number_2
        result = eval.main(example)
        if random_number_1 == random_number_2:
            assert result.get("0_Left") == None
            assert result.get("0_Right") == 1
        else:
            assert result.get("0_Left") == 1
            assert result.get("0_Right") == None


def test_is_larger():
    """Test isLarger operation
    Note: If they are equal, it will return false
    """
    example_file = open(IS_LARGER_Path, "r").read()
    example = json.loads(example_file)

    for i in range(100):
        random_number_1 = random.randint(-20, 20)
        random_number_2 = random.randint(-20, 20)
        example["xValue"] = random_number_1
        example["yValue"] = random_number_2
        result = eval.main(example)
        if random_number_1 > random_number_2:
            assert result.get("0_Left") == None
            assert result.get("0_Right") == 1
        else:
            assert result.get("0_Left") == 1
            assert result.get("0_Right") == None

def test_multiply():
    """Test multiply operation"""
    example_file = open(MULTIPLY_PATH, "r").read()
    example = json.loads(example_file)

    for i in range(100):
        random_number_1 = random.randint(-20, 20)
        random_number_2 = random.randint(-20, 20)
        example["xValue"] = random_number_1
        example["yValue"] = random_number_2
        result = eval.main(example)
        assert result.get("0_Out") == random_number_1 * random_number_2