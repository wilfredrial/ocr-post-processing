import os
import re
import seqTester
import logger
from multiprocessing import Pool
from functools import partial
__author__ = 'William'


# holds information for the log file
dict_fr = logger.Logger()
st_cap = logger.Logger()
dict_err_left = logger.Logger()
contr_err = logger.Logger()
one_w_err = logger.Logger()
merged = logger.Logger()
dict_err_right = logger.Logger()
are_cap = logger.Logger()
fix_sub = logger.Logger()
total_words = logger.Logger()
log_list = [dict_fr,
            st_cap,
            dict_err_left,
            contr_err,
            one_w_err,
            merged,
            dict_err_right,
            are_cap,
            fix_sub,
            total_words]


def loadDictOfErr(p):
    # This fct skips the first line in the file
    d = {}
    with open(p + 'dictErrors.txt', encoding="utf") as f:
        for line in f:
            line_components = re.sub("\t+", "\t", line)
            line_components = re.sub("\n", "", line_components)
            line_components = line_components.split("\t")

            if len(line_components) > 1:
                key = line_components[0]
                value = line_components[1]
                d[key] = value
    return d
path = '../../Dictionaries/'
dictErrors = loadDictOfErr(path)


def atEndofLine(word, curr_line):
    # Tests if the current word is at the end of the line
    if curr_line[-1] == word:
        return 1


def ignorePunct(word):
    # This ought to solve problems where punct at beginning or end of word causes errors
    # temporarily removes these marks for the while it is checked in a dictionary
    clean_word = re.sub("[-,.':;?]+\Z", "", word)
    clean_word = re.sub("\A[-,.':?]+", "", clean_word)
    return clean_word


def inDictF(word):
    # checks if the word is in the french dictionary
    freqDict = "../../Dictionaries/all_words_conversations.txt"
    specialDict = "../../Dictionaries/rareDict.txt"
    allDict = "../../Dictionaries/omni_dict.txt"
    dictList = [freqDict, specialDict, allDict]
    if len(word) > 1:
        word = ignorePunct(word)
    for dictionary in dictList:
        with open(dictionary, 'r', encoding="utf-8") as fh:
            reader = fh.read()
            reader = reader.split()
            for entry in reader:
                # ignore case while comparing
                if word.lower() == entry.lower():
                    return 1
    return 0


def sub_mistake(word, char_err, char_sub):
    word = re.sub(char_err, char_sub, word)
    return word


def fix_substitution(word):
    # attempts some simple substitutions
    # checks the french dictionaries
    temp = sub_mistake(word, "t", "r")
    if inDictF(temp):
        print("%s is in the dictionary" % temp)
        return temp
    temp = sub_mistake(word, 'f', 's')
    if inDictF(temp):
        print("%s is in the dictionary" % temp)
        return temp
    temp = sub_mistake(word, 'lb', 'so')
    if inDictF(temp):
        print("%s is in the dictionary" % temp)
        return temp
    temp = sub_mistake(word, 'e', 'é')
    if inDictF(temp):
        print("%s is in the dictionary" % temp)
        return temp


def startCapital(word):
    if word.istitle():
        return 1


def hasEndPunct(word):
    # checks if the word might need to be joined with another word
    # assumes the word is at the end of a line
    joiner_punct = ["-", "..", ".", ".'", "-.", "'.", ",.", "-z", "...", ":", "..z", "e.s"] # maybe change this to regex
    for mark in joiner_punct:
        if word[-(len(mark)):len(word)] == mark:
            return 1


def hasLetter(word):
    if re.search('[a-zA-Z]', word):
        return 1
    else:
        return 0


def mergeTwoWord(nextLine, word, firstWordNextLine):
    word = re.sub("[-,.':]+\Z", "", word)
    firstWordNextLine = re.sub("\A[-,.':]+", "", firstWordNextLine)
    if nextLine:
        del nextLine[0]
    return word+firstWordNextLine


