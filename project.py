# we will impement
# FIFO, LRU, LFU, Second-Chance, Enhance Second-Chance, and optimal page
# each algorithm will have a distinct function
# and a main function that generates the input and calls the functions
#!/usr/bin/python3
# -*- coding: utf-8 -*-


import random
# import pylab


def fifo(reference_string, frame_num, page_num):
    """
        the first page to enter the table is the first to be replaced
        returns number of page faults
        paramarters:
        reference_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    frames = [-1] * frame_num
    j = 0
    faults = 0
    print("-1 MEANS AN EMPTY FRAME")
    for i in reference_string:
        if i in frames:
            continue
        j = j % frame_num
        frames[j] = i
        j += 1
        faults += 1
        print("the Memory : {}".format(frames))
    return faults


def lru(reference_string, frame_num, page_num):
    """
        the page that was used a long time ago at that exact moment is to be replaced
        returns number of page faults
        paramarters:
        reference_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    frames = [-1] * frame_num
    recently = [0] * frame_num
    faults = 0
    print("-1 MEANS AN EMPTY FRAME")
    for i in reference_string:
        if i in frames:
            j = max(recently)
            recently[frames.index(i)] = j + 1
            continue
        k = min(recently)
        j = max(recently)
        frames[recently.index(k)] = i
        recently[recently.index(k)] = j + 1
        faults += 1
        print("the Memory : {}".format(frames))
    return faults


def lfu(reference_string, frame_num, page_num):
    """
        look at the entire string untill this moment and find the page addressed the least
        if there's more than one take the first one entered
        returns number of page faults
        paramarters:
        reference_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    frames = [-1] * frame_num
    frequency = [0] * frame_num
    faults = 0
    counter=0
    print("-1 MEANS AN EMPTY FRAME")
    for i in reference_string:
        counter += 1
        if i in frames:
            frequency[frames.index(i)] += 1
            continue
        k = min(frequency)
        if faults >= frame_num:
            minimums = []
            for j in range(len(frequency)):
                if frequency[j] == k:
                    minimums.append(frames[j])
            if len(minimums) > 1:
                for m in reversed(range(counter)):
                    if reference_string[m] in frames and reference_string[m] in minimums:
                        minimums.pop(minimums.index(reference_string[m]))
                        if len(minimums) == 1:
                            break
                frequency[frames.index(minimums[0])] = 1
                frames[frames.index(minimums[0])] = i
                faults += 1
                print("the Memory : {}".format(frames))
                continue
        frames[frequency.index(k)] = i
        frequency[frequency.index(k)] = 1
        faults += 1
        print("the Memory : {}".format(frames))
    return faults


def second_chance(reference_string, frame_num, page_num):
    """
        each page will have a used bit when it is first allocated this bit is set to 0 when it's addressed again while in the table the bit changes to 1 , if we want to replace
        the first page that meets us with a 0 used bit is removed and add the new page to the end of the queue , if we meet any page with 1 used bit before we find a page with 0
        used bit we change the used bit of that page to 0 and move it to the end of the queue
        returns number of page faults
        paramarters:
        reference_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    memqueue = []
    selectdict = {}
    pagefault = 0
    for i in range(page_num):
        selectdict.update({i + 1: 0})
    # print("The used and modified bits of each page in the system :\n{}".format(selectdict))
    for reference in reference_string:
        if reference in memqueue:
            selectdict[reference] = 1
        elif len(memqueue) == frame_num:
            pagefault += 1
            while(1):
                x = memqueue[0]
                if selectdict[x] == 0:
                    memqueue[0] = reference
                    break
                else:
                    # print("give {} a second chance".format(memqueue[0]))
                    selectdict[x] = 0
                    memqueue.remove(x)
                    memqueue.append(x)
        else:
            pagefault += 1
            memqueue.append(reference)
        # print(memqueue)
        # print(selectdict)
        print("The used and modified bits of each page in the system :\n{}".format(selectdict))
        print()
        print("the Memory : {}".format(memqueue))
        print()
    return pagefault
    # print(selectdict)


