"""
WAP that outputs all posable strings formed by combinations c,a,t,d,o and g only once
"""

import itertools

from icecream import ic

# ic.disable()


def string_combination_itertools(seq: list):
    return list(itertools.permutations(seq))


def string_combination():
    chars = ["c", "a", "t", "d", "o", "g"]

    combo = []

    for each in chars:
        temp = "".join(chars)
        combo.append(temp)


def helper(string, string_start_index, prefix):

    start_till_index_i = string[:string_start_index]
    index_plus_1_till_end = string[1 + string_start_index :]

    ic(start_till_index_i)
    ic(index_plus_1_till_end)

    remaining = start_till_index_i + index_plus_1_till_end

    ic(remaining)
    # ic("recursion".center(100,"-"))
    new_prefix = prefix + string[string_start_index]
    ic(new_prefix)
    return remaining, new_prefix


combi = []


def string_permutation(
    string: str,
    prefix: str = "",
):
    if len(string) == 0:
        combi.append(prefix)

    #
    for i in range(len(string)):
        remaining, new_prefix = helper(string, string_start_index=i, prefix=prefix)
        ic("Recursion".center(20, "-"))
        string_permutation(remaining, new_prefix)
        # when there are no chrs remain it will return new prefix


def iterative_permute(st: str):
    li = list(st)  # Convert string to list for easier manipulation
    length_of_str = len(li)
    stack = [(0, li)]  # Stack to keep track of the current state
    # ic(stack)

    # count = 0
    while stack:
        # if count == 1:
        # break
        # count += 1
        start_index, current_combination = stack.pop()
        ic(current_combination)
        ic(length_of_str)
        if start_index == length_of_str:
            ic("".join(current_combination))
        else:
            for chr in range(start_index, length_of_str):
                # ic(start_index)
                ic(chr)
                ic("for loop".center(10, "-"))
                # ic(length_of_str)
                new_combination = current_combination[:]
                temp = new_combination[start_index]
                ic(temp)

                new_combination[start_index] = new_combination[chr]
                ic(new_combination[start_index])

                new_combination[chr] = temp
                ic(new_combination[chr])
                # new_combination[start_index], new_combination[chr] = (
                #     new_combination[chr],
                #     new_combination[start_index],
                # )
                ic(new_combination)
                stack.append((start_index + 1, new_combination))
            print(stack)
            ic("STACK".center(100, "-"))


# Letters to use
letters = "cat"

# Generate and print permutations
# iterative_permute(letters)

""" Approach 2, use list indices"""


def recursion_indices(array, first_idx, second_idx):
    if first_idx == len(array):
        print("".join(list(map(str, array))), end=", ")
        return

    else:
        ic(array)
        for i in range(first_idx, len(array)):
            array[first_idx], array[i] = array[i], array[first_idx]
            recursion_indices(array, first_idx + 1, second_idx)
            array[first_idx], array[i] = array[i], array[first_idx]


def all_combos_v2(array):
    array = list(array)
    first_idx = 0
    second_idx = len(array)
    recursion_indices(array, first_idx, second_idx)
    return


print("\n\nApproach 2")


if __name__ == "__main__":
    # li = ["c", "a", "t", "d", "o", "g"]
    # li = ["c", "a", "t", "s", "e"]
    li = ["c", "a", "t"]
    # ic(string_combination_itertools(["c", "a", "t", "d", "o", "g"]))
    # ic(string_permutation("".join(li)))
    # ic(combi)
    ic(all_combos_v2("cat"))
    # ic(iterative_permute("cat"))