def isMergeable(word, firstWordNextLine):
    # Assumes word occurs at the end of the line
    # removes non letters from the end of word and start of next word
    # merges the words and checks if it forms a word in the dictionary
    word = re.sub("[-,.':]+\Z", "", word)
    firstWordNextLine = re.sub("\A[-,.':]+", "", firstWordNextLine)
    return inDictF(word+firstWordNextLine)


def mergeWithHyphen(word, firstWordNextLine):
    # removes some potentially erroneous chars from the beginning of firstWordNextLine
    # and from the end of word
    # then merges the two strings
    word = re.sub("[-,.']+\Z", "-", word)
    firstWordNextLine = re.sub("\A[-,.']+", "", firstWordNextLine)
    return word+firstWordNextLine


def areCapital(word, firstWordNextLine):
    if startCapital(word) and startCapital(firstWordNextLine):
        return 1


def corrErrOneW(word):
    # Takes a single word and checks for an easy fix
    # Assumes that the word has already been searched for in the french dictionary
    # Checks in order of list so it MAY introduce erroneous situations
    vowels = "aeiouàâéêëïîôüûù"
    wrong_e = ["ë", "ez", "e.", "es",]
    for seq in wrong_e:
        if seq in word:
            return word.replace(seq, "é")
    wrong_apostrophe = [".", "s", "a"]
    for error in wrong_apostrophe:
        for char in vowels:
            if (error + char) in word:
                charList = list(word)
                charList[1] = "'"
                word = "".join(charList)
                return word
    return word


def generateTrainingSet(word, destination=None):
    twoBestList = seqTester.closestWords(word)
    if len(twoBestList) == 3:
        if destination:
            with open(destination, 'a', encoding="utf8") as fh:
                ratioList = [twoBestList[-1][0], str(twoBestList[-1][1]), twoBestList[-2][0],
                            str(twoBestList[-2][1]), twoBestList[-3][0], str(twoBestList[-3][1])]
                levList = [twoBestList[-1][0], str(twoBestList[-1][2]), twoBestList[-2][0],
                            str(twoBestList[-2][2]), twoBestList[-3][0], str(twoBestList[-3][2])]
                trainingList = [word,] + ratioList + levList
                print(trainingList)
                fh.write("\t".join(trainingList) + "\t\n")
        else:
            with open("../Errors/trainingSet.txt", 'a', encoding="utf8") as fh:
                ratioList = [twoBestList[-1][0], str(twoBestList[-1][1]), twoBestList[-2][0],
                            str(twoBestList[-2][1]), twoBestList[-3][0], str(twoBestList[-3][1])]
                levList = [twoBestList[-1][0], str(twoBestList[-1][2]), twoBestList[-2][0],
                            str(twoBestList[-2][2]), twoBestList[-3][0], str(twoBestList[-3][2])]
                trainingList = [word,] + ratioList + levList
                print(trainingList)
                fh.write("\t".join(trainingList) + "\t\n")
        return trainingList


def inDictError(word, next_line=None, first_word_next_line=None):
    # checks the dictionary of errors for the current word
    # ie, it has been seen in our 36 pages
    # returns the correct word if it is found
    # otherwise, returns false
    if not next_line and not first_word_next_line:
        for key in dictErrors.keys():
            if key == word:
                word = dictErrors[key]
                return word
    else:
        merged = word + " " + first_word_next_line
        for key in dictErrors.keys():
            if key == merged:
                merged = dictErrors[key]
                del next_line[0]
                return merged
    return 0


def inDictErrEOL(nextline, word, firstWordNextLine):
    # checks the dictionary of errors for the current word
    # ie, it has been seen in our 36 pages
    # returns the correct word if it is found
    # otherwise, returns false
    merged = word + " " + firstWordNextLine
    print(merged)
    for key in dictErrors.keys():
        if key == merged:
            merged = dictErrors[key]
            del nextline[0]
            return merged
    return 0


def isOneWordErr(word):
    # checks to see if the word can be fixed with the fct corrErrOneW
    temp = corrErrOneW(word)
    if inDictF(temp):
        return temp
    else:
        return 0


