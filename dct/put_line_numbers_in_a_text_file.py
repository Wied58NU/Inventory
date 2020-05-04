ifname = input("Enter file name: ")
ofname = open("out_"+ ifname, 'w')
num_lines = 0
with open(ifname, 'r') as f:
    for line in f:
        num_lines += 1
        print(str(num_lines) + " " + line, file = ofname)
