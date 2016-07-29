import re
import os
import seqTester
from multiprocessing import Pool
from functools import partial


def generateTrainingSet(word, destination=None):
    threeBestList = seqTester.closestWords(word)
    if len(threeBestList) == 3:
        if destination:
            with open(destination, 'a', encoding="utf-8") as fh:
                ratioList = [threeBestList[-1][0], str(threeBestList[-1][1]), threeBestList[-2][0],
                            str(threeBestList[-2][1]), threeBestList[-3][0], str(threeBestList[-3][1])]
                levList = [threeBestList[-1][0], str(threeBestList[-1][2]), threeBestList[-2][0],
                            str(threeBestList[-2][2]), threeBestList[-3][0], str(threeBestList[-3][2])]
                trainingList = [word] + ratioList + levList
                print(trainingList)
                fh.write("\t".join(trainingList) + "\t\n")
        else:
            ratioList = [threeBestList[-1][0], str(threeBestList[-1][1]), threeBestList[-2][0],
                        str(threeBestList[-2][1]), threeBestList[-3][0], str(threeBestList[-3][1])]
            levList = [threeBestList[-1][0], str(threeBestList[-1][2]), threeBestList[-2][0],
                        str(threeBestList[-2][2]), threeBestList[-3][0], str(threeBestList[-3][2])]
            trainingList = [word] + ratioList + levList
        return trainingList

def make_error():
    lineList = []
    print(dirs)
    for i, file in enumerate(dirs):
        print("Current page we are working on: ", dirs[i])
        with open(directory + "/" + file, 'r', encoding="utf-8") as f1:
            if i == 0:
                with open(output, 'w', encoding="utf-8") as f2:
                    print("***if  Current page: " + file + "***")
                    for line in f1:
                        lineList = line.split()
                        for word in lineList:
                            if word[0] == '<':
                                word = err_tag.sub('', word)
                                errTuple = generateTrainingSet(word)
                                if errTuple:
                                    f2.write("\t".join(errTuple) + "\t\n")
            else:
                with open(output, 'a', encoding='utf-8') as f2:
                    print("***else  Current page: " + file + "***")
                    for line in f1:
                        lineList = line.split()
                        for word in lineList:
                            if word[0] == '<':
                                word = err_tag.sub('', word)
                                errTuple = generateTrainingSet(word)
                                if errTuple:
                                    f2.write("\t".join(errTuple) + "\t\n")

if __name__ == "__main__":
    err_tag = re.compile("<[^>]*>")
    inputPath = "../../4_Output_Final_Text/"
    dirs = os.listdir(inputPath)
    for file in dirs:
        print(file)
    chosen_folder = input("Which folder of text files would you like to process? ")
    directory = inputPath + chosen_folder
    output_folder = "../Errors/" + chosen_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    input_file_list = os.listdir(directory)
    lineList = []
    for i, file in enumerate(input_file_list):
        output = output_folder + "/" + file + ".txt"
        print("Current page we are working on: ", input_file_list[i])
        with open(directory + "/" + file, 'r', encoding="utf-8") as f1:
            if i == 0:
                with open(output, 'w', encoding="utf-8") as f2:
                    print("***if  Current page: " + file + "***")
                    for line in f1:
                        lineList = line.split()
                        for word in lineList:
                            if word[0] == '<':
                                word = err_tag.sub('', word)
                                errTuple = generateTrainingSet(word)
                                if errTuple:
                                    f2.write("\t".join(errTuple) + "\t\n")
            else:
                with open(output, 'a', encoding='utf-8') as f2:
                    print("APPENDING")
                    print("***else  Current page: " + file + "***")
                    for line in f1:
                        lineList = line.split()
                        for word in lineList:
                            if word[0] == '<':
                                word = err_tag.sub('', word)
                                errTuple = generateTrainingSet(word)
                                if errTuple:
                                    f2.write("\t".join(errTuple) + "\t\n")
    # func = partial(make_error, output_folder, directory)
    # with Pool(processes=os.cpu_count()) as my_pool:
    #     my_pool.map(func, [input_file_list])
    print("Exiting Main")
