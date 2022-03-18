import json
from typing import Dict
# Connection String
cs = {
    "shakespeare": "shakespeare-scenes.json",
    
    "terms0": "terms0.txt",
    "terms1": "terms1.txt",
    "terms2": "terms2.txt",
    "terms3": "terms3.txt",
    
    "phrase0": "phrase0.txt",
    "phrase1": "phrase1.txt",
    "phrase2": "phrase2.txt",
    
    "corpus": "corpus",
    "sceneId": "sceneId",
    "text": "text"
    
}

# Global Variable
invertedIndex = {} # Map<Term, PostingList>

# PostingList: Map< docId, int[] >
class PostingList:
    def __init__(self, postingList={}):
        self.postingList = postingList
        
    def get(self):
        return self.postingList
    
    def push(self, docId, index):
        if self.postingList.get(docId):
            self.postingList[docId].append(index)
        else:
            self.postingList[docId] = [index]

# Indexing
def indexing():
    with open(cs["shakespeare"]) as f:
        data = json.load(f)
    
    corpus = data[cs["corpus"]]
    for C in corpus:
        docId = C[cs["sceneId"]]
        
        # Splitting
        def checkEmpty(str):
            if len(str) == 0:
                return False
            return True
        tokens = list(filter(checkEmpty, C[cs["text"]].split(' ')))
        
        for index in range(0, len(tokens)):
            term = invertedIndex.get(tokens[index])
            if (not term):
                # Init new term
                invertedIndex[tokens[index]] = PostingList({docId: [index]})
                
            else:
                invertedIndex[tokens[index]].push(docId, index)
                    
    ###
    # Write to "DISK"
    # f = open("InvertedIndex.txt", "w")
    # for i in invertedIndex:
    #     f.write( i + ': ' + str(invertedIndex[i].get()) + '\n')
    # f.close()
    ###
    
    return invertedIndex

# Term-based Queries
class TermBased:
    def __init__(self, invertedIndex={}):
        self.invertedIndex = invertedIndex
        
    def writeFile(self, fileName, set):
        f = open(fileName, "w")
        for i in set:
            f.write( i + '\n')
        f.close()
            
    # Find sceneId(s) where freq from arr1 > freq from arr2
    # @param {string[]} terms1 first array of terms
    # @param {string[]} terms2 second array of terms
    # @return {set< string >} Ordered set of sceneId
    def findGreaterScene(self, terms1, terms2, fileName):
        def freqCal(terms):
            # Map< sceneId, freq >
            freq = {}
            for term in terms:
                if self.invertedIndex.get(term): 
                    for sceneId in self.invertedIndex[term].get():
                        if freq.get(sceneId):
                            freq[sceneId] += len(self.invertedIndex[term].get()[sceneId])
                        else:
                            freq[sceneId] = len(self.invertedIndex[term].get()[sceneId])
            return freq
            
        # Map< sceneId, freq >
        freq1, freq2 = {}, {}
        # Set< sceneId >
        ans = set()
        freq1 = freqCal(terms1)
        freq2 = freqCal(terms2)
        
        for sceneId in freq1:
            if freq2.get(sceneId):
                if freq1[sceneId] > freq2[sceneId]:
                    ans.add(sceneId)
            else: ans.add(sceneId)
                    
        self.writeFile(fileName, ans)
        return ans
    
    # Find playId(s) that contain(s) given term
    # @param {string[]}  first array of terms
    # @return {set< string >} Ordered set of sceneId
    def findPlays(self, term, fileName):
        ans = set()
        if self.invertedIndex.get(term): 
            for sceneId in self.invertedIndex[term].get():
                # Get playId
                playId = sceneId.split(':')[0]
                ###
                ans.add(self.invertedIndex[term].get()[playId])
               
        self.writeFile(fileName, ans)
        return ans
    

###
# Main
indexing()
termBased = TermBased(invertedIndex)
termBased.findGreaterScene(['thee', 'thou'], ['you'], cs["terms0"])
termBased.findGreaterScene(['venice', 'rome', 'denmark'], [], cs["terms1"])
termBased.findPlays('goneril', cs["terms2"])
termBased.findPlays('soldier', cs["terms3"])
