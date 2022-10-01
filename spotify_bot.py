from selenium import webdriver
import datetime 
from time import sleep
from secrets import username,passwd
from selenium.webdriver.common.action_chains import ActionChains

class Spotifybot:
    def __init__(self) :
        self.driver=webdriver.Chrome()
        self.index=2
        self.total=0

    def login(self):
        self.driver.get('https://open.spotify.com/')
        sleep(2)
        lg_btn = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/div[4]/button[2]')
        lg_btn.click()
        sleep(1)




    def fb_login(self):
        fblg_btn = self.driver.find_element_by_xpath('//*[@id="app"]/body/div[1]/div[2]/div/div[2]/div[1]/div/a')
        fblg_btn.click()
        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)
        password = self.driver.find_element_by_xpath('//*[@id="pass"]')
        password.send_keys(passwd)

        fblg_submit = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        fblg_submit.click()
        sleep(10)


    def normal_login(self):
        email_in = self.driver.find_element_by_xpath('//*[@id="login-username"]')
        password_in = self.driver.find_element_by_xpath('//*[@id="login-password"]')
        email_in.send_keys(username)
        password_in.send_keys(passwd)

        submit = self.driver.find_element_by_xpath('//*[@id="login-button"]')
        submit.click()
        sleep(10)

    def next_btn(self):
        # next_button = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]')
        nexsongdiv = sbot.driver.find_element_by_xpath('//div[@aria-rowindex="'+str(self.index) +'"]')

        action = ActionChains(self.driver)
        action.move_to_element(nexsongdiv)
        action.perform()
        play_btn = self.driver.find_element_by_xpath('//div[@aria-rowindex="'+str(self.index) +'"]/div/div[1]/div/button')
        title = play_btn.get_attribute('title')
        print(str(self.index-1) + ") "+title)
        # play_btn.click()
        self.driver.execute_script("arguments[0].click();",play_btn)
        
        self.index=self.index+1
        if self.index==self.total+1:
            exit()
        sleep(1)


        # next_button.click()

    def next_song(self):
        sleep(5)
        curr_time  = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[2]/div[1]')
        ctime=curr_time.get_attribute('innerHTML')
        end_time = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[2]/div[3]')
        etime=end_time.get_attribute('innerHTML')
        currTime=datetime.datetime.strptime(ctime,"%M:%S")
        finishTime=datetime.datetime.strptime(etime,"%M:%S")
        diff=(finishTime-currTime).total_seconds()
        
        if diff<35:
            sleep(diff)
            self.next_song()

        while diff>=8:
            ctime=curr_time.get_attribute('innerHTML')
            etime=end_time.get_attribute('innerHTML')
            currTime=datetime.datetime.strptime(ctime,"%M:%S")
            finishTime=datetime.datetime.strptime(etime,"%M:%S")
            diff=(finishTime-currTime).total_seconds()

        self.next_btn()

    def setTotalSongs(self,ind):
        if ind == 0:
            nsongselement = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[1]/div[5]/div/span')
        else:
            nsongselement = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[1]/div[5]/div/span[2]')
        nsongs=int(nsongselement.get_attribute('innerHTML').split()[0])
        self.total=nsongs

        

    def play_songs(self,ind):
        
        sleep(3)
        
        self.setTotalSongs(ind)

        nexsongdiv = self.driver.find_element_by_xpath('//div[@aria-rowindex="'+str(self.index) +'"]')

        action = ActionChains(self.driver)
        action.move_to_element(nexsongdiv)
        action.perform()
        play_btn = self.driver.find_element_by_xpath('//div[@aria-rowindex="'+str(self.index) +'"]/div/div[1]/div/button')
        title = play_btn.get_attribute('title')
        print(str(self.index-1) + ") "+title)
        # play_btn.click()
        self.driver.execute_script("arguments[0].click();",play_btn)
        self.index = self.index+1

        while True:
            self.next_song()
            sleep(40)

    def playlist(self):
        goto_playlist_section = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/nav/div[1]/ul/li[3]/div/a')
        goto_playlist_section.click()
        sleep(1)
        plists = self.driver.find_elements_by_xpath('//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[2]/div/div[2]/div/div/div/div[2]/a')
        dict = {}
        print("\n\nList of your playlists:")
        
        for idx,plist in enumerate(plists):
            print(str(idx+1)+ ") " + plist.get_attribute('text'))
            dict[idx]=plist

        
        pnumber = input('Enter the playlist number you want to play:')
        print(pnumber)
        # dict[int(pnumber)-1].click()
        self.driver.execute_script("arguments[0].click();",dict[int(pnumber)-1])
        print("\n\n")
        print("Starting to play the songs from the selected playlist\n\n")
        self.play_songs(int(pnumber)-1)

sbot=Spotifybot()
sbot.login()

print("1) Facebook Login")
print("2) Normal/google login")
ltype = input('Select the type of login you prefer(1 or 2): ')
if ltype=='1':
    sbot.fb_login()
else:
    sbot.normal_login()
# sbot.gm_login()
# sbot.fb_login()
sbot.playlist()

