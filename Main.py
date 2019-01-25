import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Process:
	def __init__(self,size):
		self.size=size
		self.start=0
		self.end=0
		self.allocated=False

class Hole:
	def __init__(self,start,end):
		self.start=start
		self.end=end
		self.empty=[start,end]
		self.space=end-start
class Memory():
	def __init__(self,size,holes,processes):
		self.holes=holes
		self.processes=processes
		self.size=size
	def allocate(self,index):
		self.holes.sort(key=lambda hole: hole.start)
		for i in self.holes:
			if(i.space >= self.processes[index].size):
				self.processes[index].start=i.empty[0]
				self.processes[index].end= i.empty[0]+self.processes[index].size
				self.processes[index].allocated=True
				i.empty[0]=self.processes[index].end
				i.space=i.empty[1]-i.empty[0]
				return True
		print ("process no."+str(self.processes.index(self.processes[index])+1),"cant get allocated.")
		del self.processes[index]
		return False
	def bestFitAllocate(self,index):
		ascSortedHoles=self.holes[:]
		for i in ascSortedHoles:
			for t in range(len(ascSortedHoles)-1):
				if(ascSortedHoles[t].space>ascSortedHoles[t+1].space):
					temp=ascSortedHoles[t]
					ascSortedHoles[t]=ascSortedHoles[t+1]
					ascSortedHoles[t+1]=temp

		for i in ascSortedHoles:
			if(i.space >= self.processes[index].size):
				self.processes[index].start=i.empty[0]
				self.processes[index].end= i.empty[0]+self.processes[index].size
				self.processes[index].allocated=True
				i.empty[0]=self.processes[index].end
				i.space=i.empty[1]-i.empty[0]
				return True
		print ("process no."+str(self.processes.index(self.processes[index])+1),"cant get allocated.")
		del self.processes[index]
		return False
	def WorstFitAllocate(self,index):
		largerst_hole=self.holes[0]
		for i in range(len(self.holes)):
			if(self.holes[i].space>largerst_hole.space):
				largerst_hole=self.holes[i]

		if(largerst_hole.space >= self.processes[index].size):
			self.processes[index].start=largerst_hole.empty[0]
			self.processes[index].end= largerst_hole.empty[0]+self.processes[index].size
			self.processes[index].allocated=True
			largerst_hole.empty[0]=self.processes[index].end
			largerst_hole.space=largerst_hole.empty[1]-largerst_hole.empty[0]
			return True
		print ("process no."+str(self.processes.index(self.processes[index])+1),"cant get allocated.")
		del self.processes[index]
		return False

	def deAllocation(self,index):
		if self.processes[index].allocated==True:
			self.processes[index].allocated=False
			procInHole=[]
			for h in self.holes:
				if self.processes[index].start >= h.start and  self.processes[index].end <= h.end:
					for p in self.processes:
						if p.start>=h.start  and p.end <= h.end and p.allocated==True:
							procInHole.append(p)

					if(len(procInHole)>0):
						procInHole[0].start=h.start
						procInHole[0].end=h.start+procInHole[0].size

					for i in range(len(procInHole)-1):
						procInHole[i+1].start=procInHole[i].end
						procInHole[i+1].end=procInHole[i+1].start+procInHole[i+1].size
					if(len(procInHole)>0):	
						h.empty=[procInHole[len(procInHole)-1].end  ,h.end]
					else:
						h.empty[0]=h.start	
					h.space=(h.empty[1]-h.empty[0])
			self.processes[index].start=0
			self.processes[index].end=0	
			for e in procInHole:
				print(e.start,e.end)
	
	def printall(self):
		print("Holes")
		i=1
		for e in self.holes:
			print(i,e.space)
			i+=1
		print("processes")
		i=1
		for e in self.processes:
			print(i,e.start,e.end)
			i+=1



