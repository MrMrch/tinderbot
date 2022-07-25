# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 19:09:03 2022
@author: marce
"""
#old stuff
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#end old stuff

#new stuff
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#end new stuff

import threading

import random
from time import sleep
from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException



# profile_info
ig_flags = ["instagram", "ig", "@", "Instagram", "insta", "ista", "ig:" ]
flags = ["onlyfans", "snapchat", "1.5", "15", "1,5", "gatito", "😼", "😻"] #this is dumb but I'm allergic to cats, and being 185 I gotta draw a line somewhere in terms of height.
name = ''

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.like_count = 0
        self.nope_count = 0
        self.matches = 0
        self.name = ''
        self.age = 0

#LAUNCHES TINDER AND OPENS FACEBOOK LOGIN --->login is currently manual
    def login(self):
        self.driver.get('https://tinder.com')

        sleep(3)
        # accedi = bot.driver.find_element_by_xpath('//*[@id="s1502865376"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a')

        accedi = bot.driver.find_element('css selector', 'a[data-testid="appLoginBtn"]')

        accedi.click()
        # data-testid="appLoginBtn
        sleep(1)
        
        fb = bot.driver.find_element('css selector', 'button[data-testid="login"]')

        fb.click()
       
#OPEN TINDER PROFILE TO INVESTIGATE
    def open_info2(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="s1502865376"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[3]/div[3]/button').click()
            print("mouseclick method")
        except:
            self.driver.find_element('css selector','body').send_keys(Keys.ARROW_UP)
            print("keyboard method")

    def open_info(self):
        self.driver.execute_script('document.querySelector(\'[data-testid="recCard_info"] + button\').click()')
        print("greyblue method")

#PROFILE ABOVE CERTAIN AGE HAVE AGE/2 % CHANCES OF CONTINUING
    def age_check(self, min_age, max_age):
        try:
            self.age = int(self.driver.find_element('css selector', 'span[data-testid="recCard__age"]').text)
            if self.age > int(max_age) or self.age < min_age: #default max age is 32
                chance = random.randint(0, 100)
                if chance != self.age:
                    print("age chance-->Nope :" + str(self.age))
                    global reason
                    reason += f"age: {self.age} /"
                    return False
                else:
                    print(f"she's {self.age} but got lucky")        
                    return True
            else:
                return True
        except Exception:
            print("can't detect age --> Nope")
            return False

# ADDING A RANDOM CHANCE THAT I WILL SWIPE LEFT
    def random_nope(self, x = 0):
        return random.choices([False, True], [x/100, 1 - x/100])            
            
    def check_bio(self):
        ig = True
        global bio
        try:
            bio = self.driver.find_element('css selector', 'div[data-testid="info-bio"]').text
            for word in ig_flags:
                if word in bio.lower():
                    print("ig flag: " + word)
                    ig = False
                else:
                    continue
            if len(bio) < 35 and ig == False:
                global reason
                reason += f"\n instagrammer - bio: {bio}\n"
                print("instagrammer")
                print(bio)
                return False
            else:
                for word in flags:
                    if word in bio.lower():
                        print("red flag: " + word)
                        return False
                    else:
                        continue
                print("no red flags")
                return True

        except Exception:
            bio =""
            like = random.choices([False, True], [.7, .3])
            if like:
                print(f"No bio but ok. Chance: {like}")
                return True
            else:
                print(f"no bio, suspiscious. Chance: {like}")
                # global reason
                reason += "no bio"

                return False

# CHECKING DISTANCE FOR PASSPORT USERS
    def check_km(self, km_lim):
        try:
            distance = self.driver.find_element('css selector', 'div[data-testid="info-distance"]').text
            km = int(distance.replace(" chilometri di distanza",""))
        
            if km > int(km_lim):
                print("usa passport")
                global reason
                reason += f"Distance: {km}km \n"
                return False
            else:
                print("distance ok")
                return True
        except:
            # global reason
            reason += "No distance \n"

            print("No distance.. suspiscious")
            return False

# DECIDE TO SWIPE BASED ON THE OTHER FUNCTIONS (distance, bio, age)
    def decision(self, km_lim, min_age, max_age):
        global swipe
        global reason
        global bio
        # if (self.check_km(km_lim) == False) or (self.check_bio() == False):
        if self.check_bio() and self.check_km(km_lim) and self.age_check(min_age, max_age):
            # global swipe
            swipe = "LIKE"
            self.like()
        else:
            # global swipe
            swipe = "NOPE"
            reason += bio
            self.nope()


################## ACTUAL SWIPING

# SWIPE RIGHT (LIKE))
    def like(self):
        like = self.driver.find_element('css selector', 'button[data-testid="gamepadLike"]')
        like.click()
        print("LIKE")
        self.like_count += 1

# SWIPE LEFT (NOPE)
    def nope(self):
        nope = self.driver.find_element('css selector', 'button[data-testid="gamepadDislike"]')
        nope.click()
        print("NOPE")
        self.nope_count += 1


################## BLOCKERS AND POPUPS

# CLOSE POPUP
    def close_popup(self):
        try:
            self.driver.find_element('css selector', 'button[data-testid="cancel"]').click()
            print("Closed popup (try)")
        except: 
            try:
                self.driver.find_element('css selector', 'button[data-testid="close"]').click()
                print("Closed superlike (try)===============================================================================================###############################")
            except: 
                self.driver.find_element('css selector', 'button[class="button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Fw($semibold) focus-button-style D(b) My(20px) Mx(a)"]').click()   
                print("Closed popup (except)")

    def close_match(self):
        print("ITS A MATCH! OPEN DEV TOOLS")
        input()
        self.driver.find_element('css selector', 'button[data-testid="emoji-message-😉"]').click()
        print("Closed match")
        
    def try_info_or_close2(self):
        try:
            self.open_info() #TRY TO OPEN THE  BIO 
        except Exception:
            try:
                self.close_popup() #TRY TO CLOSE POPUP (SUPERLIKE / INSTALL APP)
                sleep(random.uniform(1.815, 2.846))
                self.open_info()
            except Exception:
                try:
                    input()     #stops from closing match in order to
                    self.close_match() # TRY TO CLOSE MATCH
                    sleep(random.uniform(1.315, 1.846))
                    self.open_info()
                except Exception:
                    try: #TRY TO CLOSE BOOST AD
                        if self.driver.find_element('css selector', 'div[data-testid="header"]').text == 'IT’S PEAK TIME':
                            self.nope_count -= 1
                            self.nope()
                            print("Closed Boost ad")
                    except Exception: #IF NONE OF PREVIOUS SOLUTION WORKED, REFRESH PAGE AND WAIT 2 SEC
                        print("something wrong--> INVESTIGATE")
                        input()
                        self.driver.refresh()
                        sleep(random.uniform(5.315, 5.846))
                        print("no (i) button, no popup detected --> refresh")
                        # self.driver.find_element('css selector', 'button[data-testid="emoji-message-😉"]').click()

    def try_info_or_close(self):
        try:
            self.driver.find_element('css selector','body').send_keys(Keys.ARROW_UP)
            print("keyboard method")

        except Exception:
            try:
                self.close_popup() #TRY TO CLOSE POPUP (SUPERLIKE / INSTALL APP)
                sleep(random.uniform(1.315, 1.846))
                self.open_info()
            except Exception:
                try:
                    self.close_match() # TRY TO CLOSE MATCH
                    sleep(random.uniform(1.315, 1.846))
                    self.open_info()
                except Exception:
                    try: #TRY TO CLOSE BOOST AD
                        if self.driver.find_element('css selector', 'div[data-testid="header"]').text == 'IT’S PEAK TIME':
                            self.nope_count -= 1
                            self.nope()
                            print("Closed Boost ad")
                    except Exception: #IF NONE OF PREVIOUS SOLUTION WORKED, REFRESH PAGE AND WAIT 2 SEC
                        try:
                            self.driver.find_element('css selector','body').send_keys(Keys.ARROW_UP)
                            print("keyboard method")
                        except Exception:
                            print("something --> INVESTIGATE")
                            input()
                            self.driver.refresh()
                            sleep(random.uniform(5.315, 5.846))
                            print("no (i) button, no popup detected --> refresh")

    def close_first(self):
        try:
            self.matches += 1
            sleep(random.uniform(1.315, 1.846))
            self.open_info()
        except Exception:
            print("not a match")
            try:
                self.close_popup() #TRY TO CLOSE POPUP (SUPERLIKE / INSTALL APP)
                sleep(random.uniform(1.315, 1.846))
                self.open_info()
            except Exception:
                print("not a popup")
                try:
                    if self.driver.find_element('css selector', 'div[data-testid="header"]').text == 'IT’S PEAK TIME':
                        self.nope_count -= 1
                        self.nope()
                        print("Closed Boost ad")
                        sleep(random.uniform(1.315, 1.846))
                        self.open_info()

                except Exception:
                    self.open_info()

########## FULL PROFILE SWIPE AUTOMATIONS 

# A SINGLE SWIPE
    def swipe(self, km_lim, min_age, max_age):
        self.close_first()
        sleep(random.uniform(1.315, 3.846))
        self.decision(km_lim, min_age, max_age)

# Interrupt program on click button
    def stop(self):
        global stopped
        stopped = True
        print("YOU CLICKED THE BUTTON! YOU CLICKED THE BUTTOOOOOOOOOOOOOON!!!! WHYYYYYYY STOOOOOOOOOOOOOPPPPPP!")
        
# AUTOSWIPE A CERTAIN AMOUNT OF PROFILES
    def autoswipe(self, n, km_lim = 50, min_age = 20, max_age = 30):
        def run():
            global profile_info
            global swipe
            global reason
            global stopped 
            global bio
            stopped = False
            i = 0
            try:
                while i<n:
                    if stopped:

                        profile_info = " === AUTOSWIPE STOPPED ===\n"
                        answerFrame.insert("1.0", profile_info)
                        # profiles_label.pack()

                        break
                    i+=1    
                    print("-------------------------")
                    try:
                        self.close_first()
                    except Exception:
                        profile_info = " === NO MORE LIKES AVAILABLE - AUTOSWIPE STOPPED ===\n"
                        answerFrame.insert("1.0", profile_info)
                        self.driver.find_element('css selector', 'button[data-testid="modal"]').click()
                    try:
                        self.name = self.driver.find_element('css selector', 'h1[data-testid="recCard__name"]').text
                    except Exception:
                        print("name missing")
                        self.name = "NoName"
                    try:
                        self.age = int(self.driver.find_element('css selector', 'span[data-testid="recCard__age"]').text)
                    except Exception:
                        self.age = "No age"
                        print("missing age")
                        sleep(random.uniform(1.757, 2.534))
                    print(f"{i}° profile: {self.name} - {self.age}")

                    sleep(random.uniform(1.315, 3.846))
                    self.decision(km_lim, min_age, max_age)
                    profile_info = "________________________________________\n"
                    profile_info += f"{i}° profile: {self.name} - {self.age}: {swipe}\n{reason}\n"
                    reason = ""
                    nope_percent = round((self.nope_count/(self.like_count+self.nope_count))*100, 2)
                    like_percent = round((self.like_count/(self.like_count+self.nope_count))*100, 2)

                    print("% NOPES :" + str(nope_percent))
                    print_results()
                    global likesEntry
                    likesEntry.delete(0, END)
                    likesEntry.insert(0, like_percent)
                    
                    global nopeEntry
                    nopeEntry.delete(0, END)
                    nopeEntry.insert(0, nope_percent)

                    bio = ""

                    sleep(random.uniform(1.757, 2.734))
            except KeyboardInterrupt:
                print("stopped")
            
            print("LIKES :" + str(self.like_count))
            print("NOPES :" + str(self.nope_count))
            like_percent = round((self.like_count/(self.like_count+self.nope_count))*100, 2)
            nope_percent = round((self.nope_count/(self.like_count+self.nope_count))*100, 2)
            print(f"% LIKES: {like_percent}%")
            print(f"% NOPES: {nope_percent}%")
            print(f"% MATCHES: {self.matches}")
            
            profile_info = f"===========================================\n"
            profile_info +="AUTOSWIPE ENDED \n"
            profile_info +="\n"
            profile_info +=f"% LIKES: {like_percent}% \n"
            profile_info +=f"% NOPES: {nope_percent}% \n"
            profile_info +=f"% MATCHES: {self.matches}\n"
            profile_info += f"==========================================\n"
            
            print(profile_info)
            print_results()

        t = threading.Thread(target=run)
        t.start()


# AUTOSWIPE A CERTAIN AMOUNT OF PROFILES, TAKES A PAUS FOR A CERTAIN AMOUNT OF TIME AND REPEATS FOR X SESSIONS
    def swipe_pause(self, n, time_minutes, sess, km_lim = 50, min_age = 20, max_age = 30):
        ii = 1
        while ii <= sess:
            print(f"SESSION {ii} of {sess}")
            n = n + random.randint(-3, 3)
            self.autoswipe_helper(n, km_lim, min_age, max_age)
            now = datetime.now()
            pause = (time_minutes*60)+random.uniform(1.757, 59.734)
            resume_time = now + timedelta(seconds=pause)
            # APRI OFFICE MENU
            self.driver.find_element('css selector', 'button[class="Bdrs(50%) P(4px) Cur(p) Mx(8px) Mstart(4px):fc Mend(4px):lc Trsdu($fast) C(#fff):h Bgc(#000.32):h Bgc(#000.32):a C($c-light-gray) focus-outline-style Bgc(#000.12) C($c-bluegray) Sq(36px) CenterAlign"]').click()
            print(f'{now.strftime("%H:%M:%S")}: going to sleep...')
            print(f'Bot will be back online at {resume_time.strftime("%H:%M:%S")}')
            sleep(pause)
            # SWIPE AGAIN
            self.driver.find_element('css selector', 'button[class="focus-outline-style Mx(16px) Fz($xs) Td(u) Td(n):h C($c-ds-text-brand-normal):h Cur(p) P(0) Bdw(0)"]').click() #back to swiping
            print("=========================")
            print("Bot is back online")
            sleep(random.uniform(1.757, 2.734))
            ii+=1
        print(f"Automation ended. All {sess} sessions completed.")
        print(f"Total swipes = {self.like_count+self.nope_count} ")
        print(f"Likes = {self.like_count} ")
        nope_percent = round((self.nope_count/(self.like_count+self.nope_count))*100, 2)
        print(f"Nope rate = {nope_percent} ")

# HELPER FUNCTION WITHOUT DEFAULTS --> REWRITE USING OBJECT CLASS STATES?
    def autoswipe_helper(self, n, km_lim, min_age, max_age):
        i = 1
        try:
            while i<=n:
                print("-------------------------")
                self.close_first()
                try:
                    name = self.driver.find_element('css selector', 'h1[data-testid="recCard__name"]').text
                except Exception:
                    self.multi_close()
                    sleep(random.uniform(1.757, 2.534))
                    name = self.driver.find_element('css selector', 'h1[data-testid="recCard__name"]').text
                print(f"profilo {i}/{n}: {name}")
                sleep(random.uniform(1.315, 3.846))
                self.decision(km_lim, min_age, max_age)
                nope_percent = round((self.nope_count/(self.like_count+self.nope_count))*100, 2)
                print("% NOPES :" + str(nope_percent))
                sleep(random.uniform(1.757, 2.734))
                i+=1

        except KeyboardInterrupt:
            print("stopped")
        print("LIKES :" + str(self.like_count))
        print("NOPES :" + str(self.nope_count))
        like_percent = round((self.like_count/(self.like_count+self.nope_count))*100, 2)
        nope_percent = round((self.nope_count/(self.like_count+self.nope_count))*100, 2)
        print(f"% LIKES: {like_percent}%")
        print(f"% NOPES: {nope_percent}%")

# RESET COUNT OF LIKE/NOPE RATIO. AIM FOR 10% LIKES, 90% NOPES
    def reset_count(self):
        self.like_count = 0
        self.nope_count = 0


    def info(self):
        print('============================================================')
        print('to start autoswipe write "bot.autoswipe(n, km_lim, min_age, max_age)"')
        print('n = how many profiles to swipe)"')
        print('km_lim = profiles above this number will be swiped left )"')
        print('min_age = younger will be swiped left. Default min_age = 20 )"')
        print('max_age = older will be swiped left. Default max_age = 32)"')
        print('Default KM limit will be 50km, default max age will be 32')
        print('============================================================')
        print('To replicate human behaviour you can automate multiple sessions with pauses in between:')
        print('     bot.swipe_pause(self, n, time_minutes, sess, km_lim, max_age)')
        print('n = how many profiles to swipe. This will be randomized by +/- 3 profiles')
        print('time_minutes = write the minutes of pause. 60 plus minutes is recommended. Value will be randomized by +/- 60 seconds')
        print('sess = how many times should the swiping+pause be repeated')
        print('km_lim = profiles above this number will be swiped left )"')
        print('max_age = Everyone older will be swiped left according to chance)"')
        print('============================================================')
        print('To see this message again type bot.info()')
        print('============================================================')



bot = TinderBot()
bot.login()
bot.info()

################# IMPORTING TKINTER FOR USER INTERFACE

import tkinter as tk
from tkinter import *
from tkinter import END

root = tk.Tk()
root.geometry('800x800')

inputFrame = LabelFrame(root, text="Fill in your data here")
inputFrame.pack(padx=10, pady=10)

buttonFrame = LabelFrame(root, text = "click the button when ready", padx=20, pady=20)
buttonFrame.pack(padx=5, pady=5)

statsFrame = LabelFrame(root, text = "Live stats of LIKES and NOPES", padx=20, pady=20)
statsFrame.pack(padx=5, pady=5)

answerFrame = Text(root)
answerFrame.pack(padx=15, pady=15)


Label(inputFrame, text="Number of profiles:").grid(row=0, column=0)
n_profiles = Entry(inputFrame)
n_profiles.grid(row=0, column=1)
n_profiles.insert(0, 3)

Label(inputFrame, text="Max distance:").grid(row=1, column=0)
km_lim = Entry(inputFrame)
km_lim.grid(row=1, column=1)
km_lim.insert(0, 3)

Label(inputFrame, text="Insert Minimum Age:").grid(row=2, column=0)
min_age = Entry(inputFrame)
min_age.grid(row=2, column=1)
min_age.insert(0, 22)

Label(inputFrame, text="Insert Max Age:").grid(row=3, column=0)
max_age = Entry(inputFrame)
max_age.grid(row=3, column=1)
max_age .insert(0, 29)


#STATS BOX
Label(statsFrame,text="Likes %").grid(row=4, column=0)
likesEntry = Entry(statsFrame)
likesEntry.grid(row=4, column=1)
likesEntry.insert(0, "NONE")

Label(statsFrame, text="NOPE %").grid(row=5, column=0)
nopeEntry = Entry(statsFrame)
nopeEntry.grid(row=5, column=1)
nopeEntry.insert(0, "NONE")

profile_info = ""
reason = ""
swipe = ""
    
def myClick():
    n = n_profiles.get()
    km = km_lim.get()
    min_a = min_age.get()
    max_a = max_age.get()
    
    bot.autoswipe(int(n), int(km), int(min_a), int(max_a))


#THIS PRINTS PROFILES SWIPED AND OTHER INFO
def print_results():
    global profile_info

    answerFrame.insert("1.0", profile_info)

myButton = Button(buttonFrame, text="click me", padx=15, pady=15, command=myClick)
myButton.pack()

stopButton = Button(buttonFrame, text="STOP", padx=15, pady=15, command=bot.stop)
stopButton.pack()


root.mainloop()
