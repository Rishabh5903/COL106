class Empty(Exception):
    pass
class HeapPriorityQueue():
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
        if j > 0 and self._data[j] < self._data[parent]: #if parent is larger than jth element then jth element needs to be pushed up so we interchange jth element and its parent and recursively upheap it again
            self._swap(j, parent)
            self._upheap(parent) # recur at position of parent
    def _downheap(self, j): #pushes an element from top to suitable position down the heap
        if self._has_left(j): 
            left = self._left(j)
            small_child = left # initally assuming left child is smaller than right
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]: #then checking the smaller among right and left child assigning the index of smaller value to the small_child variable
                    small_child = right
            if self._data[small_child] < self._data[j]: #if the jth element is greater than small_child(i.e. greater than both children) then we need to push it down so swap j with small_child index
                self._swap(j, small_child)
                self._downheap(small_child) # recur at position of small child
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
    def min(self): #rerurns the minimum element of the heap without removing it 
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        key = self._data[0] #1st element of the list is the least element 
        return key
    def remove_min(self): #returns the least element as well as removes it from the heap
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        self._swap(0,len(self._data)-1) #swapping the 1st and last element of the list
        item=self._data.pop() #accessing the last element which is the smallest after swapping
        self._downheap(0) #downheaping the 1st element which is the last element after swapping to suitale position so that next smallesst element of the heap comes at top again
        return item #returning the smallest element 

def listCollisions(M,x,v,m,T):
    upcoming_coll=[-1]*len(M) #a list to store the times of upcoming collisions of any ith index
    times=[] #a list to store the values of times at which collision can take place initially to be used to build the heap at t=0
    ans=[] #final output list
    time=0 #variable storing the value of time elapsed at the moment a collision has completed which keeps on updating on every collision
    count=0 #variable storing the number of collisons that have took place
    prev_coll=[0]*len(M) # list storing the times of just previous collision of any ith index collision
    h=HeapPriorityQueue(times) # initiating heap using the initial time list
    for i in range(len(v)- 1): #appending possible collision times in the times list initially
        if v[i]-v[i+1]>0: #only in this case collison will be possible
            times.append([(x[i+1]-x[i])/(v[i]-v[i+1]),i]) #storing time of collsion and the index as a list
            upcoming_coll[i]=(x[i+1]-x[i])/(v[i]-v[i+1]) #updating the upcoming collision list
    for i in range(len(times)-1,-1,-1): #fast buildheap method to convert the times list into heap
        h._downheap(i)
    while time<T and count<m and not(h.is_empty()): 
        coll=h.remove_min() #extracting the collision  with least time i.e. one which will happen at first among all the possiblities inside the heap
        i=coll[1] #index of collision
        time=coll[0] #updating the time variable since the 0th index of heap element stores the time at which that collision will occur
        if time==upcoming_coll[i]:       #for handling those cases when the time of collision of any ith index might have changed in between and the heap might be containing multiple collisions of a single index. So we continue only if the value of time(same as 0th index of collision list stored in heap) is same as the upcoming value of time of collision which keeps on updating so has the correct time at which collision of ith index will take place.
            if time<=T: # we continue only if the elapsed time till this collsion is less than or equal to T.
                x[i]=x[i]+v[i]*(time-prev_coll[i]) #updating the position of ith particle using formula final position=intial position+velocity(difference between time of this collison and previous collsion) we the the difference of time because last time we updated the position when its collion took place so we need to update according to time difference till then only.
                x[i+1]=x[i]  #during collsion position of both particles will be same
                v1=v[i] #storing the value of v[i] to be used while updating v[i+1] because v[i] will be changed before v[i+1]
                v[i]=(M[i]-M[i+1])*v[i]/(M[i]+M[i+1])+(2*M[i+1])*v[i+1]/(M[i]+M[i+1]) #using formula given in reference link of assignment
                v[i+1]=(2*M[i])*v1/(M[i]+M[i+1])-(M[i]-M[i+1])*v[i+1]/(M[i]+M[i+1]) #using formula given in reference link of assignment
                prev_coll[i]=time #updating the prev_coll list to be used when collision takes place next time
                prev_coll[i+1]=time #updating the prev_coll list to be used when collision takes place next time
                ans.append((round(time,4),i,round(x[i],4))) #appending the time,index,potion of collsion in the final ans list
                count+=1 #incresing the count variable since collsion has took place
                if i>=1: #checking if the collsion of (i-1)th and ith particle after collsion of ith and (i+1)th is possible or not
                    if v[i-1]-v[i]>0: #if collision is possible
                        h.enqueue([time+(x[i]-x[i-1]-v[i-1]*(time-prev_coll[i-1]))/(v[i-1]-v[i]),i-1]) #we enqueue the time and index of (i-1)th index collision into the heap
                        upcoming_coll[i-1]=time+abs(x[i]-x[i-1]-v[i-1]*(time-prev_coll[i-1]))/(v[i-1]-v[i]) #and update the upcoming coll list as this collsion is not yet happened but can happen in future
                if i<=len(v)-3: #checking the same thing for possibility of (i+1)th and (i+2)th particle collision
                    if v[i+1]-v[i+2]>0:
                        h.enqueue([time+(x[i+2]+v[i+2]*(time-prev_coll[i+2])-x[i+1])/(v[i+1]-v[i+2]),i+1])
                        upcoming_coll[i+1]=time+(x[i+2]+v[i+2]*(time-prev_coll[i+2])-x[i+1])/(v[i+1]-v[i+2])
        else: #if the time value stored in heap element and upcoming coll list do not match that means, time of this collsion was updated and hence collision at this time is not possible and this element was removed from the heap so we continue to the next iteration without making any changes to position or velocity or heap or final ans list
            continue

    return(ans) #returning the final ans list