import numpy,math
#
#comment 3
class sphere(object):
	def __init__(self, color, radius, center):
		self.center=center;
		self.color=color;
		self.radius=radius;
	def intersection(self,line):
		p,v=line;
		#given a line=(p,v) does it intersect the sphere
		a=sum([v[i]**2 for i in range(3)])
		b=2*sum([p[i]*v[i]-v[i]*self.center[i] for i in range(3)])
		c=(sum([p[i]**2+self.center[i]**2-2*p[i]*self.center[i] for i in range(3)])-self.radius**2)
		ans=roots(a,b,c)
		if(ans==None):
				return -1 #won't be counted as valid distance
		return min(ans)
class plane(object):
	def __init__(self, color,eq):		
		self.color=color;
		self.a=eq[0]
		self.b=eq[1]
		self.c=eq[2]
		self.d=eq[3]
	def intersection(self,ray):
		p,v=ray
		den=self.a*v[0]+self.b*v[1]+self.c*v[2];
		if(not den==0):
			t=-(self.a*p[0]+self.b*p[1]+self.c*p[2]+self.d)/den
			return(t)
		return -1 #won't be counted as valid distance
class pixel(object):
	def __init__(self,x,y,color):
		self.x=x;
		self.y=y;
		self.color=color; #[r,g,b]
	def __repr__(self):
		if max(self.color)==0: return ' ' #black
		c=numpy.argmax(self.color) #dominant color
		if c==0: return 'r'
		if c==1: return 'g'
		if c==2: return 'b'

def roots(a,b,c):
	"returns a pair of roots of ax^2+bx+c, or None"
	disc=b*b-4*a*c
	if(disc<0):
		return(None)
	return([(-b+math.sqrt(disc))/(2*a),(-b-math.sqrt(disc))/(2*a)])

def screen_init(lims,bg_color):
	return([[pixel(i,j,bg_color) for i in range(lims[0],lims[1])] \
		for j in range(lims[0],lims[1])])

def screen_print(screen):
	#primitive screen printing
	for row in screen:
		for col in row:
			print col,
		print

def screen_PPM_export(name,screen):
	height=len(screen)
	width=len(screen[0])
	
	f=open(name+".ppm",'w')
	f.write("P3\n")
	f.write("#test\n")
	f.write(str(width)+' '+str(height)+"\n") #width, height
	f.write("255\n") #max color size
	for row in screen:
		for pixel in row:
			f.write(" ".join(map(str,pixel.color))+' ')
		f.write("\n")

def dirVec(p1,p2):
	"direction vector from p1 to p2"
	return([p2[i]-p1[i] for i in range(3)])

def main():
	room_size=6000
	screen_lims=[room_size/4,3*room_size/4]
	screen_size=screen_lims[1]-screen_lims[0]
	camera=[room_size/2,room_size/2,-200]; #camera needs z<0
	bg_color=[0,0,0];
	screen=screen_init(screen_lims,bg_color);
	
	S1=sphere([0,0,255], room_size/20, [room_size/2-room_size/10,room_size/2-room_size/10,100])
	top=plane([80,150,150],[0,1,0,0])
	bottom=plane([150,90,150],[0,1,0,-room_size])
	back=plane([100,255,200],[0,0,1,-room_size])
	left=plane([50,20,100],[1,0,0,0])
	right=plane([50,90,150],[1,0,0,-room_size])
	objects=[S1,left,right,top,bottom,back]

	for row in screen:
		for pixel in row:
			t_min=100000; #large number
			ray=[camera, dirVec(camera,[pixel.x,pixel.y,0])]
			distances=[]
			#check intersection with each ob
			for ob in objects:
				t=ob.intersection(ray)
				if(t<t_min and t>0):
					pixel.color=ob.color
					t_min=t

	#make a white border
	for i in range(screen_size):
		screen[i][0].color=[255,255,255]
		screen[i][screen_size-1].color=[255,255,255]
		screen[0][i].color=[255,255,255]
		screen[screen_size-1][i].color=[255,255,255]
	#screen_print(screen)
	screen_PPM_export("first_img",screen)

main()



