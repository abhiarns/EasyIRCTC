'''

                ******          Bugs            ******
                No Bugs. Things working  fine     

                ******          To Do           ******
                Nothing
'''
#===========================            Modules          ================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from datetime import timedelta  
from tkinter import ttk
from tkinter import *
import os
import json
#==========================   Global Variables        ============================
userID =  ""                                        
password =    ""                      
fromStationCode = ""
toStationCode =  ""
trainNo = ''
journeyDate =  ''               # '04-02-2018'
travelClass = "" 
travelQuota = "" 
mobileNo = 0       
paymentPreference = 0                   #        {  'Other':0 , 'PayTM':1, 'UPI':2   }
PaytmMobileNo = 0
vpa = 'test@test'
driver = None
noOfPassenger = 0
noOfPassengersSaved = 0
passengerDetails = []

clockText = ''                                          #declared in "Variables that have to be initialised after app" section
noOfPassengersSavedStr =''       #declared in "Variables that have to be initialised after app" section

hr=11
min=42
sec=1
moment = datetime.now().replace(hour=hr, minute=min, second=sec, microsecond=000000)
finalMoment = moment

firstCaptchaTime = 15
secondCaptchaTime = 15
makeThemBelieveTime = 45  # this is seconds from moment

BackgroundColor = "#E0F6FC"             # "#333"
LabelColor = "#2F6FB5"                        #                 "#B6B6E8"
LabelFont = "segoe ui"
LabelFontSize = 12
LabelFG = 'white'
hlc = 'blue'           #hight light color
hlt = 2   # high light thickness

seePswdVar = 0
# ====================================       Main Window settings    ===========================
                                  
app = Tk()
app.geometry('1010x600+100+0')
app.title("Indian Railways Fast Booking Helper")
app["bg"] = BackgroundColor

#  ****************************************    Mixture           ******************************
#Variables that have to be initialised after app

clockText = StringVar(app)
noOfPassengersSavedStr= StringVar(app)
timeDifference = StringVar(app)
#========================================   Frames  =====================================

headingFrame = Frame(app)
loginFrame = Frame(app,bg = BackgroundColor)
userIDFrame = Frame(loginFrame, highlightcolor=hlc,  highlightthickness=hlt)
passwordFrame = Frame(loginFrame, bg = BackgroundColor, highlightcolor=hlc,  highlightthickness=hlt)

planMyJourneyFrame = Frame(app)
fromStnFrame = Frame(planMyJourneyFrame, highlightcolor=hlc,  highlightthickness=hlt)
toStnFrame = Frame(planMyJourneyFrame, highlightcolor=hlc,  highlightthickness=hlt)
journeyDateFrame = Frame(planMyJourneyFrame, highlightcolor=hlc,  highlightthickness=hlt)

QuotaTrainClassFrame = Frame(app)
trainNoFrame = Frame(QuotaTrainClassFrame, highlightcolor=hlc,  highlightthickness=hlt)
travelClassFrame = Frame(QuotaTrainClassFrame, highlightcolor=hlc,  highlightthickness=hlt)
travelQuotaFrame = Frame(QuotaTrainClassFrame, highlightcolor=hlc,  highlightthickness=hlt)

noOfPsngrFrame = Frame(app, highlightcolor=hlc,  highlightthickness=hlt)
psgrDtlBtnFrame =Frame(app,bg=BackgroundColor)
psgrDtlFrame = Frame(psgrDtlBtnFrame,bg=BackgroundColor)
psgrBtnFrame = Frame(psgrDtlBtnFrame)
nameFrame = Frame(psgrDtlFrame, highlightcolor=hlc,  highlightthickness=hlt)
ageFrame = Frame(psgrDtlFrame, highlightcolor=hlc,  highlightthickness=hlt)
genderFrame = Frame(psgrDtlFrame, highlightcolor=hlc,  highlightthickness=hlt)
berthFrame = Frame(psgrDtlFrame, highlightcolor=hlc,  highlightthickness=hlt)
foodFrame = Frame(psgrDtlFrame, highlightcolor=hlc,  highlightthickness=hlt)
psgrInsertedFrame = Frame(psgrDtlFrame,bg=BackgroundColor)

psgrMobNoFrame = Frame(app,bg=BackgroundColor, highlightcolor=hlc,  highlightthickness=hlt)

paymentFrame = Frame(app)
paymentPreferFrame = Frame(paymentFrame, highlightcolor=hlc,  highlightthickness=hlt)
paytmFrame = Frame(paymentFrame, highlightcolor=hlc,  highlightthickness=hlt)
upiFrame = Frame(paymentFrame, highlightcolor=hlc,  highlightthickness=hlt)

tatkalFrame = Frame(app)
tatkalTimingFrame  = Frame(tatkalFrame, highlightcolor=hlc,  highlightthickness=hlt)
timeDiffFrame = Frame(tatkalFrame, highlightcolor=hlc,  highlightthickness=hlt)

mainButtonsFrame = Frame(app)
#====================================== Buttons      ==================================
s = ttk.Style()
s.configure('TButton', font=('Helvetica', 12))

insertButton = ttk.Button(psgrBtnFrame, text="Insert"   )
showInsertedButton = ttk.Button(psgrBtnFrame, text="Show Inserted")
clearBtn = ttk.Button(psgrBtnFrame, text="Clear Inserted")
insertButton.pack(side='left')
showInsertedButton.pack(side='left')
clearBtn.pack(side='left')

instructionButton = ttk.Button(mainButtonsFrame, text="Instructions"   )
saveAllButton = ttk.Button(mainButtonsFrame, text="Save all data"   )
launchBtn = ttk.Button(mainButtonsFrame, text="Launch")
instructionButton.pack(side='left')
saveAllButton.pack(side='left')
launchBtn.pack(side='left')

