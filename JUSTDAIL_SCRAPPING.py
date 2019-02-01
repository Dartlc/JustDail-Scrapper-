from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import xlwt
import re
from xlwt import Workbook
wb=Workbook()
row=0
sheet1=wb.add_sheet('Scrapping Sheet',cell_overwrite_ok=True)
coln=['Company Name','Address','Website','email','phone no.']
for index ,obj in enumerate(coln):
    sheet1.write(row,index ,obj)
col=0
page=1
rowname=1
rowweb=1
rowemail=1
rownum=1
rowadd=1
while(page<=5):

    col=0    
    browser = webdriver.Firefox()
    browser.get("https://www.justdial.com/Gurugram/builders/page-"+str(page))
    name_element = browser.find_elements_by_xpath("//h2[@class='store-name']")
    for x in name_element:
        name=x.text
        #print(name)        
        sheet1.write(rowname,col,name)
        rowname=rowname+1


    r_links=[]

    elems = browser.find_elements_by_xpath("//a[@class='morehvr']")
    for elem in elems:
        links=elem.get_attribute("href")
        r_links.append(links)

    #print(r_links, '\n')
    emaillist=[]
    add=[]
    web=[]
    length=len(r_links)
    s=0
    while(s<=(length-1)):
        
        browser.get(r_links[s])
        address = browser.find_elements_by_xpath("//span[@class='lng_add']")
        #print(address)
        for x in address:
            add.append(x.text)

        website = browser.find_elements_by_xpath("//span[@class='mreinfp comp-text']")
        for xx in website:
            web.append(xx.text)

        emails = browser.find_elements_by_xpath("//button[@class='jbtn fltrt']")
        for email in emails:
            e=email.get_attribute("onclick")


        try:
            match=re.findall('[^=]+%40[^&]+',e)
            final_email=match[0].replace("%40","@")
            emaillist.append(final_email)
        except:
            pass
            emaillist.append("no email")
        
        s=s+1    


    
    new_add=[]
    for k in add:
        if k not in new_add:
            new_add.append(k)

    new_web1=[]
    new_web=[]
    for kk in web:
        if kk not in new_web:
            new_web.append(kk)


    for pls in new_web:
        new_web1.append('https://'+pls)


    new_add.remove('...(Map)')
    new_web1.remove('https://Send Enquiry By Email')
                    
    #print(new_add)
    #print(new_web1)
    new_web1=[m.split('..')[0] for m in new_web1]
    
    col=1
    c=1
    while(c<(len(new_add))):

        sheet1.write(rowadd,col,new_add[c])
        rowadd=rowadd+1
        c=c+2


    
    col=2
    cc=0
    while(cc<(len(new_web1))):

        sheet1.write(rowweb,col,new_web1[cc])
        rowweb=rowweb+1
        cc=cc+1
        
    col=3
    ccc=0
    while(ccc<(len(emaillist))):

        sheet1.write(rowemail,col,emaillist[ccc])
        rowemail=rowemail+1
        ccc=ccc+1


    phonenum=[]
    n=0 
    print(new_web1)
    while(n<(len(new_web1))):
        
        try:
            browser.get(new_web1[n])
            phone = browser.find_elements_by_xpath("//a[@class='phoneNo-link']")
            phonenum.append(phone[0].text)
        except:
            pass
            phonenum.append("no phone")
        
        n=n+1


    print(phonenum)
    col=4
    d=0
    while(d<(len(phonenum))):

        sheet1.write(rownum,col,phonenum[d])
        rownum=rownum+1
        d=d+1
            
   
    
    browser.quit()
    page=page+1
wb.save('Scrapping Sheet.xlsx')
