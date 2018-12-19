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
    """
    pass


def lru(refrence_string,frame_num,page_num):
    """
        the page that was used a long time ago at that exact moment is to be replaced
        returns number of page faults
    """
    pass

def lfu(refrence_string,frame_num,page_num):
    """
        look at the entire string untill this moment and find the page addressed the least
        if there's more than one take the first one entered
        returns number of page faults
    """
    pass

def second_chance(refrence_string,frame_num,page_num):
    """
        each page will have a used bit when it is first allocated this bit is set to 0 when it's addressed again while in the table the bit changes to 1 , if we want to replace
        the first page that meets us with a 0 used bit is removed and add the new page to the end of the queue , if we meet any page with 1 used bit before we find a page with 0
        used bit we change the used bit of that page to 0 and move it to the end of the queue
        returns number of page faults
    """
    pass

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
    """
    pass

def optimal(refrence_string,frame_num,page_num):
    """
        we calculate how much will each page be used and the one which is least used is
        the one we replace
        returns number of page faults
    """
    pass



def main():
    """
        will generate a random page refrence string, random number of frames (1 to 20) and random number of pages (0 to 99)
        and call all the past functions then prints the computed page fault number

    """
    page_num = random.randint(0,99)
    frame_num = random.randint(1,20)
    refrence_string = ""
    refrence_string_length = random.randint(10,50)
    for i in range(refrence_string_length-1):
        refrence_string+=str(random.randint(1,page_num))+"->"
    refrence_string+=str(random.randint(1,page_num))

    #for debugging
    print("the page number  : {} ".format(page_num))
    print("the frame number : {} ".format(frame_num))
    print("the refrence string length : {} ".format(refrence_string_length))
    print("the refrence string {}".format(refrence_string))

    print("The page faults : ")
    print("using FIFO : {}".format(fifo(refrence_string,frame_num,page_num)))
    print("using LRU : {}".format(lru(refrence_string,frame_num,page_num)))
    print("using LFU : {}".format(lfu(refrence_string,frame_num,page_num)))
    print("using Second-Chance : {}".format(second_chance(refrence_string,frame_num,page_num)))
    print("using enhanced Second Chance : {}".format(enhanced_second_chance(refrence_string,frame_num,page_num)))
    print("using Optimal : {}".format(optimal(refrence_string,frame_num,page_num)))

main()