#================================== Dynamic labels / Entry ===============================
psgrInsertedLabel = Label(psgrInsertedFrame,
                 height = 1,
                bg =BackgroundColor,
                fg =LabelFG,
                font =(LabelFont , LabelFontSize))

TimeDiff = Label(timeDiffFrame,
                   height = 1,
                   bg =LabelColor,
                  fg =LabelFG,
                   font =(LabelFont , LabelFontSize)
                   )
noOfPassengerCb = ttk.Combobox(noOfPsngrFrame,font =(LabelFont , LabelFontSize), width = 5, state="readonly")
seePswdLbl = Label(loginFrame,height = 1,
                   bg =LabelColor,
                  fg =LabelFG,
                   font =(LabelFont , LabelFontSize))
#====================================== Core  Functions       ==================================
# Opening Login Page in Chrome
def starter():
        global driver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://www.irctc.co.in/eticketing/loginHome.jsf')

# Doing Login 
def Login():       
        #WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.ID,"usernameId")))
        unameBox=WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.ID,"usernameId")))
        unameBox.send_keys(userID)
        upwd = driver.find_element_by_class_name('loginPassword')
        upwd.send_keys(password)
        loginBtn = driver.find_element_by_id('loginbutton')

        time.sleep(firstCaptchaTime)        
        loginBtn.click()

        try:
                wrongCaptcha = WebDriverWait(driver,1,poll_frequency=0.1).until(
                        EC.element_to_be_clickable((By.ID,'loginerrorpanelok'))
                        ).click()
                Login()
        except:
                pass
       
        try:
                oldSession = WebDriverWait(driver,1,poll_frequency=0.1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,'input[value="Continue"'))
                        ).click()
        except:
                pass

# Automatic Entry on PlanMyJourney area
def planMyJourney():
        fromStn = WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH, '//input[@id="jpform:fromStation"]')))
        fromStn.send_keys(fromStationCode)       
        fromStn.send_keys(Keys.ENTER)        
        
        toStn = driver.find_element_by_xpath('//input[@id="jpform:toStation"]')
        toStn.send_keys(toStationCode)
        toStn.send_keys(Keys.ENTER)

        jDate = driver.find_element_by_xpath('//input[@id="jpform:journeyDateInputDate"]')
        jDate.send_keys(journeyDate)
       
        submitBtn = driver.find_element_by_xpath('//input[@id="jpform:jpsubmit"]')
        submitBtn.click()


#Selecting Travel Class , Train and Travel Quota
def QuotaTrainClass():
        try:
                base = r'//div[@id="qcbd"]//input[@value="' + travelQuota + '"]'
                #print(base)
                quotaRadio = driver.find_element_by_xpath(base)
                quotaRadio.click()

                base = r'//a[text()="'+ trainNo + '"]//parent::td//parent::tr//a[text()="' + travelClass +'"]'
                #print("Train and Class area",base)             
                TrainAndClass = driver.find_element_by_xpath(base)
                TrainAndClass.click()

                #base = r'//form[@id="avlAndFareForm"]//a[@id="' + trainNo+ '-' + travelClass + '-' + travelQuota + '-0"]'
                #checkAvailable = base + '//parent::td'
        except Exception as e:
                print("Exception Occured ", e)      
                
        base = r'//form[@id="avlAndFareForm"]//a[@id="' + trainNo+ '-' + travelClass + '-' + travelQuota + '-0"]'
        checkAvailable = base + '//parent::td'

        availability =WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH, checkAvailable))).text

        if(availability.find("AVAILABLE") >= 0):
                bookNowLink = driver.find_element_by_xpath(base)
                bookNowLink.click()
                try:
                        prevBook =WebDriverWait(driver, 1, poll_frequency=0.1).until(EC.element_to_be_clickable((By.ID, 'altavlfrm:continue'))).click()               
                except:
                        pass
        else:
                driver.execute_script('window.alert("Sorry, Confirm Seats not available for the date specified")')

#  Filling Passenger Details on Web
def FillUpPassengerDetails():
        
        m = 0;
        try:
                mealOpt = driver.find_element_by_xpath('//th[contains(text(),"Meal")]')
                if( mealOpt != None):
                        m=1
        except:
                pass

        base = r'//*[@id="addPassengerForm:psdetail:' + str(0) + r'"]/td[2]/input'
        xyz = WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH,base)))

        for i in range(len(passengerDetails)):
                try:
                        base = r'//*[@id="addPassengerForm:psdetail:' + str(i) + r'"]/td[2]/input'
                        addPName = driver.find_element_by_xpath(base )                                                                                                               
                        addPName.send_keys(passengerDetails[i][0])

                        base = r'//input[@id="addPassengerForm:psdetail:' + str(i) +  r':psgnAge"]' 
                        addPAge = driver.find_element_by_xpath(base)
                        addPAge.send_keys(passengerDetails[i][1])

                        base = r'//select[@id="addPassengerForm:psdetail:' +str(i)+ r':psgnGender"]'
                        pGender = driver.find_element_by_xpath(base)
                        Select(pGender).select_by_value(passengerDetails[i][2])

                except Exception as e:
                        print("Exception occurred  ",e)

                base = r'//select[@id="addPassengerForm:psdetail:' + str(i) + r':berthChoice"]'
                seatP = driver.find_element_by_xpath(base)
                try:
                        Select(seatP).select_by_value(passengerDetails[i][3])
                except Exception as e:
                        print("Exception Occured  ", e)

                if(m == 1):
                        base = r'addPassengerForm:psdetail:' + str(i) + r':foodChoice'
                        try:
                                meal = driver.find_element_by_id(base)
                                Select(meal).select_by_value(passengerDetails[i][4])
                        except Exception as e:
                                print("Exception Occured ", e)

        ISD_MobileNo_Box = driver.find_element_by_id("addPassengerForm:mobileNo")
        ISD_MobileNo_Box.clear()
        ISD_MobileNo_Box.send_keys(mobileNo)

        time.sleep(secondCaptchaTime)

        doItOnce        =       0

        if(datetime.now().time().hour == 11 and datetime.now().time().minute<11 and(travelQuota=="TQ" or travelQuota=="PT")) :
                #print("yes 1")
                while True:
                        if(datetime.now().time() > finalMoment.time() and doItOnce==0):
                                #print("yes 2")
                                doItOnce=1
                                nextBtn = driver.find_element_by_id('validate')
                                nextBtn.click()
                                break
        else:
                #print("yes 3")
                nextBtn = driver.find_element_by_id('validate')
                nextBtn.click()

