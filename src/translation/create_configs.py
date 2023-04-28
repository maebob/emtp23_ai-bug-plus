"""
This script is designed to translate the configuration data of a specific
application by updating the format of bug objects within the data. The
translation process involves reading the pre_translation configuration data
from a file, applying the translation rules defined by several functions, and
saving the translated configuration data to a new file.

Functions included in this script:

extract_ids: Extracts all the ids from the bugs, including nested bugs.
update_bugs: Updates the ids of bugs and their edges based on the id_dict.
update_edges: Updates the 'from_' and 'to' bugIds of edges based on the id_dict.
translate_bug: Translates the bug to a new format using a predefined template.
translate: Translates the input dictionary to a new format with updated bugs.
main: Main function to perform the translation and save the output.
Usage:

To execute the script, simply run it from the command line:
python translate_configurations.py

The script reads the pre_translation data from a file specified by the
TRANSLATION_PATH constant and saves the translated data to a new file in the
"Configurations" folder.
"""

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
    """
    Extract all the ids from the bugs.
    This function traverses through the list of bugs and recursively extracts
    the ids of all bugs, including those nested within other bugs.

    Argummets:
        bugs (list): A list of dictionaries containing bugs with their
                    respective ids and nested bugs.

    Returns:
        list: A list of extracted ids from the bugs.

    Example:
        bugs = [
            {"id": 1, "bugs": [{"id": 2, "bugs": []}]},
            {"id": 3, "bugs": [{"id": 4, "bugs": []}, {"id": 5, "bugs": []}]},
        ]
        result = extract_ids(bugs)
        print(result)  # Output: [1, 2, 3, 4, 5]
    """

    ids = []  # Initialize an empty list to store the extracted ids

    # Iterate through each bug in the bugs list
    for bug in bugs:
        # Append the id of the current bug to the ids list
        ids.append(bug.get("id"))

        # Recursively extract ids from the nested bugs and extend the ids list with the extracted ids
        ids.extend(extract_ids(bug.get("bugs")))

    return ids  # Return the list of extracted ids


def update_bugs(bugs: list, id_dict: dict) -> list:
    """
    Update the ids of bugs and their edges based on the id_dict.
    This function iterates through the list of bugs and recursively updates
    the ids of the bugs and their edges using the provided id_dict.

    Argummets:
        bugs (list): A list of dictionaries containing bugs with their
                    respective ids, edges, and nested bugs.
        id_dict (dict): A dictionary mapping the old ids to the new ids.

    Returns:
        list: A list of updated bugs with their ids and edges.

    Example:
        bugs = [
            {"id": 1, "edges": [2], "bugs": [{"id": 2, "edges": [], "bugs": []}]},
            {"id": 3, "edges": [4, 5], "bugs": [{"id": 4, "edges": [], "bugs": []}, {"id": 5, "edges": [], "bugs": []}]},
        ]
        id_dict = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
        result = update_bugs(bugs, id_dict)
        print(result)  # Output: [{"id": 10, "edges": [20], "bugs": [{"id": 20, "edges": [], "bugs": []}]}, {"id": 30, "edges": [40, 50], "bugs": [{"id": 40, "edges": [], "bugs": []}, {"id": 50, "edges": [], "bugs": []}]}]
    """
    # Iterate through each bug in the bugs list
    for bug in bugs:
        # Update the id of the current bug using the id_dict
        bug["id"] = id_dict.get(bug["id"])

        # Update the edges of the current bug using the id_dict
        bug["edges"] = update_edges(bug.get("edges"), id_dict)

        # Recursively update the ids of the nested bugs and their edges
        bug["bugs"] = update_bugs(bug["bugs"], id_dict)

    return bugs  # Return the list of updated bugs


