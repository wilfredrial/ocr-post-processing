from difflib import SequenceMatcher


# This function is from https://rosettacode.org/wiki/Levenshtein_distance#Python
def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]


def similar(a, b):
    return round(SequenceMatcher(None, a, b).ratio(), 3)


def closestWords(word):
    megaDict = "../../Dictionaries/omni_dict.txt"
    specialDict = "../../Dictionaries/rareDict.txt"
    dList = [megaDict, specialDict]
    threeClosest = []
    for dictionary in dList:
        with open(dictionary, 'r', encoding="utf-8") as fh:
            for entry in fh:
                if len(entry) > len(word)+3 or len(entry) < len(word)-3:
                    continue
                entry = entry.replace("\n", "")
                ratio = similar(word, entry)
                dist = levenshteinDistance(word, entry)
                if dist and ratio:
                    if ratio >= .6 and dist <= 5:
                        threeClosest.append((entry, ratio, dist))
                else:
                    ratio = similar(word.lower(), entry)
                    dist = levenshteinDistance(word.lower(), entry)
                    if ratio >= .6 and dist <= 5:
                        threeClosest.append((entry, ratio, dist))
    threeClosest = set(threeClosest)
    threeClosest = list(threeClosest)
    threeClosest.sort(key=lambda tup: tup[2], reverse=True)
    for tuple in threeClosest:
        print(tuple)
    del threeClosest[0:-3]
    return threeClosest