def errWithinWord(word):
    # computes similarity and Levenshtein distance between word and entries in the dictionary
    # returns some of the closest matches
    threeBestWords = generateTrainingSet(word, "../Errors/realErrorsVol2.txt")
    return threeBestWords


def checkContraction(word):
    # **** Potential for error if the initial letter and contraction are both s
    if word == "ns":
        return
    if word[0] == "s" and word[1] == "s":
        print("ERROR in checkContraction()", word)
    vowels = list("aeiouàâéêëïîôüûùy")
    initialLetter = ["c", "d", "j", "l", "m", "n", "qu", "s",]
    contractions = ["'", ".", "?", "s",]
    temp = "empty"
    for char in contractions:
        if char in word[1:len(word)]:
            temp = word.split(char, 1)
            for i in initialLetter:
                if temp[0] == i:
                    for v in vowels:
                        if len(temp[1]) > 1:
                            if temp[1][0] == v:
                                return temp


def contractionErr(word):
    # gets a list with two entries, the contracted word and the word it is connected to
    temp = checkContraction(word)
    if temp:
        if inDictF(temp[1]):
            print("the 2nd part is an actual word")
        return temp[0] + "'" + temp[1]


def leftTree(word, correctLine):
    # This represents the left side of the flowchart
    if inDictF(word):
        correctLine = correctLine + word + " "
        if not log_list[0].get_name():
            log_list[0].set_name("French Dictionary")
        log_list[0].increment_num()
    else:
        if startCapital(word):
            correctLine = correctLine + word + " "
            if not log_list[1].get_name():
                log_list[1].set_name("Start Capital")
            log_list[1].increment_num()
        else:
            temp = inDictError(word)
            if temp:
                correctLine = correctLine + temp + " "
                if not log_list[2].get_name():
                    log_list[2].set_name("Dictionary Error Left")
                log_list[2].increment_num()
            else:
                temp = contractionErr(word)
                if temp:
                    correctLine = correctLine + temp + " "
                    if not log_list[3].get_name():
                        log_list[3].set_name("Contraction Error")
                    log_list[3].increment_num()
                else:
                    temp = fix_substitution(word)
                    if temp:
                        correctLine = correctLine + temp + " "
                        if not log_list[8].get_name():
                            log_list[8].set_name("Substitution Fix")
                        log_list[8].increment_num()
                    else:
                        temp = isOneWordErr(word)
                        if temp:
                            correctLine = correctLine + temp + " "
                            if not log_list[4].get_name():
                                log_list[4].set_name("One Word Error")
                            log_list[4].increment_num()
                        else:
                            print("Error: <err>", word)
                            correctLine = correctLine + "<err>" + word + "</err> "
    return correctLine


def flowchart(currLine, nextLine, firstWordNextLine):
    # represents the flowchart that we came up with
    # checks each word and concatenates it to the line
    # returns the line once every word has been checked
    correctLine = ""
    for word in currLine:
        if not log_list[-1].get_name():
            log_list[-1].set_name("Total words")
        log_list[-1].increment_num()
        if atEndofLine(word, currLine):
            if hasEndPunct(word):
                if isMergeable(word, firstWordNextLine):
                    correctLine = correctLine + mergeTwoWord(nextLine, word, firstWordNextLine) + " "
                    if not log_list[5].get_name():
                        log_list[5].set_name("Merged")
                    log_list[5].increment_num()
                else:
                    temp = inDictErrEOL(nextLine, word, firstWordNextLine)
                    if temp:
                        correctLine = correctLine + temp + " "
                        if not log_list[6].get_name():
                            log_list[6].set_name("Error Dictionary EOL")
                        log_list[6].increment_num()
                    else:
                        if areCapital(word, firstWordNextLine):
                            correctLine = correctLine + mergeWithHyphen(word, firstWordNextLine) + " "
                            if not log_list[7].get_name():
                                log_list[7].set_name("Are Capitals")
                            log_list[7].increment_num()
                        else:
                            correctLine = leftTree(word, correctLine)
            else:
                correctLine = leftTree(word, correctLine)
        else:
            correctLine = leftTree(word, correctLine)
    return correctLine


