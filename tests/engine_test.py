import json
import sys

sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/')
from src.engine import eval

INCREMENTOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/incrementor.json"
NESTED_INCREMENTOR_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/nestedIncrementor.json"
IS_ZERO_PATH = "/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/isZero.json"


def test_incrementor():
    """Test the incrementor function."""
    example_file = open(INCREMENTOR_PATH, "r").read()
    example = json.loads(example_file)
    example["xValue"] = 1
    example["yValue"] = None
    assert eval.main(example).get("0_dataOut") == 2


def test_is_zero():
    """Test the is_zero function."""
    example_file = open(IS_ZERO_PATH, "r").read()
    example = json.loads(example_file)
    example["xValue"] = 0
    example["yValue"] = 0
    result = eval.main(example)
    assert result.get("0_controlOutL") == 0
    assert result.get("0_controlOutR") == 1


def test_is_not_zero():
    """Test the is_not_zero function."""
    example_file = open(IS_ZERO_PATH, "r").read()
    example = json.loads(example_file)
    example["xValue"] = 1
    example["yValue"] = 0
    result = eval.main(example)
    assert result.get("0_controlOutL") == 1
    assert result.get("0_controlOutR") == 0


def test_nested_incrementor():
    """Test the nested incrementor function."""
    example_file = open("/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/nestedIncrementor.json", "r").read()
    example = json.loads(example_file)
    example["xValue"] = 10
    example["yValue"] = None
    assert eval.main(example).get("0_dataOut") == 11