class Example(QWidget):
    
	def __init__(self,memory):
		super(Example, self).__init__()
		self.setWindowTitle('Memory')
		self.memory=memory
		self.factor=1000/self.memory.size
		self.setGeometry(200,100,self.memory.size*self.factor+30,550)
		self.show()
		self.insert()
		

	def insert(self):
		fonts=QFont("Times", 14,QFont.Bold)
		label=QLabel("Add Process:",self)
		label.setFont(fonts)
		label.move(20,350)
		label.show()
		Mylineedit=QLineEdit(self)
		font2=QFont("Arial",14)
		Mylineedit.setFont(font2)
		Mylineedit.move(140,350)
		Mylineedit.setValidator(QIntValidator())
		Mylineedit.setMaxLength(4)
		Mylineedit.setPlaceholderText("Process Size")
		Mylineedit.setAlignment(Qt.AlignLeft)
		Mylineedit.show()
		Allocatebtn=QPushButton("Allocate",self)
		Allocatebtn.setFont(font2)
		Allocatebtn.move(340,340)
		Allocatebtn.resize(100,50)
		Allocatebtn.show()
		Allocatebtn.clicked.connect(lambda : self.Allocate(Mylineedit,radio1,radio2,radio3))
		label2=QLabel("Remove Process:",self)
		label2.setFont(fonts)
		label2.move(20,450)
		label2.show()
		Mylineedit2=QLineEdit(self)
		Mylineedit2.setFont(font2)
		Mylineedit2.move(175,450)
		Mylineedit2.setValidator(QIntValidator())
		Mylineedit2.setMaxLength(2)
		Mylineedit2.setPlaceholderText("Process no.")
		Mylineedit2.setAlignment(Qt.AlignLeft)
		Mylineedit2.show()
		deallocatebtn=QPushButton("Deallocate",self)
		deallocatebtn.setFont(font2)
		deallocatebtn.move(375,440)
		deallocatebtn.resize(100,50)
		deallocatebtn.show()
		deallocatebtn.clicked.connect(lambda: self.Deallocate(Mylineedit2))
		font3=QFont("Arial",9)
		groupbox=QGroupBox('Allocation Methodology:',self)
		groupbox.setFont(font2)
		radio1=QRadioButton('First Fit',self)
		radio1.setFont(font3)
		radio2=QRadioButton('Best Fit',self)
		radio2.setFont(font3)
		radio3=QRadioButton('Worst Fit',self)
		radio3.setFont(font3)
		radio1.show()
		vbox=QVBoxLayout(self)
		vbox.addWidget(radio1)
		vbox.addWidget(radio2)
		vbox.addWidget(radio3)
		vbox.addStretch(1)
		radio1.setChecked(1)
		groupbox.setLayout(vbox)
		groupbox.move(470,330)
		groupbox.resize(200,100)
		groupbox.show()

	def Allocate(self,Mylineedit,radio1,radio2,radio3):
		size=int(Mylineedit.text())
		if(size < 10):
			self.info("Process size is too small!")
			return
		self.memory.processes.append(Process(size))
		flag=True
		if(radio1.isChecked()):
			flag=self.memory.allocate(-1)
		elif(radio2.isChecked()):
			flag=self.memory.bestFitAllocate(-1)
		elif(radio3.isChecked()):
			flag=self.memory.WorstFitAllocate(-1)
		if(flag==False):
			self.info("Process can't get allocated!","Not enough memory space (try deallocating some processes.)")	
		self.update()	
		

	def Deallocate(self,Mylineedit2):
		index=int(Mylineedit2.text())-1
		if(index>=len(self.memory.processes) or index <0):
			self.info("No process found with such index!")
			return
		if(self.memory.processes[index].allocated==False):
			self.info("This process is already deallocated!")
			return
		self.memory.deAllocation(index)
		self.update()


	def info(self,text,information=''):
		msg=QMessageBox(self)
		msg.setIcon(QMessageBox.Information)	
		msg.setText(text)
		msg.setInformativeText(information)
		msg.setWindowTitle("Allocation error")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.show()
		retval = msg.exec_()

	


	def paintEvent(self, e):

		qp = QPainter()
		qp.begin(self)
		self.drawmemory(qp)
		qp.end() 

	def drawmemory(self,qp):
		font =QFont("Times", 8,QFont.Bold)
		qp.setFont(font)
		color = QColor('black')
		pen = QPen(color, 4, Qt.SolidLine)
		qp.setPen(pen)
		brush = QBrush(Qt.SolidPattern) 
		brush.setColor(QColor('Wheat')) 
		qp.setBrush(brush)
		qp.drawRect(10,10,self.memory.size*self.factor,280)
		qp.drawText(8,305,'0')
		qp.drawText(self.memory.size*self.factor+8,305,str(self.memory.size))
		brush.setColor(QColor("white"))
		qp.setBrush(brush)
		for e in self.memory.holes:
			qp.drawRect(e.start*self.factor+10,10,(e.end-e.start)*self.factor,280)
			qp.drawText(e.start*self.factor+8,305,str(e.start))
			qp.drawText(e.end*self.factor+8,305,str(e.end))
		brush.setColor(QColor("brown"))
		qp.setBrush(brush)
		colorchoices=['red','Orange','Sienna','Royalblue','yellow','Plum']
		x=0
		y=0
		for e in self.memory.processes:
			if(e.allocated==False):
				x+=1
				y+=1
				continue
			if(y>=len(colorchoices)):
				y=0	
			brush.setColor(QColor(colorchoices[y]))
			qp.setBrush(brush)
			qp.drawRect(e.start*self.factor+10,10,e.size*self.factor,280)
			qp.drawText(e.start*self.factor+13,160,'P'+str(x+1))
			x+=1
			y+=1

			
