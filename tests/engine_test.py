import json
import sys

sys.path.append('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/')

from src.engine import eval

def test_incrementor():
    """Test the incrementor function."""
    example_file = open("/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/incrementor.json", "r").read()
    example = json.loads(example_file)
    example["xValue"] = 1
    example["yValue"] = None
    assert eval.main(example).get("0_dataOut") == 2

def test_is_zero():
    """Test the is_zero function."""
    example_file = open("/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/isZero.json", "r").read()
    example = json.loads(example_file)
    example["xValue"] = 0
    example["yValue"] = 0
    result = eval.main(example)
    assert result.get("0_controlOutL") == 0
    assert result.get("0_controlOutR") == 1

def test_is_not_zero():
    """Test the is_not_zero function."""
    example_file = open("/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/BugsPlusEditor/Configurations/isZero.json", "r").read()
    example = json.loads(example_file)
    example["xValue"] = 1
    example["yValue"] = None
    result = eval.main(example)
    assert result.get("0_controlOutL") == 1
    assert result.get("0_controlOutR") == 0