def generate_booklet_sequence_as_lists(total_pages, start_page=2, end_page=2):
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
        front_left = (
            pages_to_include[right_index]
            if pages_to_include[right_index] is not None
            else "Blank"
        )
        front_right = (
            pages_to_include[left_index]
            if pages_to_include[left_index] is not None
            else "Blank"
        )
        left_index += 1
        right_index -= 1

        # Back side of A3: Inner-left and Inner-right pages
        if left_index < right_index:
            back_left = (
                pages_to_include[left_index]
                if pages_to_include[left_index] is not None
                else "Blank"
            )
            back_right = (
                pages_to_include[right_index]
                if pages_to_include[right_index] is not None
                else "Blank"
            )
            left_index += 1
            right_index -= 1
        else:
            back_left = back_right = None  # For the last page, back might not exist

        # Add pages to sequence, keeping them as individual elements
        sequence.append([front_left, front_right])
        if back_left is not None and back_right is not None:
            sequence.append([back_left, back_right])

    return sequence


sequ = generate_booklet_sequence_as_lists(17)
for each in sequ:
    print(each)
