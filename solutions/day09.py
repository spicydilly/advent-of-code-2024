from typing import List, Tuple, Dict


class Solution:
    def __init__(self, input: str):
        self.input = input.strip()

    def part_1(self) -> int:
        compressed_disk_map = self.add_fragmentation(self.input)
        return self.get_checksum(compressed_disk_map)

    def part_2(self) -> int:
        compressed_disk_map = self.move_entire_files(self.input)
        return self.get_checksum(compressed_disk_map)

    @staticmethod
    def flatten_disk_map(disk_map: str) -> Tuple[List[str], Dict[int, int]]:
        """
        Generate the flattend disk map from the disk map

        Args:
            disk_map (str): The disk map to generate the flat disk map from

        Returns:
            Tuple[List[str], Dict[int, int]]: The flat disk map and the dictionary
        """
        flat_map = []
        dict_map = dict()
        file_id = 0

        # Iterate through the disk map
        for i in range(0, len(disk_map), 2):
            file_size = int(disk_map[i])
            free_space = int(disk_map[i + 1]) if i + 1 < len(disk_map) else 0

            # Add file blocks and free spaces
            start = len(flat_map)
            flat_map.extend([file_id] * file_size)
            dict_map[file_id] = (file_size, start, start + file_size - 1)
            flat_map.extend(["."] * free_space)

            file_id += 1

        return flat_map, dict_map

    def add_fragmentation(self, disk_map: str) -> List[int]:
        """
        Add fragmentation to the disk map by moving the files starting from the end, to
        leftmost free space ( removing all gaps )

        Args:
            disk_map (str): The disk map to compress

        Returns:
            List[int]: The compressed disk map
        """
        disk, _ = self.flatten_disk_map(disk_map)
        free_spaces = [i for i, x in enumerate(disk) if x == "."]

        # start at the end of the disk
        for i in range(len(disk) - 1, -1, -1):
            # if there are no more free spaces, break
            if not free_spaces or free_spaces[0] > i:
                break
            # if there is a file, move it to the free space
            if disk[i] != "." and free_spaces[0] < i:
                disk[free_spaces.pop(0)] = disk[i]
                disk[i] = "."

        # Remove all empty spaces
        return [x for x in disk if x != "."]

    @staticmethod
    def get_checksum(disk_map: List[int]) -> int:
        """
        Get the checksum of the disk map, the checksum is the sum of the sum of the
        position the file is in multipled by the file id

        Args:
            disk_map (str): The disk map to get the checksum from

        Returns:
            int: The checksum
        """
        # ignore 0 for time saving on larger inputs
        return sum(file_id * i for i, file_id in enumerate(disk_map))

    def move_entire_files(self, disk_map: str) -> List[int]:
        """
        Move entire files to the leftmost free space, prioritizing highest file IDs.

        Args:
            disk_map (str): The disk map to move the files from.

        Returns:
            List[int]: The disk map with the files moved.
        """
        disk, dict_map = self.flatten_disk_map(disk_map)
        free_spaces = self.get_free_chunks(disk)

        # Sort free spaces by start index
        free_spaces.sort(key=lambda x: x[1][0])

        # Move through files starting at highest index
        for file_id in sorted(dict_map.keys(), reverse=True):
            file_size, start, end = dict_map[file_id]

            # Find the first valid free space that fits the file size
            for i, (chunk_size, (chunk_start, chunk_end)) in enumerate(free_spaces):
                if chunk_size >= file_size and chunk_end < start:
                    # Move the file to the free space
                    disk[chunk_start : chunk_start + file_size] = disk[start : end + 1]
                    # Clear the old file
                    disk[start : end + 1] = ["."] * file_size
                    # Update the affected free space region
                    free_spaces[i] = (
                        chunk_size - file_size,
                        (chunk_start + file_size, chunk_end),
                    )
                    break

        # Replace all empty spaces with 0 for final representation
        return [x if x != "." else 0 for x in disk]

    @staticmethod
    def get_free_chunks(disk_map: List[int]) -> List[Tuple[int, Tuple[int, int]]]:
        """
        Get the free chunks of the disk map

        Args:
            disk_map (str): The disk map to get the free chunks from

        Returns:
            List[int, Tuple[int, int]]: The size of each free chunk, with the
                start and end of the chunk
        """
        free_ranges = []
        start = None

        for i, block in enumerate(disk_map):
            if block == ".":
                if start is None:  # Mark the start of a free chunk
                    start = i
            else:
                if start is not None:  # End of a free chunk
                    free_ranges.append((abs(start - i), (start, i - 1)))
                    start = None

        return free_ranges
