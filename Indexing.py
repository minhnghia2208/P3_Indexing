import collections
import json
import time
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
    "playId": "playId",
    "text": "text"
    
}

# Global Variable
invertedIndex = {} # Map<Term, PostingList>
average_len, num_scene = 0, 0

shortest_len, shortest_scene = 1000000, ''
longest_len, longest_scene = 0, ''

play_dict = {}
shortest_plen, shortest_play = 1000000, ''
longest_plen, longest_play = 0, ''

# PostingList: Map< docId, int[] >
# PlayId: Map< docId, playId >
class PostingList:
    def __init__(self, postingList={}, playId={}):
        self.postingList = postingList
        self.playId = playId
        
    def get(self):
        return self.postingList
    
    def getPlayID(self):
        return self.playId
    
    def push(self, docId, index):
        if self.postingList.get(docId):
            self.postingList[docId].append(index)
        else:
            self.postingList[docId] = [index]
    
    def pushPlayId(self, docId, playId):
        if (not self.playId.get(docId)):
            self.playId[docId] = playId

# Indexing
def indexing():
    with open(cs["shakespeare"]) as f:
        data = json.load(f)
    
    corpus = data[cs["corpus"]]
    for C in corpus:
        docId = C[cs["sceneId"]]
        playId = C[cs["playId"]]
        
        # Splitting
        def checkEmpty(str):
            if len(str) == 0:
                return False
            return True
        tokens = list(filter(checkEmpty, C[cs["text"]].split(' ')))
        
        ###
        # Q6 section
        # global shortest_len, shortest_scene
        # global longest_len, longest_scene
        
        # global average_len, num_scene
        # global play_dict
        
        # shortest_len = min(shortest_len, len(tokens))
        # if shortest_len == len(tokens):
        #     shortest_scene = docId
            
        # longest_len = max(longest_len, len(tokens))
        # if longest_len == len(tokens):
        #     longest_scene = docId
            
        # average_len = average_len + len(tokens)
        # num_scene = num_scene + 1
        
        # if play_dict.get(playId):
        #     play_dict[playId] += len(tokens)
        # else: 
        #     play_dict[playId] = len(tokens)
        # End Q6
        ###
        
        for index in range(0, len(tokens)):
            term = invertedIndex.get(tokens[index])
            if (not term):
                # Init new term
                # invertedIndex.update({tokens[index]: PostingList({docId: [index]}, {docId: playId})})
                invertedIndex[tokens[index]] = PostingList({docId: [index]}, {docId: playId})
                
            else:
                invertedIndex[tokens[index]].push(docId, index)
                invertedIndex[tokens[index]].pushPlayId(docId, playId)
                    
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
        set = sorted(set)
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
                            # freq.update({sceneId: len(self.invertedIndex[term].get()[sceneId])})
                            freq[sceneId] = len(self.invertedIndex[term].get()[sceneId])
            return freq
            
        # Map< sceneId, freq >
        freq1, freq2 = {}, {}
        # Set< sceneId >
        ans = set()
        freq1 = freqCal(terms1)
        freq2 = freqCal(terms2)
        
        ###
        # Store for Q7:
        # temp = collections.OrderedDict(sorted(freq1.items()))
        # f = open('Scene1Id.txt', "w")
        # for i in temp:
        #     f.write( i + '\n')
        # f.close()
        
        # f = open('Scene1Count.txt', "w")
        # for i in temp:
        #     f.write( str(temp[i]) + '\n')
        # f.close()
        
        # temp = collections.OrderedDict(sorted(freq2.items()))
        # f = open('Scene2Id.txt', "w")
        # for i in temp:
        #     f.write( i + '\n')
        # f.close()
        
        # f = open('Scene2Count.txt', "w")
        # for i in temp:
        #     f.write( str(temp[i]) + '\n')
        # f.close()
        ###
        
        for sceneId in freq1:
            if freq2.get(sceneId):
                if freq1[sceneId] > freq2[sceneId]:
                    ans.add(sceneId)
            else: ans.add(sceneId)
                    
        self.writeFile(fileName, ans)
        return ans
    
    # Find playId(s) that contain(s) given term
    # @param {string[]} term: first array of terms
    # @param {string} fileName
    # @return {set< string >} Ordered set of playId
    def findPlays(self, term, fileName):
        ans = set()
        if self.invertedIndex.get(term): 
            for playId in self.invertedIndex[term].getPlayID():
                ans.add(self.invertedIndex[term].getPlayID()[playId])
               
        self.writeFile(fileName, ans)
        return ans
    
