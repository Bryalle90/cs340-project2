from avl import pyavltree
import time
import random

infile = open( './dictionaryWin.txt', 'r')
wordlist = []
mysteryWord = '*******'
for i, item in enumerate( infile ):
	wordlist.append(item)
	if i == 700000:
		break

random.shuffle(wordlist)

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
				#shift data
				newNode = node()
				newNode.data[0] = nodePtr.ptr[index].data[2]
				nodePtr.data[promoteIndex] = promoteValue
				nodePtr.ptr[index].data[1] = None
				nodePtr.ptr[index].data[2] = None
				#shift pointers
				newNode.ptr[0] = nodePtr.ptr[index].ptr[2]
				newNode.ptr[1] = nodePtr.ptr[index].ptr[3]
				nodePtr.ptr[index].ptr[2] = None
				nodePtr.ptr[index].ptr[3] = None
				nodePtr.ptr[index+1] = newNode

		def insert( self, data ):
				#check the split for root
				self.root = self.splitRoot( self.root )
				curr = self.root
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

		def printTree( self ):
				self.printRecursive( self.root, 0 , 0 )

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



T = t234()
for i in range(10,100,10):
	T.insert(i)
	T.printTree()
	print '----------------'
T.insert(35)
T.printTree()
print '----------------'
T.insert(37)
T.printTree()
print '----------------'
T.insert(38)
T.printTree()
print '----------------'
T.insert(39)
T.printTree()
print '----------------'

testWords = ['banana', 'apple', 'carrot', 'lettuce', 'pepper', 'kljdfg', 'sdflkj', 'fdgijerl', 'reoijht', 'troiu', 'ertoij', 'erwt', 'erty', 'ezz', 'exa', 'oerijfgdkm', 'sdff', 'qwer']

#print testWords
#print sorted( testWords )

print '----------------'

avlTree = pyavltree.AVLTree()

avlTree.insert( 10 )
avlTree.insert( 20 )
avlTree.insert( 30 )
avlTree.insert( 40 )

print avlTree.as_list(1)