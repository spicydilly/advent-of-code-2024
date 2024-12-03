import os


def read_input(day, use_example=False, part=0) -> str:
    """
    Read the input for the given day

    Args:
        day (int): the day to read the input for
        use_example (bool, optional):
            whether the input is an example or not
        part (int, optional): the part of the challenge
            0 means the example is shared

    Returns:
        str: the input for the given day
    """
    # Determine the file name
    file_name = f"day{day:02}{'-example' if use_example else ''}"
    if part != 0:
        file_name += f"-p{part}"
    file_name += ".txt"
    file_path = os.path.join("inputs", file_name)

    # check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Could not find the input file for day {day} - {file_name}"
        )

    with open(file_path, "r") as f:
        return f.read()
