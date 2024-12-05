from pathlib import Path
import shutil


def move_file(source_dir: Path, filename: str, dest_dir: Path) -> None:
    """
    Moves a file from source_dir to dest_dir if it exists.

    Args:
        source_dir (Path): Directory where the file is initially located.
        filename (str): Name of the file to move.
        dest_dir (Path): Directory where the file should be moved to.
    """
    source_path = source_dir / filename
    dest_path = dest_dir / filename

    if source_path.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(dest_path))
        print(f"Moved {source_path} to {dest_path}")
    else:
        print(f"{source_path} not found!")


def clean_up(template_dir: Path) -> None:
    """
    Clean up the now-empty template directory.

    Args:
        template_dir (Path): Path to the created template directory.
    """
    if template_dir.exists():
        shutil.rmtree(template_dir)
        print(f"Removed {template_dir}")
    else:
        print(f"{template_dir} not found!")


def move_files() -> None:
    """
    Moves generated files from the template subdirectories to the correct locations.
    """
    day_number = "{{cookiecutter.__day_number}}"
    base_dir = Path.cwd()  # Current directory after generation
    parent_dir = base_dir.parent  # Destination root directory

    # File configurations
    file_mappings = [
        ("solutions", f"day{day_number}.py"),
        ("tests", f"test_day{day_number}.py"),
        ("inputs", f"day{day_number}-example.txt"),
        ("inputs", f"day{day_number}.txt"),
    ]

    # Move files
    for subdir, filename in file_mappings:
        move_file(base_dir / subdir, filename, parent_dir / subdir)

    # Clean up empty subdirectories
    clean_up(base_dir)


if __name__ == "__main__":
    move_files()
