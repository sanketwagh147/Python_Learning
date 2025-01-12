from collections import namedtuple

# Define named tuples
A4 = namedtuple("A4", ["left", "right"])  # Represents an A4 sheet with two pages
A3 = namedtuple(
    "A3", ["front", "back"]
)  # Represents an A3 sheet with front and back sides


def generate_booklet_sequence_as_named_tuples(total_pages, start_page=2, end_page=2):
    # Adjust the range of pages based on start_page and end_page
    pages_to_include = list(range(start_page + 1, total_pages - end_page + 1))

    # Ensure pages_to_include is a multiple of 4, keeping the last page at the end
    last_page = total_pages
    while len(pages_to_include) % 4 != 0:
        pages_to_include.append(None)  # Add blank pages (None)

    # Place the last page explicitly at the end
    if last_page not in pages_to_include:
        pages_to_include[-1] = last_page

    sequence = []
    left_index = 0
    right_index = len(pages_to_include) - 1

    while left_index < right_index:
        # Front side of A3: Outer-right and Outer-left pages
        front = A4(
            left=(
                pages_to_include[right_index]
                if pages_to_include[right_index] is not None
                else "Blank"
            ),
            right=(
                pages_to_include[left_index]
                if pages_to_include[left_index] is not None
                else "Blank"
            ),
        )
        left_index += 1
        right_index -= 1

        # Back side of A3: Inner-left and Inner-right pages
        if left_index < right_index:
            back = A4(
                left=(
                    pages_to_include[left_index]
                    if pages_to_include[left_index] is not None
                    else "Blank"
                ),
                right=(
                    pages_to_include[right_index]
                    if pages_to_include[right_index] is not None
                    else "Blank"
                ),
            )
            left_index += 1
            right_index -= 1
        else:
            back = None  # For the last page, back might not exist

        sequence.append(A3(front=front, back=back))

    return sequence


# Example usage
total_pages = int(input("Enter the total number of pages: "))
start_page = int(
    input("Enter the number of pages to skip at the start (default 2): ") or 2
)
end_page = int(input("Enter the number of pages to skip at the end (default 2): ") or 2)

booklet_sequence = generate_booklet_sequence_as_named_tuples(
    total_pages, start_page, end_page
)

# Print the result
for idx, a3_page in enumerate(booklet_sequence, start=1):
    print(f"A3 Page {idx}:")
    print(f"  Front: {a3_page.front}")
    if a3_page.back:
        print(f"  Back:  {a3_page.back}")
