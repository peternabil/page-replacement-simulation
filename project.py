# we will impement
# FIFO, LRU, LFU, Second-Chance, Enhance Second-Chance, and optimal page
# each algorithm will have a distinct function
# and a main function that generates the input and calls the functions
#!/usr/bin/python
# -*- coding: utf-8 -*-


import random

def fifo(refrence_string,frame_num,page_num):
    """
        the first page to enter the table is the first to be replaced
        returns number of page faults
        paramarters:
        refrence_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    pass


def lru(refrence_string,frame_num,page_num):
    """
        the page that was used a long time ago at that exact moment is to be replaced
        returns number of page faults
        paramarters:
        refrence_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    pass

def lfu(refrence_string,frame_num,page_num):
    """
        look at the entire string untill this moment and find the page addressed the least
        if there's more than one take the first one entered
        returns number of page faults
        paramarters:
        refrence_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    pass

def second_chance(refrence_string,frame_num,page_num):
    """
        each page will have a used bit when it is first allocated this bit is set to 0 when it's addressed again while in the table the bit changes to 1 , if we want to replace
        the first page that meets us with a 0 used bit is removed and add the new page to the end of the queue , if we meet any page with 1 used bit before we find a page with 0
        used bit we change the used bit of that page to 0 and move it to the end of the queue
        returns number of page faults
        paramarters:
        refrence_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    memqueue = []
    selectdict = {}
    pagefault = 0
    for i in range(page_num):
        selectdict.update({i+1:0})

    for refrence in refrence_string:
        if refrence in memqueue:
            selectdict[refrence]=1
        elif len(memqueue)==frame_num:
            pagefault+=1
            while(1):
                x = memqueue[0]
                if selectdict[x]==0:
                    memqueue[0] = refrence
                    break
                else:
                    # print("give {} a second chance".format(memqueue[0]))
                    selectdict[x] = 0
                    memqueue.remove(x)
                    memqueue.append(x)
        else:
            pagefault+=1
            memqueue.append(refrence)
        # print(memqueue)
        # print(selectdict)
    return pagefault
    # print(selectdict)

