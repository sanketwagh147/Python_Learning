"""Leet code 15 3 sum"""


class Solution:

    def threeSum(self, nums):

        nums.sort()
        n = len(nums)
        result = []

        for i in range(n):

            # since it is sorted arr if the val is gt than 0 it cannot reduce it to 0
            if nums[i] > 0:
                break
            # check if last i and current i were not same
            elif i > 0 and nums[i] == nums[i - 1]:
                continue

            low, high = i + 1, n - 1

            while low < high:
                sum_ = nums[i] + nums[low] + nums[high]

                if sum_ == 0:
                    result.append([nums[i], nums[low], nums[high]])
                    low = low + 1
                    high = high - 1

                    # bound check and skip if last iteration yields a same value of low
                    while low < high and nums[low] == nums[low - 1]:
                        low += 1

                    # bound check and skip if last iteration yields a same value of high
                    while low < high and nums[high] == nums[high + 1]:
                        high -= 1
                # if sum is less increase low
                elif sum_ < 0:
                    low += 1
                else:
                    high -= 1

        return result

    # def threeSum(self,nums):
    #     # Sort the list
    #     nums.sort()
    #     n = len(nums)
    #     res = []

    #     for i in range(n - 2):
    #         if i > 0 and nums[i] == nums[i - 1] ==  # Skip duplicate elements
    #             continue

    #         left, right = i + 1, n - 1
    #         while left < right:
    #             total = nums[i] + nums[left] + nums[right]

    #             if total == 0:
    #                 res.append([nums[i], nums[left], nums[right]])
    #                 left += 1
    #                 right -= 1
    #                 while left < right and nums[left] == nums[left - 1]:  # Skip duplicates
    #                     left += 1
    #                 while left < right and nums[right] == nums[right + 1]:  # Skip duplicates
    #                     right -= 1
    #             elif total < 0:
    #                 left += 1
    #             else:
    #                 right -= 1

    #     return res

    # def threeSum(self,nums):
    #     n = len(nums)
    #     res = set()  # Using a set to store unique triplets

    #     for i in range(n - 2):
    #         for j in range(i + 1, n - 1):
    #             for k in range(j + 1, n):
    #                 if nums[i] + nums[j] + nums[k] == 0:
    #                     res.add(tuple(sorted([nums[i], nums[j], nums[k]])))  # Sorting to avoid duplicates

    #     return list(res)  # Convert set to list

    # def threeSum(self, nums: List[int]) -> List[List[int]]:
    #     h = {}
    #     n=  len(nums)

    #     s = set()

    #     for i,num in enumerate(nums):
    #         h[num] = i

    #     for i in range(n):
    #         for j in range(i+1,n):
    #             desired =  -nums[i] - nums[j]

    #             if desired in h and h[desired] != i and h[desired] !=j:
    #                 s.add(tuple(sorted([nums[i],nums[j],desired])))

    #     return list(s)