#MakePayment function 
def processPayment():
        makePayment = driver.find_element_by_xpath('//input[@id="validate"]')
        makePayment.click()

#^^^^^^^^^         Various Payment Options        ^^^^^^^

# 1. PayTM
def PaytmWallet():
        walletCashCard = driver.find_element_by_css_selector("td[id='CASH_CARD']")
        walletCashCard.click()
        Paytm = driver.find_element_by_xpath("//input[@type='radio' and @value='71']")
        Paytm.click()

        processPayment()

        loginPaytm =WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.ID,"otp-btn")))
        loginPaytm.click()

        temp = WebDriverWait(driver,15,poll_frequency=0.1).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'login-iframe')))
        
        time.sleep(1)
        PaytmMobileNoField = WebDriverWait(driver,15,poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH,'//div[@class="group"]/input[1]')))
        PaytmMobileNoField.send_keys(PaytmMobileNo)
        RequestOTP = driver.find_element_by_class_name('myBtn')
        RequestOTP.click()

# 2. UPI
def BHIM_UPI():
        upiRadioBtn = WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.NAME,"UPI_VPA")))
        upiRadioBtn.click()

        processPayment()

        vpaField = driver.find_element_by_id('vpa')
        vpaField.send_keys(vpa)
        vpaSubmit = driver.find_element_by_id('payNow')
        vpaSubmit.click()
        
#firstPart of program which runs few minutes before Booking Time
def firstPart():
        starter()
        Login()
        planMyJourney()

#secondPart of program which starts at specified booking time
def secondPart():
        QuotaTrainClass()
        FillUpPassengerDetails()
                               
        journeySummaryPage = WebDriverWait(driver, 15, poll_frequency=0.1).until(EC.title_is("Book Ticket - Journey Summary"))
        #time.sleep(makeThemBelieveTime)

        if(paymentPreference == 1):         
                PaytmWallet()
        elif(paymentPreference == 2):
                BHIM_UPI()
        else:
            pass

        #time.sleep(900)                 #15 minute time to do things manually ( ONLY IF WEBDRIVER FAILS /  User choses other payment option )


#-----------------------------------------------------------------------------------------------------------------------------------------------
#====================================== GUI  Functions       ==================================
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def clock():
    global clockText,moment,TimeDiff
    clockText.set(datetime.now().strftime("%H:%M:%S"))  # I  for 12hr format H for 24hr 
    moment = datetime.now().replace(hour=hr, minute=min, second=sec, microsecond=000000)
    TimeDiff['text'] = moment - datetime.now()
    app.after(1, clock)

def userIDEntryFn(*args):
        global userID
        userID = userIDEntry.get()
        userID = userID.strip()

def passwordEntryFn(*args):
        global password
        password = passwordEntry.get()

def set_text():
        global seePswdVar,seePswdLbl
        if(seePswdVar%2==0):
                seePswdLbl.pack()
                if(len(password)>0):
                        seePswdLbl['text'] = password
                else:
                        seePswdLbl['text'] = "No password !!"
                seePswdVar += 1
        else:
                seePswdLbl.pack_forget()
                seePswdVar += 1

def fromStnEntryFn(*args):
        global fromStationCode
        fromStationCode = fromStnEntry.get()
        fromStationCode = fromStationCode.strip()
        fromStationCode = fromStationCode.upper()

def toStnEntryFn(*args):
        global toStationCode
        toStationCode = toStnEntry.get()
        toStationCode = toStationCode.strip()
        toStationCode = toStationCode.upper()

def jDateEntryFn(*args):
        global journeyDate
        journeyDate = jDateEntry.get()
        journeyDate = journeyDate.strip()

def trainNoEntryFn(*args):
        global trainNo
        trainNo = trainNoEntry.get()
        #print(trainNo)

def setTravelQuota(*args):
        global travelQuota, noOfPassengerCb
        travelQuota = travelQuotaCb.get()
        travelQuota =travelQuota[-3:-1]

        if(travelQuota == "TQ" or travelQuota == "PT"):
                noOfPassengerCb['values'] = ('1', '2', '3', '4')
                tatkalFrame.grid(row = 16)
        else:
                noOfPassengerCb['values'] = ('1', '2', '3', '4', '5', '6')
                tatkalFrame.grid_forget()

def setTravelClass(*args):
        global travelClass
        travelClass = travelClassCb.get()
        travelClass =travelClass[-3:-1]

