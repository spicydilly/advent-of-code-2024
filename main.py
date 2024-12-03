from utils.read_input import read_input
import importlib
import argparse


def main(day: int, use_example: bool):
    """
    Run the solution for a specific day of Advent of Code 2024

    Args:
        day (int): The day of the challenge
        use_example (bool): Use the example input file
    """
    try:
        # import the solution module for the passed day
        module_name = f"solutions.day{day:02}"
        module = importlib.import_module(module_name)

        # Read the input data
        input_data = read_input(day=day, use_example=use_example)

        # Create instance of Solution class
        solution = module.Solution(input_data)

        # Solve Part 1
        if hasattr(solution, "part_1"):
            result_part_1 = solution.part_1()
            print(f"Day {day:02} Part 1: {result_part_1}")
        else:
            print(f"Day {day:02} Part 1: Not implemented.")

        # Solve Part 2
        if hasattr(solution, "part_2"):
            result_part_2 = solution.part_2()
            print(f"Day {day:02} Part 2: {result_part_2}")
        else:
            print(f"Day {day:02} Part 2: Not implemented.")

    except ModuleNotFoundError:
        print(f"Solution for Day {day:02} not found.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions.")
    parser.add_argument("day", type=int, help="The day of the challenge (1-25).")
    parser.add_argument(
        "-e",
        "--use-example",
        action="store_true",
        help="Use the example input file instead of the actual input.",
    )
    args = parser.parse_args()

    # Run the main function
    main(day=args.day, use_example=args.use_example)