def update_edges(edges: list, id_dict: dict) -> list:
    """
    Update the 'from_' and 'to' bugIds of edges based on the id_dict.
    This function iterates through the list of edges and updates the 'from_'
    and 'to' bugIds using the provided id_dict.

    Argummets:
        edges (list): A list of dictionaries containing edges with their
                    'from_' and 'to' bugIds.
        id_dict (dict): A dictionary mapping the old ids to the new ids.

    Returns:
        list: A list of updated edges with their 'from_' and 'to' bugIds.

    Example:
        edges = [
            {"from_": {"bugId": 1}, "to": {"bugId": 2}},
            {"from_": {"bugId": 2}, "to": {"bugId": 3}},
        ]
        id_dict = {1: 10, 2: 20, 3: 30}
        result = update_edges(edges, id_dict)
        print(result)  # Output: [{"from_": {"bugId": 10}, "to": {"bugId": 20}}, {"from_": {"bugId": 20}, "to": {"bugId": 30}}]
    """
    # Iterate through each edge in the edges list
    for edge in edges:
        # Update the 'from_' bugId of the current edge using the id_dict
        edge["from_"]["bugId"] = id_dict.get(edge["from_"].get("bugId"))

        # Update the 'to' bugId of the current edge using the id_dict
        edge["to"]["bugId"] = id_dict.get(edge["to"].get("bugId"))

    return edges  # Return the list of updated edges


def translate_bug(bug: dict) -> dict:
    """
    Translate the bug to a new format using a predefined template.
    This function takes a bug dictionary and translates it into a new format
    using a predefined template based on the bug's 'Type'. The template is
    updated with the bug's id and random unique ids for nested bugs and edges.

    Argummets:
        bug (dict): A dictionary containing the bug with its 'Type', 'id', and
                    other properties.

    Returns:
        dict: A dictionary containing the translated bug in the new format.

    Example:
        bug = {"Type": "A", "id": 1}
        result = translate_bug(bug)
        print(result)  # Output: {"id": 1, "bugs": [...], "edges": [...], "Type": "A"}
    """
    # Get the bug type
    bug_template_path = TRANSLATION_DICT.get(bug.get("Type"))
    bug_template_file = open(bug_template_path, "r").read()
    bug_template = json.loads(bug_template_file)

    # Get all ID's in the template
    id_dict = {}
    id_dict[bug_template["id"]] = bug.get("id")

    # Set the id of the bug
    bug_template["id"] = bug.get("id")

    # Add unique ids to a set
    unique_ids = extract_ids(bug_template.get("bugs"))
    unique_ids = set(unique_ids)
    for id in unique_ids:
        id_dict[id] = random.randint(1_000, 1_000_000_000_000_000)

    # Replace all the ids in the template
    bug_template["bugs"] = update_bugs(bug_template.get("bugs"), id_dict)
    bug_template["edges"] = update_edges(bug_template.get("edges"), id_dict)

    # Set the 'Type' of the bug
    bug_template["Type"] = bug.get("Type")

    return bug_template  # Return the translated bug


def translate(pre_translation: dict) -> dict:
    """
    Translate the input dictionary to a new format with updated bugs.
    This function takes a pre_translation dictionary and translates the bugs
    within it to a new format using the 'translate_bug' function, except for
    bugs of type 'plus' which remain unchanged. The translated bugs are added
    back to the pre_translation dictionary.

    Argummets:
        pre_translation (dict): A dictionary containing the original data
                                with a list of bugs.

    Returns:
        dict: A dictionary containing the translated data with updated bugs.

    Example:
        pre_translation = {
            "bugs": [
                {"Type": "A", "id": 1},
                {"Type": "plus", "id": 2},
            ]
        }
        result = translate(pre_translation)
        print(result)  # Output: {"bugs": [{"id": 1, "bugs": [...], "edges": [...], "Type": "A"}, {"Type": "plus", "id": 2}]}
    """

    # Only the bugs need to be translated
    bugs = pre_translation.get("bugs")
    translated_bugs = []
    for bug in bugs:
        if bug.get("Type") == "plus":
            translated_bugs.append(bug)
            continue

        translated_bugs.append(translate_bug(bug))

    # Add the translated bugs to the pre_translation dictionary
    pre_translation["bugs"] = translated_bugs
    return pre_translation  # Return the translated dictionary


def main():
    """
    Main function to perform the translation and save the output.
    This function loads the pre_translation data from a file, translates it
    using the 'translate' function, and saves the translated data to a new file.
    """

    # Load the pre_translation data from a file
    pre_translation_file = open(TRANSLATION_PATH, "r").read()
    pre_translation = json.loads(pre_translation_file)

    # Translate the pre_translation data
    translated = translate(pre_translation)

    # Save the translated data to a new file
    with open("Configurations/multiply.json", "w") as f:
        json.dump(translated, f, indent=4)


if __name__ == "__main__":
    main()