def showInsertedFn():
    global noOfPassenger, passengerDetails
    showDetails = Tk()
    showDetails.geometry('600x230')
    showDetails.title("Showing details")
    x = Label(showDetails, font=(LabelFont,LabelFontSize))
    x['text'] = "Showing details in order : Name  ,  Age  ,  Gender  ,  Berth Preference  ,  Food Choice\n\
    IRCTC codes are shown for Gender  ,  Berth Preference  ,  Food Choice "
    x.place(x=0, y=175)
    for i in range(len(passengerDetails)):
        for j in range(5):
            x = Label(showDetails, font=(LabelFont,LabelFontSize))
            x['text'] = passengerDetails[i][j]
            x.grid(row=i + 1, column=j)

def noOfPassengerFn(*a):
    global passengerDetails, noOfPassenger,noOfPassengersSaved

    noOfPassenger = int(noOfPassengerCb.get())
    passengerDetails.clear()
    noOfPassengersSaved = 0
    psgrInsertedLabel['bg'] = LabelColor
    psgrInsertedLabel['text'] =str(noOfPassengersSaved) + "  INSERTED"

def insertButtonFn():
    global passengerDetails, noOfPassenger,noOfPassengersSaved, noOfPassengersSavedStr
    if(noOfPassenger > noOfPassengersSaved):
            
            tempList = []
            nm = nameEntry.get()
            nm = nm.strip()
            if(len(nm) !=0):
                    nm = nm.upper()
                    tempList.append(nm)
            else:
                    return

            try:
                tempList.append(int((ageEntry.get()).strip()))
            except Exception as e:
                    print("Enter a valid age (positive integers only)")
                    return

            if (genderCb.get() == "Male"):
                tempList.append('M')
            elif (genderCb.get() == "Female"):
                tempList.append('F')
            else:
                tempList.append('T')

            if (berthCb.get() == "Lower"):
                tempList.append('LB')
            elif (berthCb.get() == "Middle"):
                tempList.append('MB')
            elif (berthCb.get() == "Upper"):
                tempList.append('UB')
            elif (berthCb.get() == "Side Lower"):
                tempList.append('SL')
            elif (berthCb.get() == "Side Upper"):
                tempList.append('SU')
            elif (berthCb.get() == "Window Side"):
                tempList.append('WS')
            elif (berthCb.get() == "Cabin"):
                tempList.append('CB')
            elif(berthCb.get() == "Coupe"):
                tempList.append('CP')
            else:
                tempList.append("  ")

            if (foodCb.get() == "Veg"):
                tempList.append('V')
            elif (foodCb.get() == "Non Veg"):
                tempList.append('N')
            else:
                tempList.append('D')

            passengerDetails.append(tempList)
            noOfPassengersSaved +=1

            psgrInsertedLabel['text'] =str(noOfPassengersSaved) + "  INSERTED"

def clearBtnFn():
    global passengerDetails, noOfPassengersSaved
    noOfPassengersSaved = 0
    passengerDetails.clear()
    psgrInsertedLabel['text'] = str(noOfPassengersSaved) + "  INSERTED"

def psgrMobNoEntryFn(*args):
        global mobileNo
        mobileNo = psgrMobNoEntry.get()

def upiEntryFn(*args):
        global vpa
        vpa = upiEntry.get()

def paytmEntryFn(*args):
        global PaytmMobileNo
        PaytmMobileNo = int( (paytmEntry.get()).strip() )

def paymentCbFn(*args):
        global paymentPreference
        choice = paymentCb.get()
        if(choice == "BHIM / UPI"):
                paymentPreference = 2
                paytmFrame.pack_forget()
                upiFrame.pack()
        elif(choice == "Paytm"):
                paymentPreference = 1
                upiFrame.pack_forget()
                paytmFrame.pack()
        else:
                paymentPreference=0
                upiFrame.pack_forget()
                paytmFrame.pack_forget()

def askTatkalTimeEntryFn(*args):
        global hr,min,sec, moment
        temp = askTatkalTimeEntry.get()
        temp = temp.strip()
        if(len(temp) == 8):
                temp = temp.split(':')
                hr= int(temp[0])
                min= int(temp[1])
                sec =int(temp[2])                
                timeDiffFrame.pack(side='left')

def instructionFn():
        instr = Tk()
        instr.title("Instructions")
        instr.geometry("900x500+25+25")
        lbl = Label(instr, font=(LabelFont,LabelFontSize), justify='left')
        lbl['text'] = "INSTRUCTIONS TO USE THIS SOFTWARE\n\n\n\
1. Fill all details from top to bottom in CORRECT FORMAT. Example: Date is DD-MM-YYYY and Time is HH:MM:SS\n\n\
2. When booking has started, you will be required to enter 3 things only : 2 Captchas and 1 Otp / UPI PIN .\
\n      We recommend payment using Paytm/UPI as these methods are much faster than other methods.\
\n      DO NOT CLICK/ENTER ANYTHING ELSE. We have taken care of all the cases.\
\n\n3. You will be given 15 seconds to fill in Captcha. Captcha will be on the left side of screen . \
\n\n4. If you are booking Tatkal/Premium-Tatkal make sure you click Launch button atleast 90 seconds or more \
\n      before the booking time. The software will login and wait till BookingTime then it will do everything automatically.\
\n      Just enter captcha when it is brought infront of you.\
\n\n5. Make sure that the details you are entering are Valid for a particular train . Software will not check for validty\
\n      of entered information. It will be better if you are sure about all details. Ex (i): Food Option is valid only for trains like\
\n      Shatabdi/Rajdhani etc. For other trains please keep Food Option Empty. Ex (ii): Different types of trains have different\
\n      types of Berth. Common trains have LB/MB/UB/SL/SU , Shatabdi has WS(Window Side), some other trains have\
\n      Cabin/Coupe type berth. Just make sure all details enetered by you is valid for that train.\
"
        lbl.grid(row = 0)       

