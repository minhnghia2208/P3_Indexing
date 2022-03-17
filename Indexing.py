import json
from typing import Dict
# Connection String
cs = {
    "shakespeare": "shakespeare-scenes.json"
}
###

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

# Global Variable
# Map<Term, PostingList>
invertedIndex = {}

# Indexing
def indexing():
    with open(cs["shakespeare"]) as f:
        data = json.load(f)
    
    corpus = data['corpus']
    
    count = 0
    
    for C in corpus:
        if count > 2: break
        count += 1
        
        docId = C['sceneId']
        
        # Splitting
        def checkEmpty(str):
            if len(str) == 0:
                return False
            return True
        tokens = list(filter(checkEmpty, C['text'].split(' ')))
        
        for index in range(0, len(tokens)):
            term = invertedIndex.get(tokens[index])
            if (not term):
                # Init new term
                invertedIndex[tokens[index]] = PostingList({docId: [index]})
                
            else:
                invertedIndex[tokens[index]].push(docId, index)
                    
    # f = open("InvertedIndex.txt", "w")
    # f.write(invertedIndex)
    # f.close()
    for i in invertedIndex:
        print(i, invertedIndex[i].get())
    return invertedIndex

indexing()