def enhanced_second_chance(refrence_string,frame_num,page_num):
    """
        each page will have two bits added to them one used bit (same as second_chance)
        and the other is the modified bit this bit will be put randomly , the priority for
        replacement is as follows:
        1. (0, 0) neither recently used nor modified—best page to replace
        2. (0, 1) not recently used but modified—not quite as good, because the
        page will need to be written out before replacement
        3. (1, 0) recently used but clean—probably will be used again soon
        4. (1, 1) recently used and modified—probablywill be used again soon, and
        the page will be need to be written out to disk before it can be replaced
        returns number of page faults
        paramarters:
        refrence_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    pagefault = 0
    memqueue0 = []
    memqueue1 = []
    memqueue2 = []
    memqueue3 = []
    selectdict = {}
    for page in range(page_num):
        selectdict.update({page+1:[0,random.randint(0,1)]})
    # print(selectdict)
    for refrence in refrence_string:
        # print(memqueue0)
        # print(memqueue1)
        # print(memqueue2)
        # print(memqueue3)
        if refrence in memqueue0:
            memqueue0.remove(refrence)
            memqueue2.append(refrence)
            selectdict[refrence][0] = 1
        elif refrence in memqueue1:
            memqueue1.remove(refrence)
            memqueue3.append(refrence)
            selectdict[refrence][0] = 1
        elif refrence in memqueue2 or refrence in memqueue3:
            continue
        else:
            pagefault+=1
            if len(memqueue0)+len(memqueue1)+len(memqueue2)+len(memqueue3) < frame_num:
                # print("{} there's space in buffer".format(refrence))
                if selectdict[refrence][1] == 0:
                    memqueue0.append(refrence)
                else:
                    memqueue1.append(refrence)

            elif len(memqueue0) != 0:
                # print("we will add {} in queue00 and remove {}".format(refrence,memqueue0[0]))
                memqueue0.remove(memqueue0[0])
                if selectdict[refrence][1] == 0:
                    memqueue0.append(refrence)
                else:
                    memqueue1.append(refrence)

            elif len(memqueue1) !=0:
                # print("we will add {} in queue00 and remove {}".format(refrence,memqueue1[0]))
                memqueue1.remove(memqueue1[0])
                if selectdict[refrence][1] == 0:
                    memqueue0.append(refrence)
                else:
                    memqueue1.append(refrence)

            elif len(memqueue2) !=0:
                # print("we will add {} in queue00 and remove {}".format(refrence,memqueue2[0]))
                selectdict[memqueue2[0]][0] = 0
                memqueue2.remove(memqueue2[0])
                if selectdict[refrence][1] == 0:
                    memqueue0.append(refrence)
                else:
                    memqueue1.append(refrence)
                for item in memqueue2:
                    selectdict[item][0] = 0
                    memqueue0.append(item)
                    memqueue2.remove(item)
                    selectdict[item][0] = 0

            elif len(memqueue3) !=0:
                # print("we will add {} in queue00 and remove {}".format(refrence,memqueue3[0]))
                selectdict[memqueue3[0]][0] = 0
                memqueue3.remove(memqueue3[0])
                if selectdict[refrence][1] == 0:
                    memqueue0.append(refrence)
                else:
                    memqueue1.append(refrence)
                for item in memqueue3:
                    selectdict[item][0] = 0
                    memqueue1.append(item)
                    memqueue3.remove(item)
                    selectdict[item][0] = 0

    return pagefault

def optimal(refrence_string,frame_num,page_num):
    """
        we calculate how much will each page be used and the one which is least used is
        the one we replace
        returns number of page faults
        paramarters:
        refrence_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    frequency = {}
    memqueue = []
    pagefault = 0
    for item in refrence_string:
        frequency.update({item:0})
    for item in refrence_string:
        frequency[item]+=1
    for refrence in refrence_string:
        if refrence in memqueue:
            continue
        if len(memqueue) < frame_num:
            memqueue.append(refrence)
            pagefault+=1
        else:
            pagefault+=1
            tempdict = {}
            for memitem in memqueue:
                tempdict.update({memitem:frequency[memitem]})
            replacement = min(tempdict, key=tempdict.get)
            memqueue[memqueue.index(replacement)]=refrence

    return pagefault

def printing(refrence_string):
    refrence_string_modified = ""
    for i in range(len(refrence_string)-1):
        refrence_string_modified+=str(refrence_string[i])+"-->"
    refrence_string_modified+=str(refrence_string[-1])
    return refrence_string_modified


def main():
    """
        will generate a random page refrence string, random number of frames (1 to 20) and random number of pages (0 to 99)
        and call all the past functions then prints the computed page fault number

    """
    page_num = random.randint(0,99)
    frame_num = random.randint(1,20)
    refrence_string = []
    refrence_string_length = random.randint(10,50)
    for i in range(refrence_string_length):
        refrence_string.append(random.randint(1,page_num))

    #for debugging
    print("the page number  : {} ".format(page_num))
    print("the frame number : {} ".format(frame_num))
    print("the refrence string length : {} ".format(refrence_string_length))
    print("the refrence string {}".format(printing(refrence_string)))
    print("The page faults : ")
    print("using FIFO : {}".format(fifo(refrence_string,frame_num,page_num)))
    print("using LRU : {}".format(lru(refrence_string,frame_num,page_num)))
    print("using LFU : {}".format(lfu(refrence_string,frame_num,page_num)))
    print("using Second-Chance : {}".format(second_chance(refrence_string,frame_num,page_num)))
    print("using enhanced Second Chance : {}".format(enhanced_second_chance(refrence_string,frame_num,page_num)))
    print("using Optimal : {}".format(optimal(refrence_string,frame_num,page_num)))

main()
