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
			if not nodePtr.data[promoteIndex] == None and promoteIndex < 2:
				nodePtr.data[promoteIndex+1] = nodePtr.data[promoteIndex]
				if not nodePtr.ptr[promoteIndex+1] == None:
					nodePtr.ptr[promoteIndex+2] = nodePtr.ptr[promoteIndex+1]

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
					# 	  curr.data[i] = curr.data[i-1]
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
			#print right to left, then curr
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

		def getSize(self):
			return self.getSizeOfTree( self.root )

		def getSizeOfTree(self, curr):
			if curr == None:
				return 0
			childrenSize = 0
			currSize = 0
			for i in range(3, -1, -1):
				childrenSize = self.getSizeOfTree(curr.ptr[i])
			for i in range(3):
				if not curr.data[i] == None:
					currSize += sys.getsizeof(curr.data[i])
			return childrenSize + currSize

		def find( self, word ):
			return self.findWord( word, self.root )

		def findWord( self, word, curr):
			if curr == None:
				return []
			hasWildcard = False
			for l in word:
				if l == '*':
					hasWildcard = True
					break
			if not hasWildcard:
				return [word]
			else:
				pass



infile = open( './dictionaryWin.txt', 'r')
mysteryWord = '*******'

wordlist = []
T = t234()
avlTree = pyavltree.AVLTree()
wlSize = 15

for i, item in enumerate( infile ):
	wordlist.append(item)
	if i >= wlSize:
		break

random.shuffle(wordlist)

# Start timing insert
tInsert_start = time.clock()
for w in wordlist:
	T.insert(w)
tInsert_end = time.clock()

aInsert_start = time.clock()
for w in wordlist:
	avlTree.insert(w)
aInsert_end = time.clock()

print T.printTree(1)
print avlTree.as_list(1)

print '---------------------------------'
print ' insert time '
print 'wordlist size, 234 tree insert time, avl tree insert time, 234 size'
print wlSize
print tInsert_end - tInsert_start
print aInsert_end - aInsert_start
print T.getSize()
print '---------------------------------'

# Testing t234 insert
# for i in range(10,100,10):
# 	T.insert(i)
# T.insert(35)
# T.insert(37)
# T.insert(38)
# T.insert(39)
# T.insert(25)
# T.insert(27)
# T.insert(26)
# T.insert(29)
# T.insert(11)
# T.insert(12)
# T.insert(13)
# T.insert(101)
# T.insert(96)
# T.insert(99)
# T.insert(98)
# T.insert(105)
# T.printTree()
# print '----------------'

# testWords = ['banana', 'apple', 'carrot', 'lettuce', 'pepper', 'kljdfg', 'sdflkj', 'fdgijerl', 'reoijht', 'troiu', 'ertoij', 'erwt', 'erty', 'ezz', 'exa', 'oerijfgdkm', 'sdff', 'qwer']

# for t in testWords:
# 	T.insert(t)




#print testWords
#print sorted( testWords )


# avlTree.insert( 10 )
# avlTree.insert( 20 )
# avlTree.insert( 30 )
# avlTree.insert( 40 )

# print avlTree.as_list(1)