Hnum=0
holes_arr=[]
holes_arr2=[]
button_arr=[]
label_arr=[]
	
class Window(QMainWindow):
	def __init__(self):
		super(Window,self ).__init__()
		self.upoff=80;
		self.setGeometry(50,50,500,150)
		self.setWindowTitle("OS")
		self.home()

	def home(self):
		global Tholesnum
		global Tmemsize
		memLab = QLabel("Memory Size", self)
		memLab.move(15,20)
		memLab.resize(150,50)
		Tmemsize = QLineEdit(self)
		Tmemsize.setValidator(QIntValidator())
		Tmemsize.setMaxLength(4)
		Tmemsize.move(120,30)
		Tmemsize.resize(180,30)

		hnumLab = QLabel("Number Of Holes", self)
		hnumLab.move(15,self.upoff)
		Tholesnum = QLineEdit(self)
		Tholesnum.setValidator(QIntValidator())
		Tholesnum.setMaxLength(2)
		Tholesnum.move(120,self.upoff)
		Tholesnum.resize(180,30)

		btn = QPushButton("Show boxes",self)
		btn.move(340,self.upoff)
		btn.clicked.connect(self.setHoles)
		#QCoreApplication.instance().quit
		self.show()
		

	def setHoles(self):
		global Hnum
		Hnum=Tholesnum.text()
		global holes_arr
		global holes_arr2
		global button_arr
		global label_arr
		for e in holes_arr:
			e.close()
		del holes_arr[:]	
		for e in holes_arr2:
			e.close()
		del holes_arr2[:]	
		for e in label_arr:
			e.close()
		del label_arr[:]	
		for e in button_arr:
			e.close()
		del button_arr[:]	

		for i in range(int(Hnum)):
			templen = QLabel("Hole #"+str(i+1), self)
			templen.move(15,self.upoff+((1+i)*40))
			label_arr.append(templen)
			temp_tbox= QLineEdit(self)
			temp_tbox.setValidator(QIntValidator())
			temp_tbox.setMaxLength(4)
			temp_tbox.move(120,self.upoff+((1+i)*40))
			temp_tbox.resize(130,30)
			temp_tbox.setPlaceholderText("Start")
			holes_arr.append(temp_tbox)
			self.setGeometry(50,50,500,150+(int(Hnum)*45))
			temp_tbox.show()
			templen.show()

		for i in range(int(Hnum)):
			temp_tbox= QLineEdit(self)
			temp_tbox.setValidator(QIntValidator())
			temp_tbox.setMaxLength(4)
			temp_tbox.move(270,self.upoff+((1+i)*40))
			temp_tbox.resize(130,30)
			temp_tbox.setPlaceholderText("end")
			holes_arr2.append(temp_tbox)
			temp_tbox.show()
		
		capBTN= QPushButton("Show Memory",self)
		button_arr.append(capBTN)
		capBTN.show()
		capBTN.move(210,self.upoff+((1+int(Hnum))*40))
		capBTN.clicked.connect(self.captuerHoles)


	def captuerHoles(self):
		global holesList
		global holes_arr
		global holes_arr2
		holesList=[]
		global Hnum
		for i,j in zip(holes_arr,holes_arr2):
			tempHole=Hole( int(i.text())  ,  int(j.text()) )
			holesList.append(tempHole)
		global MemorySize
		MemorySize=int(Tmemsize.text())
		showmemory()

def showmemory():
	process=[]
	Mymem=Memory(MemorySize,holesList,process)
	ex=Example(Mymem)

def run():
	app=QApplication(sys.argv)
	GUI=Window()	
	sys.exit(app.exec_())
run()
