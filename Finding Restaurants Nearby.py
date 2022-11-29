class treeNode(object): #node class with desired properties to use later
    def __init__(self,value):
        self.range=None #to store the range of x coordinate in the tree
        self.value=None #to return the value stored at a node
        self.l=None #to assign the left child
        self.r=None #to assign the right child

    def mergesort(self,node): #mergesroting function to solt the list atores at node
        arr=node.value #return the list stored at node
        if len(arr)>1:
            mid=len(arr)//2 
            L=arr[:mid] #left half
            l1=treeNode(L) #new node storing left half of the list
            l1.value=L #assigning the value of node
            R=arr[mid:] #right half
            r1=treeNode(R) #new node storing right half of the list
            r1.value=R #assigning the value of node
            node.l=l1.mergesort(l1) #assigning the left of the node as the sorted list of left half of the list
            node.r=r1.mergesort(r1) #assigning the left of the node as the sorted list of left half of the list
            node.value=merge(node.l.value,node.r.value) #merging the two sorted lists of left and right half and assigning the value of node to it
            if len(node.l.value)==1: #assigning the range of left of node when its length is 1 i.e. it is the leaf node , also the base case for assigning ranges of nodes
                node.l.range=node.l.value[0].range #already range was stored during the creation of these leaf nodes 
            if len(node.r.value)==1:
                node.r.range=node.r.value[0].range
            node.range=(node.l.range[0],node.r.range[1]) #for assigning ranges of other nodes as the lower limit of range of left node to the higher limit of range of right node
            i=j=k=0
            while i<len(L) and j< len(R):
                if L[i].value[0][1]<=R[j].value[0][1]: #comparing the two lists and changing the value of that index in arr accordingly
                    arr[k]=L[i]
                    i+=1
                else:
                    arr[k]=R[j]
                    j+=1
                k+=1
            while i<len(L): #for remaining elements in the bigger list after comparison
                arr[k]=L[i]
                i+=1
                k+=1
            while j<len(R): #for remaining elements in the bigger list after comparison
                arr[k]=R[j]
                j+=1
                k+=1
        
        node.value=arr #creating new node to store the 
        return node #returns the node containing the y sorted list

def merge(l1,l2): #for merging two sorted lists
    l=[]
    n1=len(l1)
    n2=len(l2)
    i=0
    j=0
    while i<n1 and j<n2:
        if l1[i].value[0][1]<=l2[j].value[0][1]: #comparing the two lists and appending the value in teh final list accordingly
            l.append(l1[i])
            i+=1
        else:
            l.append(l2[j])
            j+=1
    while i<n1:
        l.append(l1[i]) #for remaining elements in the bigger list after comparison
        i+=1
    while j<n2:
        l.append(l2[j]) #for remaining elements in the bigger list after comparison
        j+=1
    return l

def search(arr, x,o): #for the searching the index of just higher and just lower y coordinate than x(it is also a y coordinate) where o=1 is for jsut higher and o=-1 for just lower using binary search
    if arr[0].value[0][1]>=x and o==1: #if the lowest element of arr is greater than x then all elements will be greater than x so just higher will be at index 0
        return 0
    elif arr[-1].value[0][1]<=x and o==-1: #if the lowest element of arr is greater than x then all elements will be greater than x so just higher will be at index 0
        return len(arr)-1
    if arr[-1].value[0][1]<x and o==1: #if largest element of list is lower than x then none of the elements will be larger than x so return -1
        return -1
    elif arr[0].value[0][1]>x and o==-1: #if smallest element of list is larger than x then none of the elements will be smaller than x so return -1
        return -1
    else:
        if o==1: #searching the just higher element
            low = 0 #common binary search code
            high = len(arr) - 1
            mid = 0
            while low <= high:
                mid = (high + low) // 2
                if arr[mid].value[0][1] < x: 
                    if mid<len(arr)-1 and o==-1:
                        if arr[mid+1].value[0][1]>x:
                            return mid
                    low = mid + 1
                elif arr[mid].value[0][1] >= x: #if mid element is greater than x and the previous element is less than x that means mid is the jsut higher element than x
                    if mid>0 and o==1:
                        if arr[mid-1].value[0][1]<x:
                            return mid
                    high = mid - 1
            return -1
        else: #searching the just lower element
            low = 0
            high = len(arr) - 1
            mid = 0
            while low <= high:

                mid = (high + low) // 2
                if arr[mid].value[0][1] <= x: #if mid element is less than x and the previous element is higher than x that means mid is the jsut lower element than x
                    if mid<len(arr)-1 and o==-1:
                        if arr[mid+1].value[0][1]>x: 
                            return mid
                    low = mid + 1
                elif arr[mid].value[0][1] > x:
                    if mid>0 and o==1:
                        if arr[mid-1].value[0][1]<x:
                            return mid
                    high = mid - 1
            return -1

class PointDatabase(object): #main class
    def __init__(self,pointlist):
        if len(pointlist)==0: 
            self._data=[]
        else:
            self._root=None #root node
            self._data=pointlist 
            self._data=sorted(self._data) #sorting the input pointlist w.r.t x coordinates
            li=[]
            for i in self._data:
                a=treeNode([i]) #storing each point inside a list as a node
                a.value=[i] #assigning its value
                a.range=(i[0],i[0]) #assigning the range of single elements inside the list to be used later while merging them adn assignig its value
                li.append(a)
            self._data=li #updating self._data
            self.build() #calling the build function to build the data structure storing all the points
    def build(self): #build function to build the data structure storing all the points
        a=treeNode(self._data) #creating another node for the base list
        a.value=self._data #assigning value
        self._root=a.mergesort(a) #assigning the node containing sorted list of the base list as the value of root node
    def searchNearby(self,q,d): #nearby searching function
        if len(self._data)==0:
            return []
        if d==0: #if d is 0 then return empty list because no point can be at exact d distance away from q
            return []
        x1=q[0]-d #lower limit of allowed x values
        x2=q[0]+d #upper limit of allowed x values
        y1=q[1]-d #lower limit of allowed y values
        y2=q[1]+d #upper limit of allowed y values
        ans=[] #final output list
        def search_2(node,x1,x2,y1,y2,ans): # helper function to recursively search nodes in the data structure for fiding the nodes with appropriate range of x
            if node.range[0]>x2 or node.range[1]<x1: #the allowed intervals is outside the range of x in node so exit from the function
                return 
            elif node.range[0]>=x1 and node.range[1]<=x2: # the range of x is completely indide the allowed range so search for suitable y and append in ans
                i=search(node.value, y1, 1) #searching the index of element just higher than y1
                j=search(node.value, y2, -1) #searching the index of element just lower than y2
                if i!=-1 and j!=-1 and i<=j: #if i and j have suitable values
                    for k in range(i,j+1):
                        ans.append(node.value[k].value[0]) #apppending the correct points in the final list
                return 
            
            else:
                if node.l!=None :
                    search_2(node.l, x1, x2, y1, y2, ans) #recursively searching on the left child node
                if node.r!=None :
                    search_2(node.r, x1, x2, y1, y2, ans) #recursively searching on the right child node
        search_2(self._root, x1, x2, y1, y2, ans) #calling the function on root node
        return ans #returning the final ans