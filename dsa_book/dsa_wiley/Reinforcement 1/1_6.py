"""
Exercise R-1.6
Exercise R-1.7
s -> str having len(s) = n
k = ?
j = ?   j >= 0
s[k] -n <= k < 0
s[k] == s[j]

Basically find the positive index when negative index is given

"""

from icecream import ic


def get_positive_index(neg_index: int, li: list) -> int:
    """
    # 📌
    To return positive index from negative add the length of the list and vice versa
    """
    return len(li) + neg_index


if __name__ == "__main__":
    sam_l1 = [1, 2, 3, 4, 5]
    sam_l2 = list(range(10, 20, -1))
    neg_index_1 = -1
    pos_index_1 = get_positive_index(-1, sam_l1)
    item_neg_ind = sam_l1[neg_index_1]
    ic(item_neg_ind)

    item_pos_ind = sam_l1[get_positive_index(neg_index_1, sam_l1)]
    ic(item_pos_ind)
    ic(sam_l1[neg_index_1] == sam_l1[get_positive_index(neg_index_1, sam_l1)])