def saveAllFn():
        allData = {}
        allData['IRCTCUserID'] = userID
        allData['IRCTCPassword'] = password
        allData['FromStationCode'] = fromStationCode
        allData['ToStationCode'] = toStationCode
        allData['JourneyDate'] = journeyDate
        allData['TrainNo'] = trainNo
        allData['TravelQuota'] = travelQuota
        allData['TravelClass'] = travelClass
        allData['TotalnoofPassenger'] = noOfPassenger
        allData['PassengerDetails'] = passengerDetails
        allData['NoOfPassengersSaved'] = noOfPassengersSaved
        allData['MobileNumber'] = mobileNo
        allData['PaymentPreference'] = paymentPreference
        if(paymentPreference == 2):
                allData['VPA'] = vpa
        elif(paymentPreference == 1):
                allData['PaytmMobileNo'] = PaytmMobileNo
        else:
                pass

        s = json.dumps(allData)
        with open('data.txt','w' ) as f:
                f.write(s)


        

def launchFn():
        global finalMoment
        cls()
        clickOn = 0
        firstPart()
        if(travelQuota == "TQ" or travelQuota == "PT"):
                while True:
                        if(moment.hour == datetime.now().time().hour and moment.minute == datetime.now().time().minute 
                           and moment.second== datetime.now().time().second and clickOn==0):
                                finalMoment = datetime.now() + timedelta(seconds=makeThemBelieveTime)
                                clickOn =1
                                break
                secondPart()
        else:
                secondPart()


        #allDetails.mainloop()
#===================================    Labels and Input        ===================

# Horizontal Spacers
horizontalSpacer0 = Label(headingFrame, text='                              ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )

horizontalSpacer1 = Label(loginFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )
horizontalSpacer2 = Label(planMyJourneyFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )
horizontalSpacer3 = Label(planMyJourneyFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )
horizontalSpacer4 = Label(QuotaTrainClassFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )
horizontalSpacer5 = Label(QuotaTrainClassFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )
horizontalSpacer6 = Label(psgrInsertedFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )
horizontalSpacer7 = Label(paymentFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )
horizontalSpacer8 = Label(tatkalFrame, text='            ',
                                        bg = BackgroundColor,
                                        font =(BackgroundColor , LabelFontSize)
                                        )

# Vertical Spacers

verticalSpacer1 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer2 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer3 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer4 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer5 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer6 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer7 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer8 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer9 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
verticalSpacer10 = Label(app, text = ' ',
                                                        height =1,
                                                        bg =BackgroundColor,
                                                        font = (BackgroundColor , 3)
                                                        )
#Heading
heading = Label(app, text ='Quick Booker',
                                           height = 1,
                                           #width = 10,
                                           bg ='#35b1ea',
                                           fg = 'white',
                                           font =(LabelFont , 16)
                                           ).grid(row = 0, sticky= 'ew')

time_label = Label(app, textvariable = clockText,
                   height = 1,
                   bg = LabelColor,
                   fg = LabelFG,
                  font =(LabelFont , 16)
                   )
time_label.grid(row = 0, sticky = 'e' )

# Login portion
verticalSpacer1.grid(row =1)

userIDLbl = Label(userIDFrame, text ='IRCTC User ID',
                                           height = 1,
                                           #width = 10,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)
                                           ).pack(side="left")

userIDEntry = Entry(userIDFrame,
                                           width = 25,                                           
                                           font =( LabelFont ,  LabelFontSize)
                                           )
userIDEntry.bind("<KeyRelease>",  userIDEntryFn)
userIDEntry.pack(side='left')

userIDFrame.pack(side = 'left')

horizontalSpacer1.pack(side = 'left' , fill = "both" , expand =True)

passwordLbl = Label(passwordFrame, text ='IRCTC Password',
                                           height = 1,
                                           bg =LabelColor,
                                           fg = LabelFG,
                                           font =(LabelFont , LabelFontSize),
                                           ).pack(side="left" )

passwordEntry = Entry(passwordFrame,
                                           width = 25,                                           
                                           font =(LabelFont , LabelFontSize) , 
                                           show ='*'
                                           )
passwordEntry.bind("<KeyRelease>",  passwordEntryFn)
passwordEntry.pack(side='left')

seePswdBtn = Button(passwordFrame,text="⚡",command=lambda:set_text(),  font =(LabelFont , LabelFontSize-3))
seePswdBtn.pack(side='left')

passwordFrame.pack(side ='left')
loginFrame.grid(row = 2,  sticky='w' )

#===================    Plan MyJourney area              =====
verticalSpacer2.grid(row =3)
fromStnLbl = Label(fromStnFrame, text ='From Station Code',
                                           height = 1,
                                           #width = 10,
                                           bg =LabelColor,
                                           fg = LabelFG,
                                           font =(LabelFont , LabelFontSize)
                                           ).pack(side="left")

fromStnEntry = Entry(fromStnFrame,
                                           width = 10,                                           
                                           font =( LabelFont ,  LabelFontSize)
                                           )
fromStnEntry.bind("<KeyRelease>",  fromStnEntryFn)
fromStnEntry.pack(side='left')

fromStnFrame.pack(side = 'left')
horizontalSpacer2.pack(side = 'left' , fill = "both" )

toStnLbl =      Label(toStnFrame, text ='To Station Code',
                                           height = 1,
                                           #width = 10,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)
                                           ).pack(side="left")
toStnEntry = Entry(toStnFrame,
                                           width = 10,                                           
                                           font =( LabelFont ,  LabelFontSize)
                                           )
toStnEntry.bind("<KeyRelease>",  toStnEntryFn)
toStnEntry.pack(side='left')

toStnFrame.pack(side = 'left')
horizontalSpacer3.pack(side = 'left' , fill = "both" )

jDateLbl =      Label(journeyDateFrame, text ='Journey Date ( DD-MM-YYYY )',
                                           height = 1,
                                           #width = 10,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)
                                           ).pack(side="left")
jDateEntry = Entry(journeyDateFrame,
                                           width = 10,                                           
                                           font =( LabelFont ,  LabelFontSize)
                                           )
jDateEntry.bind("<KeyRelease>",  jDateEntryFn)
jDateEntry.pack(side='left')

journeyDateFrame.pack(side = 'left')

planMyJourneyFrame.grid(row = 4, sticky='w')

#       Quota Train Class
verticalSpacer3.grid(row =5)

trainNoLbl = Label(trainNoFrame, text ='Train No.',
                                           height = 1,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)
                                           ).pack(side="left")
