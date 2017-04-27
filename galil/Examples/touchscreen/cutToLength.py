import kivy
#kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial
import gclib



class CutToLength(FloatLayout):
    dmc=gclib.py()#gclib object to communicate with Galil controllers
    sliderRange = (-500, 500000)
    cutLengthDefault = 500000
    controllerConnected = 0

    def start(self):
        Clock.schedule_interval(self._update_clock, 1 / 10.)#Setup the UI to run clock update 10 times a second
        self.populateControllers()

    #This function disconnects from the controller, 
    # returns the screen to the Choose Controller menu,
    # and refreshes the controller list
    def disconnectAndRefresh(self):
        self.ids.chooseController.collapse = False#Open starting screen
        self.controllerConnected = 0
        self.dmc.GClose()#close connection to controller
        self.ids.avTitle.title = 'Galil Motion Control'#Update the title 
        self.populateControllers()

    #This function is called when the E-STOP button is pressed.
    def eStop(self):
        if(self.controllerConnected > 0):
            self.dmcCommand('AB')#The abort command will disable the drive.
            self.controllerConnected = 0
            self.dmc.GClose()#close connection to controller
        self.ids.chooseController.collapse = False#Open starting screen
        self.ids.avTitle.title = 'E-STOP Triggered.'#Update the title

    #This function will populate the UI is available controllers on the network
    def populateControllers(self, *args):
        self.ids['row1'].clear_widgets()
        self.ids['row1'].add_widget(Label(height= 100,size_hint=(.33,.15),
                                          text='[b]Click to Select Controller[/b]',markup= True,font_size= 14))
        self.ids['row1'].add_widget(Label(height=100,size_hint=(.33,.15),text='[b]Address[/b]',
                                          markup=True,font_size= 14))
        self.ids['row1'].add_widget(Label(height=100,size_hint=(.33,.15),text='[b]Revision[/b]',
                                          markup=True,font_size= 14))
        self.controllers=self.dmc.GAddresses()#the gclib API call will return all controllers with IP addresses
        if(len(self.controllers)):
            for key, value in self.controllers.iteritems():
                print " ", key, " \t| ", value
                btn1 = Button(  height= 100, size_hint=(.33, .15),text=value.split('Rev')[0],background_color= [.6, 1.434, 2.151, 1],)
                btn1.bind(on_press=partial(self.selectController, key))#If controller is selected then pass info to the selectController function
                self.ids['row1'].add_widget(btn1)
                self.ids['row1'].add_widget(Label(height= 100,size_hint=(.33, .15),text=key))
                try:
                    self.ids['row1'].add_widget(Label(height= 100, size_hint=(.33, .15),text='Rev'+value.split('Rev')[1]))
                except:
                    self.ids['row1'].add_widget(Label(height= 100,size_hint=(.33, .15),text='Special'))
        else:
            self.ids['row1'].add_widget(Label(height= 100, size_hint=(.33, .15), text='No Contollers Found',font_size= 14))
            btn2 = Button(height= 100,size_hint=(.33, .15),text='Refresh',background_color= [.6, 1.434, 2.151, 1],)
            btn2.bind(on_press=partial(self.populateControllers))
            self.ids['row1'].add_widget(btn2)

   
    #This function is called when a controller is selected on the first page
    def selectController(self, value, *args):
        opened = self.appGOpen(value)
        if(opened):
            self.ids.homeSetup.collapse = False#Open the Homing and Setup screen
            self.ids.avTitle.title = 'Connected to: '+value #Update the title to show the connected controller
            self.controllerConnected = 1
            #Download slider program
            self.dmc.GProgramDownload("""
#slider
MO;         'Motor Off
MT-2.5;     'Setup axis as stepper motor
SHA;        'Servo the motor
AC512000;   'Set Acceleration Rate
DC512000;   'Set Deceleration Rate
SPA=180000; 'Set Motor Speed
pa=_RPA;    'Record current position
PTA=1;      'Setup Position Tracking Mode
#loop;      'Start of loop
PAA=pa;     'Update absolute position based on variable sent from HMI
WT100;      'Setup 100ms scan loop
JP#loop;    'Jump to loop
EN
""")
            self.dmcCommand("XQ#slider")#Run the downloaded program
    #This function is called when a controller is selected on the first page
    def appGOpen(self, value):
        try:
            self.dmc.GOpen(value +' -d')#Call GOpen with the IP Address selected
            return 1
        except Exception as e:
            self.ids.avTitle.title = 'Error: ' + str(e)
            return 0

    #This function will perform error trapping on any GCommand calls.
    #It is intended to capture any gclib errors and report the message to the title bar
    def dmcCommand(self, cmd):
        try:
            rc = self.dmc.GCommand(cmd)#Send command into the GCommand gclib API
        except Exception as e:
            print e
            tc1 = self.dmc.GCommand('TC1')
            print tc1
            self.ids.avTitle.title = 'Error: '+tc1#Update title with error message
    #This function will update the homing screen UI elements.
    #The function will ask for the Reported Position (RP) and Tell the state of the Switches (TS)
    #From this data the LED elements, text elements and sliders can be updated.
    def updateHomingScreen(self):
        data = self.dmc.GCommand('MG{Z10.0} _RPA, _TSA')#Get Position and Switch info
        self.ids['TPA'].text = data.split()[0]#Update the Position Text Element
        self.ids['slider_TPA'].value = int(data.split()[0])#Update the Slider element
        if(int(data.split()[1])&128):#extract bit index 7 in _TSA that tells if the axis is moving
            self.ids['_BGA'].text = 'Axis Moving'
        else:
            self.ids['_BGA'].text = 'Idle'
        if(int(data.split()[1])&4):#extract bit index 2 in _TSA for the Reverse Limit Switch status
            self.ids['_RLA'].active = False
        else:
            self.ids['_RLA'].active = True
        if(int(data.split()[1])&8):#extract bit index 3 in _TSA for the Forward Limit Switch status
            self.ids['_FLA'].active = False
        else:
            self.ids['_FLA'].active = True
        if(int(data.split()[1])&32):#extract bit index 5 in _TSA for the Motor Off status
            self.ids['_MOA'].active = True
        else:
            self.ids['_MOA'].active = False

    #This function is called at 10Hz.
    #It will call the functions to update the selected screen 
    def _update_clock(self, dt):
        if(self.controllerConnected == 1):
            self.updateHomingScreen()
        elif(self.controllerConnected == 2):
            self.updateCutScreen()

    #This function is executed when the slider is released. 
    #It sends its position to the controller as a variable. 
    #The program running on the controller will read that variable and perform the 
    #Position Absolute move in Position Tracking mode. 
    #This Position Tracking mode allows a new position to be chosen before the previous one finishes.
    def sliderMove(self, *touch):
        #Test if a controller is connected and check that the slider was touched
        if(self.controllerConnected == 1 and self.ids['slider_PAA'].collide_point(touch[1].ox, touch[1].oy)):
            self.dmcCommand("pa="+str(int(self.ids['slider_PAA'].value)))
            #print "slider moving to: " + str(int(self.ids['slider_PAA'].value))

    #This function will update the Cut-to-length screen UI elements.
    #The function will ask for the Reported Position (RP) and a variable called i
    def updateCutScreen(self):
        data = self.dmc.GCommand('MG{Z10.0} _RPA, i')#Get Position and variable info
        self.ids['cutPosition'].text = data.split()[0]#Update the Position Text Element
        self.ids['cutPositionSlider'].value = int(data.split()[0])#Update the Slider element
        self.ids['currentCut'].text = data.split()[1]#Update the counter element
        if(int(data.split()[1])>= int(self.ids['numCuts'].text)):
            self.controllerConnected = 2
            self.ids['currentStatus'].text = "Completed."

    #This function is called when the cut-to-length application is started
    #It will download a simple proof of concept cut-to-length application code the cycles the motor
    #back and forth and toggles IO at that start and end of the move.
    def startCutToLength(self):
        self.dmc.GProgramDownload("""
j=10;len=12000
#cut
WT1000
i=0
PTA=0
SHA
PA0
BGA
AMA
#loop
SB1
WT200
PAA=len
BGA
AMA
CB1
WT200
PAA=0
BGA
AMA
i=i+1
JP#loop, i<j
EN""")
        self.dmc.GSleep(100)
        self.dmcCommand('j='+self.ids['numCuts'].text)#Set the number of cuts variable on the controller
        self.dmcCommand('len='+self.ids['cutLen'].text)#Set the length of cut variable on the controller
        #rc = self.dmc.GCommand("XQ#cut")
        self.dmcCommand("XQ#cut")#Run the downloaded program
        self.controllerConnected = 2#update the variable to tell the UI which screen to update
        self.ids['currentStatus'].text = "Running..."#Update the status text

    #This function is to stop the cut-to-length application
    #TODO: Send the ST command to the controller to stop the application
    def stopCutToLength(self):
        self.ids['currentStatus'].text = "Stopping"
        self.dmcCommand("ST")#Stop the program

    #This is a simple function to increment or decrement the number of cuts
    #function is called from the accordian.kv UI file
    def addToCuts(self, count):
        value = int(self.ids['numCuts'].text) + count
        self.ids['numCuts'].text = str(value)

class ControllerApp(App):

    def build(self):
        c2l = CutToLength()
        c2l.start()
        return c2l

if __name__ == '__main__':
    ControllerApp().run()
    