def enhanced_second_chance(reference_string, frame_num, page_num):
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
        reference_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    pagefault = 0
    memqueue = []
    memqueue0 = []
    memqueue1 = []
    memqueue2 = []
    memqueue3 = []
    selectdict = {}
    for page in range(page_num):
        selectdict.update({page + 1: [0, random.randint(0, 1)]})
    # print("The used and modified bits of each page in the system :\n{}".format(selectdict))
    for reference in reference_string:
        # print(memqueue0)
        # print(memqueue1)
        # print(memqueue2)
        # print(memqueue3)
        if reference in memqueue0:
            memqueue0.remove(reference)
            memqueue2.append(reference)
            selectdict[reference][0] = 1
        elif reference in memqueue1:
            memqueue1.remove(reference)
            memqueue3.append(reference)
            selectdict[reference][0] = 1
        elif reference in memqueue2 or reference in memqueue3:
            continue
        else:
            pagefault += 1
            if len(memqueue0) + len(memqueue1) + len(memqueue2) + len(memqueue3) < frame_num:
                # print("{} there's space in buffer".format(reference))
                if selectdict[reference][1] == 0:
                    memqueue0.append(reference)
                else:
                    memqueue1.append(reference)

            elif len(memqueue0) != 0:
                # print("we will add {} in queue00 and remove {}".format(reference,memqueue0[0]))
                memqueue0.remove(memqueue0[0])
                if selectdict[reference][1] == 0:
                    memqueue0.append(reference)
                else:
                    memqueue1.append(reference)

            elif len(memqueue1) != 0:
                # print("we will add {} in queue00 and remove {}".format(reference,memqueue1[0]))
                memqueue1.remove(memqueue1[0])
                if selectdict[reference][1] == 0:
                    memqueue0.append(reference)
                else:
                    memqueue1.append(reference)

            elif len(memqueue2) != 0:
                # print("we will add {} in queue00 and remove {}".format(reference,memqueue2[0]))
                selectdict[memqueue2[0]][0] = 0
                memqueue2.remove(memqueue2[0])
                if selectdict[reference][1] == 0:
                    memqueue0.append(reference)
                else:
                    memqueue1.append(reference)
                for item in memqueue2:
                    selectdict[item][0] = 0
                    memqueue0.append(item)
                    memqueue2.remove(item)
                    selectdict[item][0] = 0

            elif len(memqueue3) != 0:
                # print("we will add {} in queue00 and remove {}".format(reference,memqueue3[0]))
                selectdict[memqueue3[0]][0] = 0
                memqueue3.remove(memqueue3[0])
                if selectdict[reference][1] == 0:
                    memqueue0.append(reference)
                else:
                    memqueue1.append(reference)
                for item in memqueue3:
                    selectdict[item][0] = 0
                    memqueue1.append(item)
                    memqueue3.remove(item)
                    selectdict[item][0] = 0
        memqueue = []
        for i in memqueue0:
            memqueue.append(i)
        for i in memqueue1:
            memqueue.append(i)
        for i in memqueue2:
            memqueue.append(i)
        for i in memqueue3:
            memqueue.append(i)
        print("The used and modified bits of each page in the system :\n{}".format(selectdict))
        print()
        print("the Memory : \n queue00 : {}\nqueue01 : {}\nqueue10 : {}\nqueue11 : {}\n".format(memqueue0, memqueue1, memqueue2, memqueue3))

    return pagefault


def optimal(reference_string, frame_num, page_num):
    """
        we calculate how much will each page be used and the one which is least used is
        the one we replace
        returns number of page faults
        paramarters:
        reference_string : list of the calls of the pages
        frame_num : integer representing the number of frames
        page_num : integer representing the number of pages
    """
    frequency = {}
    memqueue = []
    pagefault = 0
    for item in reference_string:
        if item in frequency.keys():
            frequency[item] += 1
        else:
            frequency.update({item: 0})
    print(frequency)
    for reference in reference_string:
        if reference in memqueue:
            continue
        if len(memqueue) < frame_num:
            memqueue.append(reference)
            pagefault += 1
        else:
            pagefault += 1
            tempdict = {}
            minfreq = max(frequency, key=frequency.get)
            for memitem in memqueue:
                if frequency[memitem] < frequency[minfreq]:
                    minfreq = memitem

            memqueue[memqueue.index(minfreq)] = reference
        print("the Memory : {}".format(memqueue))
    return pagefault