def prepPage(pageAsList):
    # prepares a page that has already been read into memory for the flowchart
    # removes any blank lines
    # as well as the first line (which is a header)
    # returns the prepared page
    l = ['\n']
    text = [word for word in pageAsList if word not in l]
    lineList = []
    for line in text:
        lineList.append(line.split())
    del lineList[0]
    return lineList


def loadapage(currPage, nextPage=None):
    # once we reach the last line, we read the next line from the following page
    # for line in currPage:
    for lineNo in range(len(currPage)-1, -1, -1):
        if not currPage[lineNo]:
            del currPage[lineNo]
    pageTxt = ""
    if nextPage:
        for lineNo in range(len(nextPage) - 1, -1, -1):
            if not nextPage[lineNo]:
                del nextPage[lineNo]
        print("Current page length: ", len(currPage))
        for lineNo in range(0, len(currPage)):
            currLine = currPage[lineNo]
            if lineNo < len(currPage)-1:
                nextLine = currPage[lineNo+1]
                firstWordNextLine = nextLine[0]
            elif lineNo == len(currPage)-1:
                nextLine = nextPage[0]
                firstWordNextLine = nextPage[0][0]
            pageTxt = pageTxt + flowchart(currLine, nextLine, firstWordNextLine) + "\n"
    else:
        print("Current page length: ", len(currPage))
        for lineNo in range(0, len(currPage)):
            if not currPage[lineNo]:
                del currPage[lineNo]
        for lineNo in range(0, len(currPage)):
            currLine = currPage[lineNo]
            if lineNo < len(currPage)-1:
                nextLine = currPage[lineNo+1]
                print("Following line: ", nextLine)
                firstWordNextLine = nextLine[0]
            pageTxt = pageTxt + flowchart(currLine, nextLine, firstWordNextLine) + "\n"
    return pageTxt


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def postProcess(picked_folder, process_folder, inList):
    out_folder = "../../4_Output_Final_Text/" + picked_folder
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    info("function postProcess")
    for i, file in enumerate(inList):
        print("this is the current page", inList[i])
        path = process_folder + "/" + inList[i]
        with open(path, 'r', encoding="utf8") as fOpen:
            currPage = fOpen.readlines()
            for line in currPage:
                print(line)
            currPage = prepPage(currPage)
        if i == len(inList) - 1:  # at the last page in the file
            pageTxt = loadapage(currPage)
        else:
            path = process_folder + "/" + inList[i + 1]
            with open(path, 'r', encoding="utf8") as fOpen:
                nextPage = fOpen.readlines()
            nextPage = prepPage(nextPage)
            pageTxt = loadapage(currPage, nextPage)
        print("")
        outPath = out_folder + "/" + file
        with open(outPath, 'w', encoding="utf-8") as of:
            of.write(pageTxt)
    log_path = "../Log/" + picked_folder + ".txt"
    with open(log_path, 'w', encoding='utf-8') as f_log:
        correct_word_count = 0
        for i, log in enumerate(log_list):
            if i < len(log_list) - 1:
                correct_word_count += log_list[i].get_count()
            if log_list[i].name:
                f_log.write("\n")
                f_log.write("=" * 50)
                log_list[i].display_name()
                f_log.write("\n" + log_list[i].get_name())
                f_log.write("\nWord count = " + str(log_list[i].get_count()))
        f_log.write("\n==================================================\n")
        f_log.write("Total correct words\n")
        f_log.write(str(correct_word_count))


if __name__ == "__main__":
    info("main title")
    path = "../../3_Output_OCR/"
    dirs = os.listdir(path)
    for file in dirs:
        print(file)
    chosen_folder = input("Which folder of tiffs would you like to process? ")
    directory = path + chosen_folder
    input_file_list = os.listdir(directory)
    func = partial(postProcess, chosen_folder, directory)
    with Pool(processes=os.cpu_count()) as my_pool:
        my_pool.map(func, [input_file_list])
