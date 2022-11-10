from typing import Union

Number = Union[int, float, complex]


def find_insert_position(array: list[Number], number: Number) -> int:
    ...


if __name__ == '__main__':
    A: list[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: list[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