trainNoEntry = Entry(trainNoFrame,
                                           width = 10,                                           
                                           font =( LabelFont ,  LabelFontSize)
                                           )
trainNoEntry.bind("<KeyRelease>", trainNoEntryFn )
trainNoEntry.pack(side ='left')

trainNoFrame.pack(side='left')

horizontalSpacer4.pack(side = 'left' , fill = "both" )

travelQuotaLbl = Label(travelQuotaFrame ,  text="Travel Quota",
                                           height = 1,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)
                       ).pack(side='left')
travelQuotaCb = ttk.Combobox(travelQuotaFrame,
                             width = 30,
                             font =(LabelFont , LabelFontSize), 
                             state="readonly"
                             )
travelQuotaCb['values'] = ("PREMIUM TATKAL  (PT)",
                                                            "LOWER BERTH/SR. CITIZEN  (SS)",
                                                            "GENERAL  (GN)",
                                                            "DIVYANGJAN  (HP)",
                                                            "LADIES  (LD)",
                                                            "TATKAL  (TQ)"
                                                        )
travelQuotaCb.bind("<<ComboboxSelected>>", setTravelQuota)
travelQuotaCb.pack(side='left')
travelQuotaFrame.pack(side='left')

horizontalSpacer5.pack(side = 'left' , fill = "both" )

travelClassLbl = Label(travelClassFrame ,  text="Travel Class",
                                        height = 1,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)
                       ).pack(side='left')
travelClassCb = ttk.Combobox(travelClassFrame,
                             width = 25,
                             font =(LabelFont , LabelFontSize),
                            state="readonly"
                             )
travelClassCb['values'] = (
                                                        "EXECUTIVE ANUBHUTI  (EA)",
                                                        "FIRST AC  (1A)", 
                                                        "EXECUTIVE CLASS  (EC)",
                                                        "SECOND AC  (2A)",
                                                        "FIRST CLASS  (FC)",
                                                        "THIRD AC  (3A)",
                                                        "THIRD AC ECONOMY  (3E)",
                                                        "CHAIR CAR  (CC)",
                                                        "SLEEPER CLASS  (SL)",
                                                        "SECOND SITTING  (2S)"
                                                        )
travelClassCb.bind("<<ComboboxSelected>>", setTravelClass)
travelClassCb.pack(side='left')

travelClassFrame.pack(side = 'left')

QuotaTrainClassFrame.grid(row = 6, sticky ='w')

#Passenger Details Area
verticalSpacer4.grid(row=7)
nameLabel = Label(nameFrame, text="Name",
                                           height = 1,                                           
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)).pack(side='top', fill ='both')
nameEntry = Entry(nameFrame,font =( LabelFont ,  LabelFontSize),width = 35)
nameEntry.bind("<KeyRelease>")
nameEntry.pack(side='top')

ageLabel = Label(ageFrame, 
                 text="Age",
                 height = 1,
                bg =LabelColor,
                fg =LabelFG,
                font =(LabelFont , LabelFontSize)
                ).pack(side='top', fill ='both')
ageEntry = Entry(ageFrame,font =( LabelFont ,  LabelFontSize),
                 width = 5,)
ageEntry.bind("<KeyRelease>")
ageEntry.pack(side='bottom')

genderLabel = Label(genderFrame, 
                    text="Gender",
                    height = 1,
                bg =LabelColor,
                fg =LabelFG,
                font =(LabelFont , LabelFontSize)
                ).pack(side='top', fill ='both')
genderCb = ttk.Combobox(genderFrame,font =(LabelFont , LabelFontSize), width = 15, state="readonly")
genderCb['values'] = ("Male", "Female", "Others")
genderCb.bind("<<ComboboxSelected>>")
genderCb.pack(side='bottom')

berthLabel = Label(berthFrame, 
                   text="Berth Preference",
                   height = 1,
                bg =LabelColor,
                fg =LabelFG,
                font =(LabelFont , LabelFontSize)).pack(side='top', fill ='both')
berthCb = ttk.Combobox(berthFrame,font =(LabelFont , LabelFontSize), width = 15, state="readonly")
berthCb['values'] = ("Lower", "Middle", "Upper", "Side Lower", "Side Upper", "Window Side", "Cabin", "Coupe","No preference")
berthCb.bind("<<ComboboxSelected>>")
berthCb.pack(side='bottom')

foodLabel = Label(foodFrame,
                 text="Food",
                 height = 1,
                bg =LabelColor,
                fg =LabelFG,
                font =(LabelFont , LabelFontSize)).pack(side='top', fill ='both')
