def generate_booklet_sequence(total_pages):
    # Ensure total pages is a multiple of 4
    if total_pages % 4 != 0:
        total_pages += 4 - (total_pages % 4)

    sequence = []
    left, right = 1, total_pages

    while left < right:
        # Add the pair of pages for the booklet
        sequence.append(right)  # Outer-right page
        sequence.append(left)  # Outer-left page
        left += 1
        right -= 1

        if left < right:
            sequence.append(left)  # Inner-left page
            sequence.append(right)  # Inner-right page
            left += 1
            right -= 1

    return sequence


# Example usage:
total_pages = int(input("Enter the total number of pages: "))
sequence = generate_booklet_sequence(total_pages)
print("Booklet print sequence:", sequence)
