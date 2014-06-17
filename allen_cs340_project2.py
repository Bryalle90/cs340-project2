from avl import pyavltree
import sys
import time
import random

class node:
	def __init__(self):
		self.data = [None, None, None]
		self.ptr = [None, None, None, None]

	def isLeaf(self):
		return self.ptr[0] == None

	def getDataIndex( self, data ):
		if self.data[0] == None:
				return 0
		elif data <= self.data[0]:
				return 0
		elif self.data[1] == None:
				return 1
		elif data <= self.data[1]:
				return 1
		else:
				return 2
	def getPtrIndex( self, data ):
		if data <= self.data[0]:
				return 0
		elif self.data[1] == None:
				return 1
		elif data <= self.data[1]:
				return 1
		elif self.data[2] == None:
				return 2
		elif data <= self.data[2]:
				return 2
		else:
				return 3
	def __str__(self):
		return str(self.data)

class t234:
	def __init__( self ):
		self.root = node()

	def splitRoot(self, nodePtr):
		if nodePtr.data[2] == None:
				return nodePtr
				
		# Your code here
		
		p = node()
		l = node()
		r = node()
		
		p.data[0] = self.root.data[1]
		l.data[0] = self.root.data[0]
		r.data[0] = self.root.data[2]

		p.ptr[0] = l
		p.ptr[1] = r
		l.ptr[0] = self.root.ptr[0]
		l.ptr[1] = self.root.ptr[1]
		r.ptr[0] = self.root.ptr[2]
		r.ptr[1] = self.root.ptr[3]
		
		newRoot = p

		return newRoot

	def split( self, nodePtr, index ):
		if nodePtr.ptr[index].data[2] == None:
				return

		# Your code
		promoteValue = nodePtr.ptr[index].data[1]
		promoteIndex = nodePtr.getDataIndex(promoteValue)

		# shift larger data one space to the right in current node
		if promoteIndex == 0 or promoteIndex == 1:
			nodePtr.data[2] = nodePtr.data[1]
			if not nodePtr.ptr[2] == None:
				nodePtr.ptr[3] = nodePtr.ptr[2]
		if promoteIndex == 0:
			nodePtr.data[1] = nodePtr.data[0]
			if not nodePtr.ptr[1] == None:
				nodePtr.ptr[2] = nodePtr.ptr[1]

		# promote the middle item from child node
		nodePtr.data[promoteIndex] = promoteValue

		# create a new node for the right item and transfer children 1 & 2
		newNode = node()
		newNode.data[0] = nodePtr.ptr[index].data[2]
		newNode.ptr[0] = nodePtr.ptr[index].ptr[2]
		newNode.ptr[1] = nodePtr.ptr[index].ptr[3]

		# remove data and children from old child node
		nodePtr.ptr[index].data[1] = None
		nodePtr.ptr[index].data[2] = None
		nodePtr.ptr[index].ptr[2] = None
		nodePtr.ptr[index].ptr[3] = None

		# insert the new node as a child of current node
		nodePtr.ptr[index+1] = newNode

	def insert( self, data ):
		#check the split for root
		self.root = self.splitRoot( self.root )
		curr = self.root
		#print 'inserting:', data
		while curr != None:
			#check if we are at a leaf
			if curr.isLeaf():
				index = curr.getDataIndex( data )
				# for i in range(  len( curr.data )-1, index, -1 ):
				# 	curr.data[i] = curr.data[i-1]
				curr.data[(index+1):] = curr.data[index:2]
				curr.data[index] = data
				return
			else:
				#find pointer to follow
				index = curr.getPtrIndex( data )
				self.split( curr, index )
				index = curr.getPtrIndex( data )
				curr = curr.ptr[index]

	def printTree( self , direction):
		if direction == 0:
			self.printRecursive(self.root, 0, 0)
		elif direction == 1:
			self.printRecursiveLR( self.root, 0 , 0 )
		elif direction == 2:
			self.printRecursiveIO( self.root, 0 )

	def printRecursive( self, curr, depth, index ):
		#print right to left, then curr
		if curr == None:
				return
		self.depthSpace = '\t\t'
		#print pointers right->left
		for i in range(3, -1, -1):
			self.printRecursive(curr.ptr[i], depth + 1, i)
		#print current node data
		print self.depthSpace * depth, index, curr.data
		return
		# Finish the print function

	def printRecursiveLR( self, curr, depth, index ):
		#print left to right, then curr
		if curr == None:
				return
		self.depthSpace = '\t\t'
		#print current node data
		print self.depthSpace * depth, index, curr.data
		#print pointers right->left
		for i in range(0, 4, 1):
			self.printRecursiveLR(curr.ptr[i], depth + 1, i)
		return
		# Finish the print function

	def printRecursiveIO( self, curr, depth):
		#print right to left, then curr
		if curr == None:
				return
		self.depthSpace = '\t\t'

		self.printRecursiveIO(curr.ptr[0], depth + 1)
		print self.depthSpace * depth, curr.data[0]
		self.printRecursiveIO(curr.ptr[1], depth + 1)
		print self.depthSpace * depth, curr.data[1]
		self.printRecursiveIO(curr.ptr[2], depth + 1)
		print self.depthSpace * depth, curr.data[2]
		self.printRecursiveIO(curr.ptr[3], depth + 1)
		return
		# Finish the print function

	def getSize(self):
		return self.getSizeOfTree( self.root )

	def getSizeOfTree(self, curr):
		if curr == None:
			return 0
		childrenSize = 0
		currSize = 0
		pointerSize = 0
		for i in range(3, -1, -1):
			childrenSize += self.getSizeOfTree(curr.ptr[i])
			pointerSize += sys.getsizeof(curr.ptr[i])
		for i in range(3):
			currSize += sys.getsizeof(curr.data[i])
		return childrenSize + currSize + pointerSize

	def find( self, word ):
		return self.findWord( word, self.root )

	def findWord( self, word, curr):
		matchList = []
		if curr == None:
			return matchList
		else:
			for j in range(3):
				i = 0
				compare = 'same'
				if not curr.data[j] == None:
					size = len(word) if len(word) <= len(curr.data[j]) else len(curr.data[j])
					for i in range(size):
						if word[i] == '*':
							break
						elif word[i] < curr.data[j][i]:
							compare = 'smaller'
							break
						elif word[i] > curr.data[j][i]:
							compare = 'larger'
							break
						i += 1
					if compare == 'same':
						if len(word) == len(curr.data[j]):
							matchList.append(curr.data[j])
						matchList += self.findWord( word, curr.ptr[j])
					elif compare == 'smaller':
						matchList += self.findWord( word, curr.ptr[j])
						break
					if j == 2 or curr.data[j+1] == None:
						matchList += self.findWord( word, curr.ptr[j+1])
						break
			return matchList


	def get_height( self ):
		return self.getHeight( self.root, 0 )
	def getHeight( self, curr, depth ):
		#print left to right, then curr
		if curr == None:
			return None

		heights = []
		returnHeight = depth
		#print pointers right->left
		for i in range(4):
			heights.append(self.getHeight(curr.ptr[i], depth + 1))
		for i in range(4):
			if not heights[i] == None and heights[i] > returnHeight:
				returnHeight = heights[i]
		return returnHeight
		# Finish the print function

	def get_nodeAmt( self ):
		return self.getNodeAmt( self.root)
	def getNodeAmt( self, curr):
		if curr == None:
			return 0
		else:
			count = 0
			for i in range(4):
				count += self.getNodeAmt(curr.ptr[i])
			return count + 1





