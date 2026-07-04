#################
#   CONSTANTS   #
#################

VALUE_MULTIPLIER = 2
VALUE_OFFSET = 1
SAMPLE_VALUES = [3, 7, 11, 19]


#################
#   FUNCTIONS   #
#################


def transform(values: list[int]) -> list[int]:
    """Transform each input value with the lesson formula"""
    transformed_values: list[int] = []

    # Transform each value independently so output order matches input order
    for value in values:
        transformed_values.append(value * VALUE_MULTIPLIER + VALUE_OFFSET)

    return transformed_values


def main() -> None:
    """Print the transformed sample values"""
    print(transform(SAMPLE_VALUES))


if __name__ == "__main__":
    main()