def printing(reference_string):
    reference_string_modified = ""
    for i in range(len(reference_string) - 1):
        reference_string_modified += str(reference_string[i]) + "-->"
    reference_string_modified += str(reference_string[-1])
    return reference_string_modified


def main():
    """
        will generate a random page reference string, random number of frames (1 to 20) and random number of pages (0 to 99)
        and call all the past functions then prints the computed page fault number
    """
    page_num = random.randint(0, 99)
    frame_num = random.randint(1, 20)
    reference_string = []
    reference_string_length = random.randint(10, 50)
    for i in range(reference_string_length):
        reference_string.append(random.randint(1, page_num))
    # for debugging
    # page_num = 10
    # frame_num = 5
    # reference_string = [2, 2, 3, 4, 5, 6, 6, 3, 5, 7, 8]
    print("the page number  : {} ".format(page_num))
    print("the frame number : {} ".format(frame_num))
    print("the reference string length : {} ".format(reference_string_length))
    print("the reference string {}".format(printing(reference_string)))
    print("The page faults : ")
    print("Using FIFO : ")
    print("The Page Faults = {} ".format(fifo(reference_string, frame_num, page_num)))
    print("Using LRU : ")
    print("The Page Faults = {} ".format(lru(reference_string, frame_num, page_num)))
    print("Using LFU : ")
    print("The Page Faults = {} ".format(lfu(reference_string, frame_num, page_num)))
    print("Using Second-Chance : ")
    print("The Page Faults = {} ".format(second_chance(reference_string, frame_num, page_num)))
    print("Using enhanced Second Chance : ")
    print("The Page Faults = {} ".format(enhanced_second_chance(reference_string, frame_num, page_num)))
    print("Using Optimal : ")
    print("The Page Faults = {} ".format(optimal(reference_string, frame_num, page_num)))

    # fifolist = []
    # lrulist = []
    # lfulist = []
    # second_chance_list = []
    # enhanced_second_chance_list = []
    # optimallist = []
    # page_num = int(input("Enter the number of pages : "))
    # frame_num = int(input("Enter the number of frames : "))
    # reference_string = []
    # list = []
    # for i in range(1,200):
    #     list.append(i)
    #     for x in range(i):
    #        reference_string.append(random.randint(1,page_num))
    #     fifolist.append(fifo(reference_string,frame_num,page_num))
    #     lrulist.append(lru(reference_string,frame_num,page_num))
    #     lfulist.append(lfu(reference_string,frame_num,page_num))
    #     second_chance_list.append(second_chance(reference_string,frame_num,page_num))
    #     enhanced_second_chance_list.append(enhanced_second_chance(reference_string,frame_num,page_num))
    #     optimallist.append(optimal(reference_string,frame_num,page_num))
    # pylab.figure(1)
    # pylab.xlabel('reference string length')
    # pylab.ylabel('page faults')
    # pylab.plot(list,fifolist,label="FIFO")
    # pylab.plot(list,lrulist,label="LRU")
    # pylab.plot(list,lfulist,label="LFU")
    # pylab.plot(list,second_chance_list,label="Second Chance")
    # pylab.plot(list,enhanced_second_chance_list,label="Enhanced Second Chance")
    # pylab.plot(list,optimallist,label="Optimal")
    # pylab.legend(loc = 'best')
    # pylab.show()


main()

# page_num = 10
# frame_num = 5
# reference_string = [2,2,3,4,5,6,6,3,5,7,8]
# print(frame_num)
# print(reference_string)
# print(optimal(reference_string,frame_num,page_num))


# # page_num = random.randint(0,99)
# page_num = 20
# # frame_num = random.randint(1,20)
# frame_num = 3
# reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
# # reference_string_length = random.randint(10,50)
# #reference_string_length = 20
# # for i in range(reference_string_length):
# #   reference_string.append(random.randint(1,page_num))
