import sys
from collections import defaultdict



###
### Run without arguments to accept user input.
### Run with "./activity_b.py test" to run test data.
###   Test mode will assert on failure.


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



## Clean the data: return alphanumerical and whitespace, ignores special chars.
## Input is not trimmed because tokenising handles that.
def clean(line: str) -> str:
  cleaned = ""
  
  for c in line:
    if c.isalnum() or c.isspace():
      cleaned += c.lower()

  return cleaned



## Tokenise by whitespace, returning list of words.
def tokenise(line: str):
  return line.split() # default is any whitespace



## Counts the frequency of each word in the wordList, and counts
## each occurence of a number (123 is one number, not three).
## Return a tuple: (wordDict, numberCount), where wordDict is {word:count}
def count(wordList: list) -> tuple:
  # defaultdict: if a key is not found, it will initialise value to 0 (because of int())
  wordDict = defaultdict(int)
  numberCount = 0
  
  # for each token, update word count and number count.
  for word in wordList:
    if word.isalpha():
      # key not found: value is 0
      # key found: current value returned
      # then we +1 (so initialise to 1 or increment current value)
      wordDict[word] += 1  
    elif word.isdigit():
      numberCount += 1

  return (wordDict, numberCount)



## Parse the input line. Non-alphanumerical characters are ignored.
## Returns a tuple: (wordDict, numberCount)
##  where wordDict is: {word:count}
def parse(input: str):
  cleaned = clean(input)
  wordList = tokenise(cleaned)
  return count(wordList) 



## Input is test data with expected results which are checked.
def test():
  # test data is a dictionary of: <input> : (result) 
  # where result is: (<numberCount>, {<word>:<count>})
  data =  {
            "Hello world" : (0, {"hello":1, "world":1}),
            "Hello, world!" : (0, {"hello":1, "world":1}),
            "Hello hello world World" : (0, {"hello":2, "world":2}),
            "dog cat dog cat cat cat" : (0, {"dog":2, "cat":4}),
            "Hello $ world £" : (0, {"hello":1, "world":1}),
            "$hello" : (0, {"hello":1}),
            "hello$" : (0, {"hello":1}),
            "he$$o" : (0, {"heo":1}),
            "2 dog dog 4 cat cat cat cat" : (2, {"dog":2, "cat":4}),
            "123 456 78 9" : (4, {})
          }
  
  for line, result in data.items():
    (wordDict, numberCount) = parse(line)
    (expectedNumberCount, expectedwordDict) = result

    assert numberCount == expectedNumberCount, line
    assert wordDict == expectedwordDict, line



# if test mode, feed hard-coded data for validation
if len(sys.argv) > 1 and sys.argv[1] == "test":
  test()
else:
  # get user provided data. user can exit by typing !
  (exit, input) = getUserInput()
  if not exit:
    (wordDict, numberCount) = parse(input)

    # format string, more convenient than string.format() in previous version
    print(f"Number Count: {numberCount}")
    
    print("Word Counts:")
    # couldn't get pprint() to display correctly with the defaultdict
    for word, wordCount in wordDict.items():
      print(f" {word} : {wordCount}")

