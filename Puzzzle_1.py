
import regex

spelled_digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

dict_spd = dict((spelled_digits[i], "{0:d}".format(i+1)) for i in range(9))

digit_pattern = regex.compile("|".join(spelled_digits))

lines= ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
lines_v2 = ["two1nine", "eightwothree", "abcone2threexyz", "xtwone3four",
            "4nineeightseven2", "zoneight234", "7pqrstsixteen"]



def getCalibrationValue(text):
    """
    str -> int
    get the calibration value for a text
    It takes the first and the last digit in the string
    and puts them together into an int
    """
    digit_table = [x for x in list(text) if x in "0123456789"] 
    digit1 = digit_table[0]
    digit2 = digit_table[-1]
    return int(digit1 + digit2)


def getCalibrationValueSpelledDigit(text):
    """
    str -> int
    get the calibration value for a text
    It takes the first and the last digit in the string
    It also consider digits that are written as text
    and puts them together into an int
    """
    digit_table = [(i,x) for i,x in enumerate(list(text)) if x in "0123456789"] 
    ##Now match the pattern
    spd_match_table = [(m.start(), dict_spd[m.group()], m.group()) 
                       for m in regex.finditer(digit_pattern, text, 
                                               overlapped = True)]
    merged_table = sorted(digit_table + spd_match_table, 
                          key = lambda m: m[0])
    digit1 = merged_table[0][1]
    digit2 = merged_table[-1][1]
    return int(digit1 + digit2)

file = "./input"

res = [getCalibrationValueSpelledDigit(x) for x in lines_v2]

#print(res)

fin = open(file, "r")
table_vals = fin.readlines()
all_digits = [getCalibrationValueSpelledDigit(l) for l in table_vals]
print("read {} lines with values".format(len(all_digits)))
print(sum(all_digits))
fin.close()
fout = open("text.txt", "w")
for i,v in enumerate(table_vals):
    fout.write("{0}\t{1}".format(all_digits[i], v))
fout.close()
#numbers = 