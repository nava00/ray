f=open("test.ppm",'w')
f.write("P3\n")
f.write("#test\n")
f.write("4 4\n") #width, height
f.write("4\n") #max color size

line=[ 1, 2,3 ,4 ];

line[0]="1 0 0 "*4+"\n" #rgb for each pixel
line[1]="2 2 0 "*4+"\n"
line[2]="2 2 0 "*4+"\n"
line[3]="4 0 3 "*4+"\n"

for l in line:
	f.write(l)
f.close()
