# -*- coding: utf-8 -*-
from Tkinter import *
import sched, time, threading
from datetime import datetime
import RPi.GPIO as GPIO
from Adafruit_PWM_Servo_Driver import PWM





breakfasttime=580.0
lunchtime=870.0
dinnertime=1230.0

pwm=PWM(0x40)
pwm.setPWMFreq(60)    

root = Tk()
GPIO.setmode(GPIO.BOARD)
breakfast = StringVar()
lunch = StringVar()
dinner = StringVar()
hadbreakfast=False
hadlunch=False
haddinner=False


def getFormatedBreakfast():
	h, m = divmod(breakfasttime, 60)
	return "%d:%02d" % (h, m)
def getFormatedLunch():
	h, m = divmod(lunchtime, 60)
	return "%d:%02d" % (h, m)

def getFormatedDinner():
	h, m = divmod(dinnertime, 60)
	return "%d:%02d" % (h, m)

def increaseBreakfast():
	global breakfasttime
	global breakfast
	breakfasttime+=1
	breakfast.set(getFormatedBreakfast())
def increaseLunch():
	global lunchtime
	global lunch
	lunchtime+=1
	lunch.set(getFormatedLunch())
def increaseDinner():
	global dinnertime
	global dinner
	dinnertime+=1
	dinner.set(getFormatedDinner())
def decreaseBreakfast():
	global breakfasttime
	global breakfast
	breakfasttime-=1
	breakfast.set(getFormatedBreakfast())
def decreaseLunch():
	global lunchtime
	global lunch
	lunchtime-=1
	lunch.set(getFormatedLunch())
def decreaseDinner():
	global dinnertime
	global dinner
	dinnertime-=1
	dinner.set(getFormatedDinner())
def checktime(sc):
	global hadbreakfast
	global hadlunch
	global haddinner
	time=datetime.now().strftime('%H:%M') 
	if(time[0]=='0'):
		time=time[1:]
	if time==getFormatedBreakfast() and int(hadbreakfast)==0:
		feed()
		hadbreakfast=True
	elif time==getFormatedLunch() and int(hadlunch)==0:
		feed()
		hadlunch=True
	elif time==getFormatedDinner() and int(haddinner)==0:
		feed()
		haddinner=True
	elif time=='24:00':
		hadbreakfast=False
		hadlunch=False
		haddinner=False
	sc.enter(1, 1, checktime, (sc,))



def feed():
	pwm.setPWM(1,1,servoMax)
def main():
	global breakfast
	global lunch
	global dinner
	
	Label(root, textvariable=breakfast,font=("Helvetica",30),fg='goldenrod2',bg='lightskyblue1').grid(row=2,column=0)
	breakfast.set(getFormatedBreakfast())
	
	Label(root, textvariable=lunch,font=("Helvetica", 30),fg='dark green',bg='lightskyblue1').grid(row=2,column=20)
	lunch.set(getFormatedLunch())
	
	Label(root, textvariable=dinner,font=("Helvetica", 30),fg='navy',bg='lightskyblue1').grid(row=2,column=40)
	dinner.set(getFormatedDinner())
	
	Label(root,text="Breakfast Time",font=("Helvetica", 24),fg='goldenrod2',bg='lightskyblue1').grid(row=0,column=0)
	Label(root,text="Lunch Time",font=("Helvetica", 24),fg='dark green',bg='lightskyblue1').grid(row=0,column=20)
	Label(root,text="Dinner Time",font=("Helvetica", 24),fg='navy',bg='lightskyblue1').grid(row=0,column=40)

	
	
	breakfastincrease = Button(root,text="↑",command=lambda:increaseBreakfast(),font=("Helvetica", 30),fg='goldenrod2',bg='dark slate blue')
	breakfastincrease.grid(row=1,column=0,padx=200,pady=100)
	
	breakfastdecrease = Button(root,text="↓",command=lambda:decreaseBreakfast(),font=("Helvetica", 30),fg='goldenrod2',bg='dark slate blue')
	breakfastdecrease.grid(row=3,column=0,padx=200,pady=100)
	
	lunchincrease = Button(root,text="↑",command=lambda:increaseLunch(),font=("Helvetica", 30),fg='dark green',bg='tomato2')
	lunchincrease.grid(row=1,column=20,padx=200,pady=100)
	
	lunchdecrease = Button(root,text="↓",command=lambda:decreaseLunch(),font=("Helvetica", 30),fg='dark green',bg='tomato2')
	lunchdecrease.grid(row=3,column=20,padx=200,pady=100)
	
	dinnerincrease = Button(root,text="↑",command=lambda:increaseDinner(),font=("Helvetica", 30),fg='navy',bg='sienna')
	dinnerincrease.grid(row=1,column=40,padx=200,pady=100)
	
	dinnerdecrease = Button(root,text="↓",command=lambda:decreaseDinner(),font=("Helvetica", 30),fg='navy',bg='sienna')
	dinnerdecrease.grid(row=3,column=40,padx=200,pady=100)
	root.title("Pet Feeder Application")
	root.configure(background='lightskyblue1')
	
	root.mainloop()
	root.destroy()

class myThread (threading.Thread):
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
	def run(self):
		self.s = sched.scheduler(time.time, time.sleep)
		self.s.enter(1, 1, checktime, (self.s,))
		self.s.run()
class feedThread(threading.Thread):
	def __init__(self,q ,threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.q = q
	def onThread(self, function, *args, **kwargs):
		self.q.put((function, args, kwargs))
	def feed(self):
		pwm.setPWM(channel,0,servoMax)
	def run(self):
		while True:
			try:
                function, args, kwargs = self.q.get(timeout=self.timeout)
                function(*args, **kwargs)
            except queue.Empty:
                self.idle()
	def idle(self):
		pass
thread1 = myThread(1)
thread1.start()

	
main()