infile = open( './dictionaryLin.txt', 'r')

wordlist = []
T = t234()
avlTree = pyavltree.AVLTree()
mysteryWord = 'sabby'
searchlist = [ 'circuitry', 'grecize', 'legislative assembly', 'primuline yellow', 'terephthalate', 'widest dissemination', 'zamiel']
wlSize = 700000

for i, item in enumerate( infile ):
	wordlist.append(item)
	if i >= wlSize:
		break

random.shuffle(wordlist)
# wordlist.sort( key= lambda x: len( x ), reverse= True )

### Start timing insert
tInsert_start = time.clock()
for w in wordlist:
	T.insert(w[:-1])
tInsert_end = time.clock()

aInsert_start = time.clock()
for w in wordlist:
	avlTree.insert(w[:-1])
aInsert_end = time.clock()


#print T.printTree(1)
#print avlTree.as_list(1)

print '---------------------------------'
print 'insert'
print 'wordlist size, 234 tree insert time, avl tree insert time, 234 size'
print wlSize
print tInsert_end - tInsert_start
print aInsert_end - aInsert_start
print '---------------------------------'



### Print the wordlist
# for w in wordlist:
# 	print w
# print '---------------------------------'

## Look for words in t234 and print matches
# found = T.find(mysteryWord)
# for w in found:
# 	print w,

### get search times
# found234 = []
# foundavl = []
# tSearch_start = []
# aSearch_start = []
# tSearch_end = []
# aSearch_end = []

# for w in searchlist:
# 	# print 'searching for', w

# 	tSearch_start.append(time.clock())
# 	found234.extend((T.find(w)))
# 	tSearch_end.append(time.clock())

# 	aSearch_start.append(time.clock())
# 	foundavl.append((avlTree.find(w).key))
# 	aSearch_end.append(time.clock())

# print 'search times'
# it = 0
# for f in found234:
# 	print tSearch_end[it] - tSearch_start[it]
# 	it += 1
# print '---------------------------------'
# it = 0
# for f in foundavl:
# 	print aSearch_end[it] - aSearch_start[it]
# 	it += 1
# print '---------------------------------'
#print avlTree.as_list(1)
#print T.printTree(1)

### get size of trees
print T.getSize()
print sys.getsizeof(avlTree.find('sabby')) * wlSize

### get tree heights
print T.get_height()
print avlTree.height()

### get 234 tree node amount
print T.get_nodeAmt()
