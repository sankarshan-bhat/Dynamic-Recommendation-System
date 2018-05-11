import sys
from textblob import TextBlob

if len(sys.argv[1:]):
	txt = sys.argv[1]
else:
	txt = """Omerta Movie !! Awesome acting by Rajkumar Rao !! """

blob = TextBlob(txt)
print(blob.noun_phrases)
