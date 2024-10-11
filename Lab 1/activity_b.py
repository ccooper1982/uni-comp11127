import sys


## Reads user input. Empty strings ignored.
## Returns a tuple as (exitFlag, userInput)
## exitFlag - true if '!' character is entered
def getUserInput():
  print ("Enter ! to exit. Empty input is ignored.")

  line = ""
  # loop whilst input is empty AND until user exits
  while line == "" and line !=  "!":
    line = input("Input: ")

  # return (exitFlag, line) tuple
  return (line == "!", line)



## Clean the data: return alphanumerical and whitespace.
## Input is not trimmed because tokenising handles that.
def clean(line):
  cleaned = ""
  for c in line:
    if c.isalnum() or c.isspace():
      cleaned += c.lower()
  return cleaned



## Tokenise by whitespace, returning list of words.
def tokenise(line):
  return line.split() # default is any whitespace



## Counts the frequency of each word in the wordList and counts
## each occurence of a number (123 is one number, not three).
## Return a tuple: (wordMap, numberCount), where wordMap is {word:count}
def count(wordList):
  wordMap = dict()
  numberCount = 0
  
  # for each token, update word count and number count. Non-alphanumerical characters ignored
  for word in wordList:
    if word.isalpha():
      # if word not found, returns 0 so +1 will set occurences to 1. 
      wordMap[word] = wordMap.get(word, 0) + 1
    elif word.isdigit():
      numberCount += 1

  return (wordMap, numberCount)



## Parse the input line. Non-alphanumerical characters are ignored.
## Returns a tuple: (wordMap, numberCount)
##  where wordMap is: {word:count}
def parse(input):
  cleaned = clean(input)
  wordList = tokenise(cleaned)
  return count(wordList) 



## Input is test data with expected results which are checked.
def test():
  # test data is a dictionary of: <input> : (result) 
  # where result is: (<numberCount>, {<word>:<count>})
  data =  {
            "Hello world" : (0, {"hello":1, "world":1}),
            "dog cat dog cat cat cat" : (0, {"dog":2, "cat":4}),
            "Hello $ world £" : (0, {"hello":1, "world":1}),
            "$hello" : (0, {"hello":1}),
            "hello$" : (0, {"hello":1}),
            "he$$o" : (0, {"heo":1}),
            "2 dog dog 4 cat cat cat cat" : (2, {"dog":2, "cat":4}),
            "123 456 78 9" : (4, {})
          }
  
  for line, result in data.items():
    (wordMap, numberCount) = parse(line)
    (expectedNumberCount, expectedWordMap) = result

    assert numberCount == expectedNumberCount, line
    assert wordMap == expectedWordMap, line



# if test mode, feed hard-coded data for validation
if len(sys.argv) > 1 and sys.argv[1] == "test":
  test()
else:
  # get user provided data
  (exit, input) = getUserInput()
  # user can exit by typing !
  if not exit:
    (wordMap, numberCount) = parse(input)

    print("Number Count: {0}".format(numberCount))
    print(wordMap)

