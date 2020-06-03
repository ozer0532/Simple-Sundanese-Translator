# Kode program string matching dari Tucil 4 - String Matcher

import os, re
from typing import Callable, Dict
from re import Match

# Load the dictionary based on a file name
# Accepts a file_name as a string
# Returns a string -> string dictionary with a source -> translated relation
# Remove leading & trailing whitespaces: https://www.journaldev.com/23763/python-remove-spaces-from-string
def loadDictionary(file_name : str, reverse : bool) -> Dict[str, str]:
    dictionary = {}
    with open(file_name, 'r') as f:
        for line in f.readlines():
            pair = line.split('=')
            pair[0] = pair[0].strip()
            pair[1] = pair[1].strip()
            if (pair[0] not in dictionary) or reverse:     # Take the first occurence only
                dictionary[pair[0]] = pair[1]
    return dictionary

# Pencocok string dengan pattern menggunakan algoritma KMP
# Menerima sebuah string yang ingin dicocokkan dengan pattern yang dimasukkan
# Mengembalikan posisi mulai pattern pada string, atau -1 bila pattern tidak ditemukan
# Berdasarkan slide materi kuliah pada web Pak Rinaldi
def kmp_matcher(string : str, pattern : str) -> int:
    # Get the KMP Border Function
    b = []
    for j in range(len(pattern) - 1):
        end = j + 1
        front_iterator = 1
        back_iterator = j
        b_k = 0
        while (back_iterator > 0):
            if pattern[0:front_iterator] == pattern[back_iterator:end]:
                b_k = front_iterator
            front_iterator += 1 
            back_iterator -= 1
        b.append(b_k)
    
    # Match the string with pattern
    i = 0
    j = 0
    m = len(pattern)
    n = len(string)
    while (i < n):
        if (string[i] == pattern[j]):
            i += 1
            j += 1
            if (j == m):
                return i - j
        else:
            if j == 0:
                j = 0
                i += 1
            else:
                j = b[j-1]
    return -1

# Pencocok string dengan pattern menggunakan algoritma Boyer-Moore
# Menerima sebuah string yang ingin dicocokkan dengan pattern yang dimasukkan
# Mengembalikan posisi mulai pattern pada string, atau -1 bila pattern tidak ditemukan
# Berdasarkan slide materi kuliah pada web Pak Rinaldi
def bm_matcher(string : str, pattern : str) -> int:
    # Get the Last Occurence Function
    L = {}
    for i in range(len(pattern)):
        L[pattern[i]] = i
    
    # Match the string with pattern
    m = len(pattern)
    n = len(string)
    i = m - 1
    j = i
    while (i < n):
        if (string[i] == pattern[j]):
            i -= 1
            j -= 1
            if (j < 0):
                return i + 1
        else:
            x = string[i]
            lo = L.get(x, -1)
            if lo < j:      # Case 1 & 3
                i += m - lo - 1
                j = m - 1
            else:           # Case 2
                i += m - j
                j = m - 1

    return -1

# Pencocok string dengan regex menggunakan algoritma KMP
# Menerima sebuah string yang ingin dicocokkan dengan pattern (sebuah regex) yang dimasukkan
# Mengembalikan posisi mulai pattern pada string, atau -1 bila pattern tidak ditemukan
# Berdasarkan slide materi kuliah pada web Pak Rinaldi
def regex_matcher(string : str, pattern : str) -> int:
    result = re.search(pattern, string)
    if result != None:
        return result.span()[0]
    else:
        return -1

def translate(source : str, matcher : Callable[[str, str], int], dictionary : Dict[str, str], remove_particle : bool, add_particle : bool) -> str:
    converted_string = []
    source = source.lstrip()
    # Conversion process
    while (source != ""):
        translatable = False
        for key in dictionary.keys():
            if matcher(source.lower(), key) == 0:
                # Check if this is a word / several words
                original = source[:len(key)]
                if len(source) > len(original) and source[len(original)].isalpha():
                    continue
                translatable = True
                break
        if translatable:
            translation = dictionary[key]
        else:
            original = source.split()[0]
            translation = original
        converted_string.append(translation)
        source = source.replace(original, "", 1).lstrip()
    

    # Remove particles
    if remove_particle:
        for entry in converted_string:
            if entry in ["teh", "mah", "tea", "atuh"]:
                converted_string.remove(entry)

    # Add particles
    if add_particle:
        for index in range(len(converted_string)):
            entry = converted_string[index]
            if entry in ["saha"]:
                converted_string[index] = "teh " + entry

    # Capitalize first letter in sentence
    capitalize = True
    for index in range(len(converted_string)):
        if capitalize:
            converted_string[index] = converted_string[index].capitalize()
            capitalize = False
        if converted_string[index] in ".?!":
            capitalize = True

    # Bind puctuation marks
    fixed_punctuation = []
    bind_with_previous = False
    for entry in converted_string:
        no_binding = True
        if entry in ".,?!)/%":
            fixed_punctuation[-1] += entry
            no_binding = False
        elif bind_with_previous:
            fixed_punctuation[-1] += entry
            bind_with_previous = False
            no_binding = False
        if entry in "/($":
            bind_with_previous = True
            no_binding = False
        if no_binding:
            fixed_punctuation.append(entry)


    # Concatenation process
    result = " ".join(fixed_punctuation)
    return result
