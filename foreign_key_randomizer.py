import random

def return_random_stevilo():
    i = 1
    outfile = open('numbersmakesssss.txt', 'w')

    while i < 1000:
    #Write 12 random intergers in the range of 1-100 on one line
    #to the file.
        num = random.randint(1500, 2000)
        outfile.write("UPDATE igralci_data SET klub =" + str(num) + " WHERE id=" + str(i) + ";")
        i+=1
    #Close the file.
    outfile.close()
    print('Data written to numbersmake.txt')

