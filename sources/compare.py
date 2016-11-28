#
# Filename: compare.py
#
# Author: /u/CrystalLord
#
#
import sys, traceback

from csv_printer import CSVPrinter

DRY_RUN = False

def compare_main():
    try:    
        print("Compare 2 INE matrices")
        print("----------------------")
        pathA = "../ine_logs/2016-01-02_output.csv"
        pathB = "../ine_logs/2016-11-27_output.csv"
        #pathA = "../ine_logs/"+str(input("Filename of previous month matrix> "))
        #pathB = "../ine_logs/"+str(input("Filename of new month matrix> "))
        output = compare(pathA, pathB)
    except IOError:
        print("Invalid file path or access restricted. Closing script.")

def compare(pathA, pathB):
    '''
    TODO: Documentation
    '''
    fileA = open(pathA, "r")
    dataA = fileA.read()
    fileA.close()
    entriesA = dataA.split("\n")
    matrixA = [x.split(",") for x in entriesA]
    
    # Remove trailing blank lines for MatrixA
    if matrixA[-1] == ['']:
        matrixA = matrixA[:-1]

    fileB = open(pathB, "r")
    dataB = fileB.read()
    fileB.close()
    entriesB = dataB.split("\n")
    matrixB = [x.split(",") for x in entriesB]
    
    # Remove trailing blank lines for MatrixB
    if matrixB[-1] == ['']:
        matrixB = matrixB[:-1]

    # Setup Printer
    printer = CSVPrinter()
    printer.set_timestamp(matrixA[0][0]+"/"+matrixB[0][0], 8)
    printer.set_header(matrixA[1])

    resized_matrixA, resized_matrixB = resize_csv(matrixA[2:], matrixB[2:])
    
    print(str(len(resized_matrixB)) + " " + str(len(resized_matrixA))) # debug
    for i in range(len(resized_matrixB)):
        printer.append_csv([
            resized_matrixB[i][0],
            resized_matrixB[i][1],
            -compare_values(resized_matrixA[i][2], resized_matrixB[i][2], "int"),
            compare_values(resized_matrixA[i][3], resized_matrixB[i][3], "int"),
            compare_values(resized_matrixA[i][4], resized_matrixB[i][4], "int"),
            health_compare(resized_matrixA[i][5], resized_matrixB[i][5]),
            round(compare_values(resized_matrixA[i][6], resized_matrixB[i][6], "float"), 3),
            round(compare_values(resized_matrixA[i][7], resized_matrixB[i][7], "float"), 3),
            ])
    
    
    if not DRY_RUN:
        filename = "../ine_logs/"+matrixA[0][0]+"_"+matrixB[0][0]+"_comparison.csv"
        f = open(filename, "w")
        f.write(printer.output_csv())
        f.close()
        print("-------------------------")
        print("CSV printed to: "+filename)
        print("-------------------------")
    else:
        print("-------------------------")
        print("Dry run, no output printed")
        print("-------------------------")

def resize_csv(matrixA, matrixB):
    '''
    Returns 2 matrices that are both the same size, generated from matrixA and matrixB
        
        @param
        -matrixA: first matrix
        -matrixB: second matrix

        @return
        Returns 2 matrices that are the same length, but not necessarily the length
        of either A or B.
    '''
    
    resized_matrixA = matrixA[:]
    resized_matrixB = matrixB[:]
    
    matrix_printer(resized_matrixA)
    matrix_printer(resized_matrixB)

    i = 0
    while i < max(len(resized_matrixA), len(resized_matrixB)):
        print("i: " + str(i))
        print("len A: " + str(len(resized_matrixA)))
        print("len B: " + str(len(resized_matrixB)))
        if i >= len(resized_matrixB) and i < len(resized_matrixA):
            print("Adding new row to B")
            resized_matrixB.append([
                resized_matrixA[i][0], # Tab
                resized_matrixA[i][1], # Name
                "-", # Rank
                "-", # Subscribers
                "-", # Submission Count
                "-", # Health
                "-", # posts per subs
                "-", # % mods
                ])
            continue
            i += 1
        if i >= len(resized_matrixA) and i < len(resized_matrixB):
            print("Adding new row to A")
            resized_matrixA.append([
                resized_matrixB[i][0], # Tab
                resized_matrixB[i][1], # Name
                "-", # Rank
                "-", # Subscribers
                "-", # Submission Count
                "-", # Health
                "-", # posts per subs
                "-", # % mods
                ])
            continue
            i += 1
        
        # Check if they are the same subreddits
        try:
            if resized_matrixA[i][1] != resized_matrixB[i][1]:
                if len(resized_matrixB) > len(resized_matrixA):
                    resized_matrixA.insert(i,[
                        resized_matrixB[i][0], # Tab
                        resized_matrixB[i][1], # Name
                        "-", # Rank
                        "-", # Subscribers
                        "-", # Submission Count
                        "-", # Health
                        "-", # posts per subs
                        "-", # % mods
                        ])
                else:
                    resized_matrixB.insert(i,[
                        resized_matrixA[i][0], # Tab
                        resized_matrixA[i][1], # Name
                        "-", # Rank
                        "-", # Subscribers
                        "-", # Submission Count
                        "-", # Health
                        "-", # posts per subs
                        "-", # % mods
                        ])
                i -= 1 # Decrement so we can review this row a second time
        except IndexError:
            print(sys.exc_info()[0])
            traceback.print_tb(sys.exc_info()[2], limit=1, file=sys.stdout)
            print("i again: " + str(i))
            print(len(resized_matrixA))
            print(len(resized_matrixB))
            print("A here: " + str(resized_matrixA[i]))
            resized_matrixA = resized_matrixA[:-1]
            resized_matrixB = resized_matrixB[:-1]
            break
        # Increment
        i += 1

    return resized_matrixA, resized_matrixB

def compare_values(valueA, valueB, value_type):
    '''
    Provides a difference comparison that still works for a variety of values.
        
        @param
        -valueA: Starting value
        -valueB: Ending value
        -value_type: A string that describes the type of data. Can be int or float

        @return
        Returns the difference of the 2 values.
    '''
    if valueA == "-" or valueA == "FORBIDDEN" or valueA == "NOT FOUND":
        valueA = 0
    if valueB == "-" or valueB == "FORBIDDEN" or valueB == "NOT FOUND":
        valueB = 0

    if value_type == "int":
        return int(valueB)-int(valueA)
    elif value_type == "float":
        return float(float(valueB)-float(valueA))

def health_compare(healthA, healthB):
    if healthA == "healthy" and healthB == "unhealthy":
        return "h -> u"
    elif healthA == "unhealthy" and healthB == "healthy":
        return "u -> h"
    elif healthA == "critical" and healthB == "unhealthy":
        return "c -> u"
    elif healthA == "healthy" and healthB == "critical":
        return "h -> c"
    elif healthA == "critical" and healthB == "healthy":
        return "c -> h"
    elif healthA == "unhealthy" and healthB == "critical":
        return "u -> c"
    else:
        return "-"

def matrix_printer(matrix):
    for index in range(len(matrix)):
        print(matrix[index])

# Main Trick
if __name__ == "__main__":
    compare_main()
