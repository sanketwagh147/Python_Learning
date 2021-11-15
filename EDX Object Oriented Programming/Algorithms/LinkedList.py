#In Python we deal with data structures like lists,
#but we don't talk much about how lists are implemented
#by Python itself.
#
#One way in which lists can be implemented is with what
#is called a Linked List. In a Linked List, a list is
#made of a series of items. Each item contains two
#elements: its own value (node.value), and a pointer to
#where to find the next element in the list
#(node.next_node). So, you can't jump right in to
#"item 7"; you instead have to start with the first
#item and keep getting the next item until you reach the
#seventh item.
#
#Below is some code we've written to implement a
#Linked List. Specifically, this code represents a
#single node in a linked list: a full list is created
#just by chaining nodes like these together. The last
#node in the linked list will point to None as the
#next item; that indicates you've reached the end of
#the linked list.
#
#Write a function called linked_list_search. Your
#linked_list_search function should take two parameters:
#a single linked list node, and a search term. Your
#function should return True if the search term is the
#value of the linked list node or any node after it.
#It should return False if the value is not found in
#the linked list.

class LinkedListNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node
        self.head = None


#Write your function here!
def linked_list_search(itr, a_int):
    # if linked list is empty
        # If key is present in current node, return true
        if(itr.value == a_int):
            return True
        if itr.next_node is None:
          print("Linked list is empty")
          return False
        # Recur for remaining list
        return linked_list_search(itr.next_node, a_int)
    # if a_node.next_node == None:
    #     return False
    # if a_node.value == a_int:
    #     return True
    #
#     current = a_node.next_node
#     while current!= None:
#
#         if current.value == a_int:
#             return True
#
#         current = current.next_node
#     return False
    # if a_int == a_node.value:
    #     return True
    # else:
    #     if a_node == None:
    #         return False
    #     else:
    #         return linked_list_search(a_node.next_node, a_int)


#Below a:re lines of code that create a linked list,
#and then search for two values in that linked list:
#one that is there, one that isn't. If your function
#works, it should print True then False.
# node_7 = LinkedListNode(5)
# node_6 = LinkedListNode(2, node_7)
# node_5 = LinkedListNode(9, node_6)
# node_4 = LinkedListNode(1, node_5)
# node_3 = LinkedListNode(4, node_4)
# node_2 = LinkedListNode(6, node_3)
# root_node = LinkedListNode(7, node_2)
#
# print(linked_list_search(root_node, 9))
# print(linked_list_search(root_node, 3))

root = LinkedListNode(value = 92, next_node = LinkedListNode(value = 1,
                        next_node = LinkedListNode(value = 36, next_node = LinkedListNode(value = 47,
                        next_node = LinkedListNode(value = 88, next_node = LinkedListNode(value = 96,
                        next_node = LinkedListNode(value = 70, next_node = LinkedListNode(value = 97,
                        next_node = LinkedListNode(value = 78, next_node = LinkedListNode(value = 34,
                        next_node = LinkedListNode(value = 59, next_node = LinkedListNode(value = 8))))))))))))

print(linked_list_search(root, 8))