foodCb = ttk.Combobox(foodFrame,font =(LabelFont , LabelFontSize), width = 10, state="readonly")
foodCb['values'] = ("Veg", "Non Veg", "No Food")
foodCb.bind("<<ComboboxSelected>>")
foodCb.pack(side='bottom')

horizontalSpacer6.pack(side ='left', fill = 'both')
psgrInsertedLabel.pack(side='top', fill ='both')

spacer = Label(psgrDtlFrame,
                                           bg =BackgroundColor,
                                           font =(LabelFont , 3)).pack(side='bottom', fill ='both')

insertButton['command'] = insertButtonFn
showInsertedButton['command'] = showInsertedFn
clearBtn['command'] = clearBtnFn

#-------------------------------------------    Put in noOfPassengerFn() to show dynamically
nameFrame.pack(side="left")
ageFrame.pack(side="left")
genderFrame.pack(side="left")
berthFrame.pack(side='left')
foodFrame.pack(side='left')
psgrInsertedFrame.pack(side='left')
psgrDtlFrame.pack(side = 'top')
psgrBtnFrame.pack(side = 'bottom')    
psgrDtlBtnFrame.grid(row=10, sticky='w')
#------------------------------------------------

noOfPassengerLbl = Label(noOfPsngrFrame, 
                         text="Total no. of Passengers",
                         height = 1,
                        bg =LabelColor,
                        fg =LabelFG,
                        font =(LabelFont , LabelFontSize)).pack(side='left', fill ='both')

noOfPassengerCb['values'] = ('1', '2', '3', '4', '5', '6')
noOfPassengerCb.bind("<<ComboboxSelected>>", noOfPassengerFn)
noOfPassengerCb.pack(side='left')

noOfPsngrFrame.grid(row=8 ,sticky='w')
verticalSpacer5.grid(row=9)

#Passenger mobile No.
verticalSpacer7.grid(row = 11)
psgrMobNoLabel = Label(psgrMobNoFrame, text ='Mobile Number',
                                           height = 1,
                                           #width = 10,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)
                                           ).pack(side="left")

psgrMobNoEntry = Entry(psgrMobNoFrame,
                                           width = 12,                                           
                                           font =( LabelFont ,  LabelFontSize)
                                           )
psgrMobNoEntry.bind("<KeyRelease>",  psgrMobNoEntryFn)
psgrMobNoEntry.pack(side='left')
psgrMobNoFrame.grid(row =12, sticky = 'w')

#Payment Preference
verticalSpacer8.grid(row = 13)
upiLabel =  Label(upiFrame, text = "Virtual Payment Address (VPA)",
                                               height = 1,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)).pack(side='left')
upiEntry = Entry(upiFrame,font =(LabelFont , LabelFontSize))
upiEntry.bind("<KeyRelease>", upiEntryFn)
upiEntry.pack(side = 'left')

paytmLabel =  Label(paytmFrame, text = "Paytm Mobile No", 
                                        height = 1,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)).pack(side='left')
paytmEntry = Entry(paytmFrame,font =(LabelFont , LabelFontSize))
paytmEntry.bind("<KeyRelease>", paytmEntryFn)
paytmEntry.pack(side = 'left')

paymentLabel = Label(paymentPreferFrame, text = "Payment Preference",
                                                 height = 1,
                                           #width = 10,
                                           bg =LabelColor,
                                           fg =LabelFG,
                                           font =(LabelFont , LabelFontSize)).pack(side='left')
paymentCb = ttk.Combobox(paymentPreferFrame,font =(LabelFont , LabelFontSize), width = 10, state="readonly")
paymentCb['values'] = ("BHIM / UPI", "Paytm", "Other" )
paymentCb.bind("<<ComboboxSelected>>", paymentCbFn)
paymentCb.pack(side='left')

paymentPreferFrame.pack(side = 'left')
horizontalSpacer7.pack(side ='left', fill = 'both')
paymentFrame.grid(row = 14 )

#TatkaL timing
verticalSpacer9.grid(row =15)
askTatkalTimeLabel = Label(tatkalTimingFrame,
                           text ="Tatkal Booking starts at ( HH:MM:SS )",
                           height = 1,                                           
                        bg =LabelColor,
                        fg =LabelFG,
                        font =(LabelFont , LabelFontSize)).pack(side='left')
askTatkalTimeEntry = Entry(tatkalTimingFrame,font =(LabelFont , LabelFontSize))
askTatkalTimeEntry.bind("<KeyRelease>", askTatkalTimeEntryFn)
askTatkalTimeEntry.pack(side = 'left')
tatkalTimingFrame.pack(side = 'left')
horizontalSpacer8.pack(side = 'left', fill ='both')

TimeDiff.pack(side='left')

#main buttons
verticalSpacer10.grid(row = 17)
instructionButton['command']= instructionFn
saveAllButton['command'] = saveAllFn
launchBtn['command'] = launchFn
mainButtonsFrame.grid(row = 18)

