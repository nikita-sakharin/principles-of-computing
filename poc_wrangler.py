"""
Student code for Word Wrangler game
"""
import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    for element in list1:
        if not result or result[-1] != element:
            result.append(element)
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    index1, index2 = 0, 0
    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] < list2[index2]:
            index1 += 1
        elif list1[index1] > list2[index2]:
            index2 += 1
        else:
            result.append(list1[index1])
            index1 += 1
            index2 += 1
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    result = []
    index1, index2 = 0, 0
    while index1 < len(list1) or index2 < len(list2):
        if index2 >= len(list2) or (index1 < len(list1) and list1[index1] < list2[index2]):
            result.append(list1[index1])
            index1 += 1
        else:
            result.append(list2[index2])
            index2 += 1
    return result

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    list_len = len(list1)
    if list_len < 2:
        return list1
    left, right = list1[: list_len / 2], list1[list_len / 2 :]
    return merge(merge_sort(left), merge_sort(right))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if not len(word):
        return ['']
    first, rest = word[0], word[1 :]
    rest_strings = gen_all_strings(rest)
    result = []
    for string in rest_strings:
        for index in xrange(len(string) + 1):
            result.append(string[: index] + first + string[index :])
    rest_strings.extend(result)
    return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    with open(filename, 'rt', encoding='UTF-8') as file:
        return file.read().splitlines()

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

run()
