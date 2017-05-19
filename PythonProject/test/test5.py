import re
class WordDictionary:
    # initialize your data structure here.
    def __init__(self):
        # Write your code here
        self.wordDictionary = []
    # @param {string} word
    # @return {void}
    # Adds a word into the data structure.
    def addWord(self, word):
        # Write your code here

        self.wordDictionary.append(word)
        return self.wordDictionary


    # @param {string} word
    # @return {boolean}
    # Returns if the word is in the data structure. A word could
    # contain the dot character '.' to represent any one letter.
    def search(self, word):
        # Write your code here
        word.replace('.','\w')
        pattern = re.compile(word)
        for w in self.wordDictionary:
            # TODO: write code...

            match = re.search(pattern,w)
            try:
                if match.group():
                    print match.group()
                    return True
            except:
                continue
        print 'ssr'
        return False
s = WordDictionary()
# s.addWord("bad")
s.addWord('dad')
s.search('da.')

# Your WordDictionary object will be instantiated and called as such:
# wordDictionary = WordDictionary()
# wordDictionary.addWord("word")
# wordDictionary.search("pattern")