#=========================      Running App     =====================
#fetch if any previous data exists
try:
        f = open('data.txt','r')
        s = f.read()
        allData = json.loads(s)
        #print(allData)
        
        userIDEntry.insert(0, allData['IRCTCUserID'])
        userID = allData['IRCTCUserID']

        passwordEntry.insert(0,allData['IRCTCPassword'])
        password = allData['IRCTCPassword']

        fromStnEntry.insert(0,allData['FromStationCode'])
        fromStationCode = allData['FromStationCode']

        toStnEntry.insert(0,allData['ToStationCode'])
        toStationCode = allData['ToStationCode']

        jDateEntry.insert(0,allData['JourneyDate'])
        journeyDate = allData['JourneyDate']

        trainNoEntry.insert(0,allData['TrainNo'])
        trainNo = allData['TrainNo']

        temp = allData['TravelQuota']

        if(temp == "PT"):
                travelQuotaCb.set("PREMIUM TATKAL  (PT)")
                travelQuota = 'PT'
        elif(temp == "SS"):
                travelQuotaCb.set("LOWER BERTH/SR. CITIZEN  (SS)")
                travelQuota = 'SS'
        elif(temp == "GN"):
                travelQuotaCb.set("GENERAL  (GN)")
                travelQuota = 'GN'
        elif(temp == "HP"):
                travelQuotaCb.set("DIVYANGJAN  (HP)")
                travelQuota = 'HP'
        elif(temp == "LD"):
                travelQuotaCb.set("LADIES  (LD)")
                travelQuota = 'LD'
        elif(temp == "TQ"):
                travelQuotaCb.set("TATKAL  (TQ)")
                travelQuota = 'TQ'
        else:
                pass

        temp = allData['TravelClass']

        if(temp == "EA"):
                travelClassCb.set("EXECUTIVE ANUBHUTI  (EA)")
                travelClass = "EA"
        elif(temp == "1A"):
                travelClassCb.set("FIRST AC  (1A)")
                travelClass = "1A"
        elif(temp == "EC"):
                travelClassCb.set("EXECUTIVE CLASS  (EC)")
                travelClass = "EC"
        elif(temp == "2A"):
                travelClassCb.set("SECOND AC  (2A)")
                travelClass = "2A"
        elif(temp == "FC"):
                travelClassCb.set("FIRST CLASS  (FC)")
                travelClass = "FC"
        elif(temp == "3A"):
                travelClassCb.set("THIRD AC  (3A)")
                travelClass = "3A"
        elif(temp == "3E"):
                travelClassCb.set("THIRD AC ECONOMY  (3E)")
                travelClass = "3E"
        elif(temp == "CC"):
                travelClassCb.set("CHAIR CAR  (CC)")
                travelClass = "CC"
        elif(temp == "SL"):
                travelClassCb.set("SLEEPER CLASS  (SL)")
                travelClass = "SL"
        elif(temp == "2S"):
                travelClassCb.set("SECOND SITTING  (2S)")
                travelClass = "2S"
        else:
                pass

        noOfPassengerCb.set(allData['TotalnoofPassenger'])
        noOfPassenger = allData['TotalnoofPassenger']

        passengerDetails = allData['PassengerDetails'] 

        noOfPassengersSaved = allData['NoOfPassengersSaved']
        psgrInsertedLabel.pack(side='top', fill ='both')
        psgrInsertedLabel['bg'] = LabelColor
        psgrInsertedLabel['text'] =str(noOfPassengersSaved) + "  INSERTED"

        psgrMobNoEntry.insert(0,  allData['MobileNumber'] )
        mobileNo  = allData['MobileNumber']

        temp = allData['PaymentPreference']

        if( temp == 2):
                paymentCb.set("BHIM / UPI")
                upiEntry.insert(0, allData['VPA'])
                vpa = allData['VPA']
                paymentPreference = allData['PaymentPreference']
                paytmFrame.pack_forget()
                upiFrame.pack()
        elif( temp == 1):
                paymentCb.set("Paytm")
                paytmEntry.insert(0, allData['PaytmMobileNo'])
                PaytmMobileNo = allData['PaytmMobileNo']
                paymentPreference = allData['PaymentPreference']
                upiFrame.pack_forget()
                paytmFrame.pack()
        else:
                paymentPreference = 0
                upiFrame.pack_forget()
                paytmFrame.pack_forget()
                pass

except:
        pass

app.after(0, clock)
app.mainloop()


'''
         IRCTC  INFO:  

        Travel Classes : 
            1. EXECUTIVE ANUBHUTI               (EA)
            2. FIRST AC                                                 (1A)
            3. EXECUTIVE CLASS                           (EC)
            4. SECOND AC                                          (2A)
            5. FIRST CLASS                                         (FC)
            6. THIRD AC                                              (3A)
            7. THIRD AC ECONOMY                   (3E)
            8. CHAIR CAR                                           (CC)
            9. SLEEPER CLASS                                  (SL)
           10. SECOND SITTING                           (2S)

        Quotas : 
            1. PREMIUM TATKAL            (PT)
            2. LOWER BERTH/SR. CITIZEN   (SS)
            3. GENERAL                   (GN)
            4. DIVYANG       (HP)
            5. LADIES                    (LD)
            6. TATKAL                    (TQ)
            

        Passenger Details :
        Format    :     [ "NAME"  ,  AGE  ,  'GENDER' ,  "BERTH", "MEAL" ]
        where 
                        Gender  =  Male                                    M
                                                Female                                F
                                                Transgender                    T


                        BERTH = Lower Berth              LB
                                              Middle Berth            MB 
                                              Upper Berth             UP 
                                              Side Lower                SU 
                                              Side Lower                SL 
                                              ------- In Shatabdi like trains -------
                                              Window Side           WS   

                        MEAL =     Non Veg                     N
                                                Veg                               V
                                                No food                      D


A 2-D list holds data of atmost 6 passengers. 


#Waiting till correct second captcha is enetered
try:
        wrongCaptcha = driver.find_element_by_xpath('//div[@class="error_div"]')
        if (wrongCaptcha == None):
                pass
        else:
                driver.execute_script('window.scrollBy(0,-700')
                time.sleep(secondCaptchaTime)
                makePayment.click()
except:
        pass



        Made with Love
'''

