class Empty(Exception):
    pass
class HeapPriorityQueue(): #heap class for extarcting the max capcacity of packets
    #------------------------------ nonpublic behaviors ------------------------------
    def _parent(self, j):
        return (j-1) // 2 #returns the index of parent element of jth element in the heap
    def _left(self, j): 
        return 2*j+1 #returns the index of left element of jth element in the heap
    def _right(self, j):
        return 2*j+2 #returns the index of right element of jth element in the heap
    def _has_left(self, j): #returns whether the jth element has a left element in the heap or not
        return self._left(j) < len(self._data) # if index of left element of jth element is less than the length of list contaning heap elements then left element will exist and returns true otherwise false
    def _has_right(self, j): #returns whether the jth element has a right element in the heap or not
        return self._right(j) < len(self._data)  # if index of right element of jth element is less than the length of list contaning heap elements then right element will exist and returns true otherwise false
    def _swap(self, i, j): #swaps the elements ith and jth index in the heap 
        self._data[i], self._data[j] = self._data[j], self._data[i] #interchanging ith  and jth elements
    def _upheap(self, j): #pushes an element from bottom to suitable position up inside the heap
        parent = self._parent(j) #accessign the parent of jth element
        if j > 0 and self._data[j][1] > self._data[parent][1]: #if parent is samller than jth element then jth element needs to be pushed up so we interchange jth element and its parent and recursively upheap it again
            self._swap(j, parent)
            self._upheap(parent) # recur at position of parent
    def _downheap(self, j): #pushes an element from top to suitable position down the heap
        if self._has_left(j): 
            left = self._left(j)
            large_child = left # initally assuming left child is larger than right
            if self._has_right(j):
                right = self._right(j)
                if self._data[right][1] > self._data[left][1]: #then checking the larger among right and left child assigning the index of larger value to the large_child variable
                    large_child = right
            if self._data[large_child][1] > self._data[j][1]: #if the jth element is samller than large_child then we need to push it down so swap j with large_child index
                self._swap(j, large_child)
                self._downheap(large_child) # recur at position of large child
#------------------------------ public behaviors ------------------------------
    def __init__(self,l): 
        self._data=l #initially taking a list l which needs to be converted into a binary heap later
    def __len__(self):
        return len(self._data) #returns lenth of the list containing elements of the binary heap
    def is_empty(self): 
        return len(self) == 0 #returns true if heap is empty
    def enqueue(self,key): #function to insert an element inside the heap
        self._data.append(key)
        self._upheap(len(self._data)-1) #since it was appended at the last index so we upheap the last index of the list
    def max(self): #rerurns the maximum element of the heap without removing it 
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        key = self._data[0] #1st element of the list is the max element 
        return key
    def remove_max(self): #returns the maximum element as well as removes it from the heap
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        self._swap(0,len(self._data)-1) #swapping the 1st and last element of the list
        item=self._data.pop() #accessing the last element which is the largest after swapping
        self._downheap(0) #downheaping the 1st element which is the last element after swapping to suitale position so that next largest element of the heap comes at top again
        return item #returning the largest element 
def findMaxCapacity(n,l,a,b): #main function
    if a==b:
        return (float('inf'),[a])
    l1=[] #adjacency list
    for i in range(n):
        l1.append([]) #empty lists for each vertex
    for x in l:
        l1[x[0]].append((x[1],x[2],x[0])) #appending the edges to both adjacency lists of two vertices
        l1[x[1]].append((x[0],x[2],x[1]))
    cap=float('inf') #initliasing the capacity of packet that needs to be returned with infinity
    prev_list=[-1]*n #a list which stores the source vertices of all the edges that we came across to be used later while printing the final path
    prev_list[a]=-2 #initialising the source vertex with -2
    ans=[] #path list
    h=HeapPriorityQueue(l1[a]) #creating heap list of the edges originating from the source vertex a 
    for i in range(len(l1[a])-1,-1,-1): #fast buildheap method
        h._downheap(i)
    while True: #loop runs till we get the destination vertex(then we break it)
        node=h.remove_max() # #extracting max capacity packets from the heap
        cap=min(cap,node[1]) #updating the cap variable since it is the min of all the capacities along the best(larget capacity) path
        if node[0]==b: #when we reach the destination vertex
            prev_list[b]=node[2] #update the source of last edge to reach dest
            break #exit from loop
        elif prev_list[node[0]]!=-1: #if the vertex is already visited then nothings needs to be done
            continue
        else:
            for i in l1[node[0]]: # if we get a new vertex other than dest vertex then we enquque the edges of that vertex in the heap
                h.enqueue(i) 
            prev_list[node[0]]=node[2] #update the sorce vertex of the edge
    temp=prev_list[b] #temporary variable which stores the value of soruce vertices for tracking the path through which we reached the dest, initialising it with source of dest vertex
    ans.append(b) #appending the dest vertex in fianl path list
    while prev_list[temp]!=-2: #backtracking the source vertices to get the path and stopping when reached the vertex a(since it's source was stored as -2)
        ans.append(temp) #appending the path in ans list
        temp=prev_list[temp] #updating temp
    ans.append(temp) #appending a when loop stops
    ans.reverse() #reversing to get the path from a-b
    return (cap,ans) #returning cap and path