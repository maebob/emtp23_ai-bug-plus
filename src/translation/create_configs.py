import json
import random

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

# Translate file
TRANSLATION_PATH = "Configurations/multiplyPre.json"


TRANSLATION_DICT = {
    "incrementor": INCREMENTOR_PATH,
    "decrementer": DECREMENTOR_PATH,
    "isZero": IS_ZERO_PATH,
    "incrementIterator": INCREMENTOR_ITERATOR_PATH,
    "decrementIterator": DECREMENTOR_ITERATOR_PATH,
    "assignment": ASIGNMENT,
    "nestedIncrementor": NESTED_INCREMENTOR_PATH,
    "pseudoParallel": PSEUDO_PARALLEL,
    "isPositive": IS_POSITIVE_PATH,
    "changeSign": CHANGE_SIGN_PATH,
    "minus": MINUS_PATH,
    "equal": EQUAL_PATH
}


def extract_ids(bugs: list) -> list:
    """Extract all the ids from the bugs."""
    ids = []
    for bug in bugs:
        ids.append(bug.get("id"))
        ids.extend(extract_ids(bug.get("bugs")))
    return ids


def update_bugs(bugs: list, id_dict: dict) -> list:
    """Update the bugs."""
    for bug in bugs:
        bug["id"] = id_dict.get(bug["id"])
        bug["edges"] = update_edges(bug.get("edges"), id_dict)
        bug["bugs"] = update_bugs(bug["bugs"], id_dict)
    return bugs


def update_edges(edges: list, id_dict: dict) -> list:
    """Update the edges."""
    for edge in edges:
        edge["from_"]["bugId"] = id_dict.get(edge["from_"].get("bugId"))
        edge["to"]["bugId"] = id_dict.get(edge["to"].get("bugId"))
    return edges


def translate_bug(bug: dict) -> dict:
    """Translate the bug."""
    # Get the bug type
    bug_template_path = TRANSLATION_DICT.get(bug.get("Type"))
    bug_template_file = open(bug_template_path, "r").read()
    bug_template = json.loads(bug_template_file)

    # Get all ID's in the template
    id_dict = {}
    id_dict[bug_template["id"]] = bug.get("id")

    # Set the if of the bug
    bug_template["id"] = bug.get("id")

    # add to set
    unique_ids = extract_ids(bug_template.get("bugs"))
    unique_ids = set(unique_ids)
    for id in unique_ids:
        id_dict[id] = random.randint(1_000, 1_000_000_000_000_000)

    # Replace all the ids in the template
    bug_template["bugs"] = update_bugs(bug_template.get("bugs"), id_dict)
    bug_template["edges"] = update_edges(bug_template.get("edges"), id_dict)
    #TODO this should be extended to the actual type
    bug_template["Type"] = bug.get("Type")
    return bug_template


def translate(pre_translation: dict) -> dict:
    """Translate the pre_translation to a post translation."""

    # Only the bugs need to be translated
    bugs = pre_translation.get("bugs")
    translated_bugs = []
    for bug in bugs:
        if bug.get("Type") == "plus":
            translated_bugs.append(bug)
            continue

        translated_bugs.append(translate_bug(bug))

    # Add the translated bugs to the pre translation
    pre_translation["bugs"] = translated_bugs
    return pre_translation


def main():
    """Main function."""

    # load the pre translation
    pre_translation_file = open(TRANSLATION_PATH, "r").read()
    pre_translation = json.loads(pre_translation_file)
    translated = translate(pre_translation)
    # Save the translated file
    with open("Configurations/multiply.json", "w") as f:
        json.dump(translated, f, indent=4)


if __name__ == "__main__":
    main()