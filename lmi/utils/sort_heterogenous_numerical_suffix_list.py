import re


def sort_heterogenous_numerical_suffix_list(lst):
    def sorting_key(elem):
        # Use regular expression to extract the prefix and numeric suffix
        match = re.match(r"([A-Za-z]+)(\d+)", elem)
        prefix = match.group(1)
        suffix = int(match.group(2) or 0)
        # Return a tuple that can be used for comparison
        return (prefix, suffix)

    # Sort the list using the custom sorting key
    return sorted(lst, key=sorting_key)
