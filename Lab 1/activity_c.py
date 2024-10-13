
import sys
import requests
from collections import defaultdict
from html.parser import HTMLParser


# words to ignore in a set. A list may be more efficient, depending
# on how it is implemented (i.e. a vector/array in contigious memory) rather than node-based list
ignoreList = {"the", "a", "in", "as", "an", "of", "but", "and", "or", "to", "be", "for", "on"}



## Counts frequency of words (excluding those in ignore list).
## Only words within the <body> tag are counted.
## Contains bool flags to indicate when particular tags are found.
## -  Looks for <h2 id="References">, and once found, looks for <ol> or <ul>, then 
##    counts all the <li> entries
## -  Looks for <a> to counts hyperlinks
## -  Data within <p> are tokenised and word frequency are counted (for words that isalpha() is true)
class Parser (HTMLParser):
  valid = False                 # if <body> was found
  inBody = False                # true whilst in <body>
  inReferencesList = False      # true whilst in <ol class="references">
  inParagraph = False           # true whilst in <p>
  foundReferencesHeader = False # true when <h2 id="References"> found
  linksCount = 0                # count of <a> tags found
  referencesCount = 0           # count of <li> within <ol class="references">
  wordMap = defaultdict(int)    # allows values to have default value 0 if key not present


  ## Override of HTMLParser.
  ## Called when a tag is found, i.e. <body>. 
  ## Attributes are in 'attrs' is a list of tuples, i.e.:
  ##  <a href="python.org"> would be: [('href', 'python.org')]
  def handle_starttag(self, tag, attrs):
    
    # check attributes in:  <h2 id="References">
    # use list comprehension:
    #   - looks for 'id' and 'References' in each tuple
    #   - if found add tuple to a new list
    #   - the returned list will either be empty or [('id', 'references')] 
    isReferenceHeader = lambda attribs : len([pair for pair in attribs if "id" in pair and "References" in pair]) == 1
    
    # check the tag and updated the flags accordingly
    if tag == "a":
      self.linksCount += 1
    elif tag == "body":
      self.inBody = True
    elif tag == "h2" and isReferenceHeader(attrs):
      # found <h2 id="References">
      self.foundReferencesHeader = True
    elif self.foundReferencesHeader and (tag == "ol" or tag == "ul"): 
      # already found <h2 id="References"> AND is this tag is a list (ol or ul)
      self.inReferencesList = True
    elif self.foundReferencesHeader and tag == "li" and self.inReferencesList:
      # already found <h2 id="References"> AND tag is <li> AND we're in the references list (<ol> or <ul>)
      self.referencesCount += 1
    elif tag == "p" and self.inBody:
      # found <p> so handle_data() can count words
      self.inParagraph = True


  ## Override of HTMLParser
  def handle_endtag(self, tag):
    # check ending tags and update tags
    if tag == "body":
      self.valid = self.inBody # parsing only valid if we have previously found <body>
      self.inBody = False
    elif (tag == "ol" or tag == "ul") and self.inReferencesList == True:
      # found </ol> or </ul> AND we were in the references list
      self.inReferencesList = False
      self.foundReferencesHeader = False
    elif tag == "p":
      self.inParagraph = False
      

  ## Override of HTMLParser
  def handle_data(self, data):
    if self.inParagraph:
      self.updateCount(data)


  ## Tokenise 'data' to separate words.
  ## If word is alpha and not in the ignore list, add to word map.
  def updateCount(self, data: str):
    tokens = data.split()
    
    for word in tokens:
      if word.isalpha() and word not in ignoreList:
        # if word not found, 0 is returned, to which we add 1, initialising the count to 1
        self.wordMap[word] += 1
      


## Grabs the URL via a HTTP GET request.
## Returns a tuple: (valid, content)
##  valid is false: the request failed and content is empty
##  valid is true: content contains the complete HTML document
def scrape(url: str):
  print("Scraping: " + url)
  # send request with a reasonable timeout
  # use 'with' for resource management, handling closing of the connection
  with requests.get(url, timeout = 5) as rsp: 
    valid = rsp.status_code == 200 # status code for HTTP OK
  
  # return (True, <content>) if request OK
  # otherwise: (False, "")
  return (True, rsp.text) if valid else (False, "")



## Using the HTML parser, count and report the word count, hyper links and references.
## Unique words and words to ignore are also reported.
def count(html: str, printWordDict: bool):
  parser = Parser() # create parser instance
  parser.feed(html) # parse the HTML

  if parser.valid: # if <body> tag found
    print(f"Ignoring words: {ignoreList}")
    print(f"Unique words: {len(parser.wordMap)}")
    print(f"Hyperlinks: {parser.linksCount}")
    print(f"References: {parser.referencesCount}")
    
    # only print word map if first command line argument is "wordmap"
    if printWordDict:
      print(parser.wordMap)



## Send HTTP GET request, parse the HTML and report findings.
## If the GET request fails, reports the failure and falls through.
def run():
  # list of articles
  # NOTE: Miss Meyers is the short test Wikipedia article, easier to read word dict in terminal
  urls =  [
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://en.wikipedia.org/wiki/C++",
            "https://en.wikipedia.org/wiki/Bjarne_Stroustrup",
            "https://en.wikipedia.org/wiki/Cat",            
            "https://en.wikipedia.org/wiki/Miss_Meyers"  
          ]
  
  

  url = ""  # either URL from command line or in the urls list
  printWordDict = False  # only print the word dictionary if requested
  
  
  if len(sys.argv) == 3:
    # URL and wordmap args present
    url = sys.argv[1]
    printWordDict = sys.argv[2].lower() == "wordmap"
  elif len(sys.argv) == 2:
    # check for wordmap arg
    if sys.argv[1].lower() == "wordmap":
      printWordDict = True
    else:
      # arg is not wordmap, so assume URL
      url = sys.argv[1]
  else:
    # default URL and don't print word dictionary
    url = urls[3]


  # send HTTP GET request, returning a tuple: (bool, string)
  (valid, content) = scrape(url) 

  # valid True if 200 OK response was received
  if valid:     
    count(content, printWordDict)
  else:
    print("Request failed")


run()
