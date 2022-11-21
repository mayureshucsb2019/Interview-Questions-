# Given an array of strings strs, group the anagrams together. You can return the answer in any order.
 
# An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, 
# typically using all the original letters exactly once.
 
# Example
 
# Input: strs = ["eat","tea","tan","ate","nat","bat"]
# Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
def compare_maps(map1, map2):
    keys_1 = map1.keys()
    keys_2 = map2.key()
    if len(keys_1) != len(keys_2):
        return False
    for x in keys_1:
        try:
            if map1[x] != map2[x]:
                return False
        except KeyError:
            return False
    return True

def getMapOfWord(word):
    map1 = {}
    for ch in word:
        if map1.get(ch, False):
            map1[ch] +=1
        else:
            map1[ch] = 1
    return map1

def group_anagrams(string_array):
    groups = {} 
    for words in string_array:
        map_word = getMapOfWord(words)
        if len(groups.keys()) == 0:
            groups[words]= [words]
            continue
        for key in groups.keys():
            map_key = getMapOfWord(key)
            if compare_maps(map_key, map_word):
                groups[key].append(words)
    output = []
    for x in groups:
        output.append(groups[x])
    return output