class PhraseBased:
    def __init__(self, invertedIndex={}):
        self.invertedIndex = invertedIndex
        
    def writeFile(self, fileName, set):
        set = sorted(set)
        f = open(fileName, "w")
        for i in set:
            f.write( i + '\n')
        f.close()
        
    # Find sceneId(s) that contain the phrase
    # with p length maximum for each terms from each other
    # @param { string } phrase
    # @param { int } p: maximum space of each term in phrase
    # @return { set<string> } set of docId
    def findScenes(self, phrase, p, fileName):
        def checkEmpty(str):
            if len(str) == 0:
                return False
            return True
        
        terms = list(filter(checkEmpty, phrase.split(' ')))
        docIds = self.findSceneIds(terms)
        ans = self.intersecting(terms, docIds, p)
        self.writeFile(fileName, ans)
        return ans
    
    # Find sceneId(s) that contain(s) all the given terms
    # @param {string[]} terms: first array of terms
    # @return {set< string >} Ordered set of sceneId
    def findSceneIds(self, terms):
        ans = set()
        init = True
        for term in terms:
            if self.invertedIndex.get(term):
                temp = set()
                # Init first set of sceneId
                if init:
                    for sceneId in self.invertedIndex[term].get():
                        ans.add(sceneId)
                    init = False
                    
                # Add the rest of scene that contain terms
                # Remove sceneId that does not contain every term
                else:
                    for sceneId in self.invertedIndex[term].get():
                        if sceneId in ans:
                            temp.add(sceneId)
                    # Re-assign temp to ans
                    ans = set()
                    for i in temp:
                        ans.add(i)
        return ans
    
    # Find sceneId(s) that contain a 
    # @param { string[] } terms
    # @param { set< string > } docIds: all sceneIds containning terms
    # @param { int } p: maximum space of each term in phrase 
    # @return { set< string > } ans: all docIds containing phrase
    def intersecting(self, terms, docIds, p):
        ans = set()
        for docId in docIds:
            index = []
            for term in terms:
                # Array of array
                # representing index of each term
                index.append(self.invertedIndex[term].get()[docId])
            if self.matchingWindow(index, p):
                ans.add(docId)
        return ans
    
    # return {bool} ans
    def matchingWindow(self, index, p):
        # @param {int} current: current index of docId window
        # @return {bool} ans: if phrase is not construtible from docId
        def recur(current, pos):
            if current >= len(index)-1:
                return True
            
            next = current + 1
            for i in range(pos, len(index[current])):
                for j in range(0, len(index[next])):
                    dis = index[next][j] - index[current][i]
                    if dis > 0 and dis <= p:
                        return recur(next, j)     
            return False
        return recur(0, 0)
        
###
# Main
indexing()
termBased = TermBased(invertedIndex)
start_time = time.time()
termBased.findGreaterScene(['thee', 'thou'], ['you'], cs["terms0"])
print("term0.txt time %s" % (time.time() - start_time))

start_time = time.time()
termBased.findGreaterScene(['venice', 'rome', 'denmark'], [], cs["terms1"])
print("term1.txt time %s" % (time.time() - start_time))

start_time = time.time()
termBased.findPlays('goneril', cs["terms2"])
print("term2.txt time %s" % (time.time() - start_time))

start_time = time.time()
termBased.findPlays('soldier', cs["terms3"])
print("term3.txt time %s" % (time.time() - start_time))

phraseBased = PhraseBased(invertedIndex)
start_time = time.time()
phraseBased.findScenes("poor yorick", 1, cs["phrase0"])
print("phrase0.txt time %s" % (time.time() - start_time))

start_time = time.time()
phraseBased.findScenes("wherefore art thou romeo", 1, cs["phrase1"])
print("phrase1.txt time %s" % (time.time() - start_time))

start_time = time.time()
phraseBased.findScenes("let slip", 1, cs["phrase2"])
print("phrase2.txt time %s" % (time.time() - start_time))

# print('Shortest scene: ', shortest_scene)
# print('Longest scene: ', longest_scene)
# print('Average length', average_len/num_scene)

# for playId in play_dict:
#     shortest_plen = min(shortest_plen, play_dict[playId])
#     if shortest_plen == play_dict[playId]:
#         shortest_play = playId
        
#     longest_plen = max(longest_plen, play_dict[playId])
#     if longest_plen == play_dict[playId]:
#         longest_play = playId
    
# print('Shortest play: ', shortest_play)
# print('Longest play: ', longest_play)
