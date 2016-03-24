print "***Accumulator 1***"
#This is from the Iteration Chapter, section "The Accumulator Pattern"
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
accum = 0
for w in nums:
   accum = accum + w
print accum

print "Rewritten using the Reduce function"
print reduce(lambda x, y: x + y, nums)



print "***Accumulator 2***"
#from Iteration, Advanced Accumulation
things=(1, 2, 3, 4, 5, 6)

accum = []
for thing in things:
    accum.append(thing+1)
print accum

print "Rewritten using map"
print map((lambda value: value+1), things)


print "***Accumulator 3***"
#from problem 26, Fall 2014 exam

L = [{'a':1, 'b':2, 'd':11},
 {'a':4, 'b':5, 'e':11},
 {'a':7, 'b':8, 'f':11}]
 
for d in L:
    print d['b']

print "Rewritten using list comprehension" 
accum7= [value['b'] for value in L]

for value in accum7:
    print value

print "***Accumulator 4***"
#From function practice problems 2, from 3/1
def sum_a_list(lt):
    tot = 0
    for i in lt:
        tot = tot + i
    return tot

print sum_a_list([1,4,7,5])

print "Rewritten using list comprehension"
def list_sum(nums):
    return reduce(lambda x, y: x + y, nums)
    
print list_sum([1,4,7,5])


print "***Accumulator 5***"
#From Iteration, Lists and for Loops, textbook example
alist = [4,2,8,6,5]
blist = [ ]
for item in alist:
   blist.append(item+5)
print blist

print "Rewritten using map"
print map((lambda value: value+5), alist)





