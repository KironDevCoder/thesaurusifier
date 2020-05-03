from string import ascii_letters as characters
from bs4 import BeautifulSoup
import urllib.request
import random

class Word:
    def __init__(self, word):
        self.foundSynonyms = False
        try:
            with urllib.request.urlopen("https://www.thesaurus.com/browse/" + word) as response:
                self.html = response.read()
                if b"MOST RELEVANT" in self.html:
                    self.foundSynonyms = True
                    self.html = self.html.split(b"MOST RELEVANT")[0]
                    self.bs4 = BeautifulSoup(self.html, 'html.parser')
        except:
            print(f"Couldn't find synonyms for '{word}'")

    def synonyms(self):
        s = []
        if self.foundSynonyms:
            for link in self.bs4.find_all("a"):
                if link.get("href") != None:
                    if link.get("href").startswith("/browse/"):
                        s.append(link.text)
        return s


characters += " "
simplifiedText = ""
finalText = ""

text = input("Input: ")

for character in text:
    if character in characters:
        simplifiedText += character

parts = simplifiedText.split(" ")

for part in parts:
    synonyms = Word(part).synonyms()

    if len(synonyms) == 0:
        finalText += part + " "
    else:
        finalText += random.choice(synonyms) + " "

print("Output: " + finalText)
