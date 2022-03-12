 # import the needed libraries for the program

from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import smtplib
import re
from PIL import ImageTk,Image 



def Check():
    """ A function that Verify all the personal details like phone no
        email id etc. , are correct or not"""
    try:
        ent_tbl['state']='readonly'
        name=Entry.get(ent_name)
        #creating variables to store details data.
        email=Entry.get(ent_mail)
        purpose=ent_pur.get()
        pyment=Entry.get(ent_Payment)

        if checkno('91'+Entry.get(ent_phno))==None:  # for phone number verification
            messagebox.showinfo('INFO','Invalid phone number !\nPlease fill a correct phone number .')
        elif ('@gmail.com' not in email) and ('@yahoo.com' not in email):# for email varification
            messagebox.showinfo('INFO','Invalid Email ID\nPlease fill a correct email id .')
        elif name =='':     # for name varification 
             messagebox.showinfo('INFO','Invalid name !\nPlease fill a name .')
        elif pyment == 'Select:-':  # for payment varification
             messagebox.showinfo('INFO','Please select a pyment mode  .')
        else:   # purpose and table no processing
            if purpose != 'Select:-':
                if purpose == 'For Packing':
                    ent_tbl.current(0)
                    ent_tbl['state']=DISABLED
                    OrderSummary()
                else:
                    if ent_tbl.get()=='Select:-':
                         messagebox.showinfo('INFO','Please Select a table number !')
                    else:
                        OrderSummary()
            else:
                messagebox.showinfo('INFO','Please select purpose')
                    
        
        
    except:
        messagebox.showinfo('INFO','Something Went Wrong !\nPlease Try Again !\n\n\nSuggestion :-\nWhich item you don\'t wnat fill its quantity zero\'0\'')
                    



def OrderSummary():
    """ A Functon that collect the data from each entries on pressing the
          done button and then process it"""
    global _format
    global sum1 # a variable that store the total bill
    name = Entry.get(ent_name)
    mail = Entry.get(ent_mail)
    ph = Entry.get(ent_phno)
    table = ent_tbl.get()
    purpose = ent_pur.get()
    # Creat a list named quantity which holds the quantities of food..
    quantity = list(map(int, [Entry.get(ent_Mtea), Entry.get(ent_Lassi), Entry.get(ent_Colcof), Entry.get(ent_Choshake), Entry.get(ent_Icecrm), Entry.get(ent_Hotcho), Entry.get(
        ent_Hotcof), Entry.get(ent_Vburg), Entry.get(ent_Pburg), Entry.get(ent_Vroll), Entry.get(ent_Proll), Entry.get(ent_Tmto), Entry.get(ent_Mansoup), Entry.get(ent_Noodle), Entry.get(ent_Thali)]))

    # creat a list named Name_item which holds the names of food or menu card
    Name_item = ["Masala Tea (Rs.15/-)   :", "Lassi (Rs.40/-) :             ", "Cold Coffee (Rs.40/-)  :", "Choco Shake (Rs.60/-):", "Ice Cream (Rs.30/-)     :", "Hot Choco_(Rs.50/-) :   ", "Hot Coffee (Rs.25)  :     ",
                 "Veg Burger (Rs.40/-)   :", "Paneer Burger(Rs.50/-):", "Veg Roll (Rs.30/-)        :", "Paneer Roll (Rs.40/-) :  ", "Tomato Soup(Rs.60/-):", "Manchow Soup(Rs.80):", "Hakka Noodles(Rs.120):", "Thali (Rs.200/-) :           "]

    # creat a dictionary that contains  all item's name as key and and their quantity as values 
    Quanti_dict = {Name_item[i]: quantity[i] for i in range(15)}
     # declearing a list of item's orignal prize for future purpose
    prize = [15, 40, 40, 60, 30, 50, 25, 40, 50, 30, 40, 60, 80, 120, 200]
    # creat a dictionary that contains  all item's name as key and and their quantity as values for multipling the quantity
    Item_dict = {Name_item[i]: prize[i] for i in range(15)}

    # call a function named OrderDetails to get order details in a billing format
    _format = OrderDetails(name, mail, ph, table,purpose, Quanti_dict, Item_dict)
    
    ent_Total['state'] = NORMAL
    ent_Total.delete(0, 'end')
    ent_Total.insert(0,sum1)
    ent_Total['state'] = DISABLED
    confirm=messagebox.askquestion("CONFIRM ORDER WINDOW ? :",'%s\n\nPress yes to confirm your order...\n\nPress no to edit your order...'%(_format))
    if confirm == 'yes':
        PlaceOrder()
    else:
        messagebox.showinfo('INFO','Till now order is not placed \nPress Place Order button to place order .\n\nThank You !')


def OrderDetails(name, mail, ph, table, purpose, Quanti_dict, Item_dict):
    global sum1
    sum1=0
    a = 'Item Name                                         Quantity                                   Prize\n\n\n',

    for value in Quanti_dict:
        if Quanti_dict[value] != 0:
            a += value, '                            ', Quanti_dict[
                value], '                                     ', Item_dict[value]*Quanti_dict[value], '\n'
            
            sum1+=Item_dict[value]*Quanti_dict[value]

    c2 = '\n\nPersonla Details :\n\nName        : ', name, '\nPhone no : ', ph, '\nEmail         : ', mail, '\nTable NO  : ', table, '\nPurpose    : ', purpose, '\nDate & Time : ', datetime.now(),'\nPayment Mode  : ',ent_Payment.get(),'\n\nOrder Details :\n\n'
    syntax1 = 'Welcome to Fast Food Restaurant'.center(60, '-')
    syntax2 = ''
    syntax3 = ''
    syntax4 = ''
    c3 = '\n\n\n                                                                                          Total   =  ',sum1,' \n\n\nAre you Sure to place the order ?'
    for i in a:
        syntax3 += str(i)
    for i in c2:
        syntax2 += str(i)
    for i in c3:
        syntax4 += str(i)

    return (syntax1+syntax2+syntax3+syntax4)


def PlaceOrder():
    """On pressing the order button send the order details to managers Email id and clear
       the item entries"""
    try:
        
        global _format  # A variable that contain a message to be sent

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login("orderbot999@gmail.com", "xdyfzszymkldjptx")

        # sending the mail
        check=s.sendmail("orderbot999@gmail.com", "fastfootcenter123@gmail.com", _format)
        # terminating the session
        s.quit()

         # show a info after successfully placed a order
        messagebox.showinfo(
                 'INFORMATION', 'Your Order has been placed .\nPlease give us some time to prepare it \n\nThank You !\n\n\nHave a Nice Day !')
        ent_Total['state'] = NORMAL

        # creat a list of name of entries by which it can easly to modify these entries using just for loop
        ent_name = [ent_Mtea, ent_Lassi, ent_Colcof, ent_Choshake, ent_Icecrm, ent_Hotcho, ent_Hotcof,
                    ent_Vburg, ent_Pburg, ent_Vroll, ent_Proll, ent_Tmto, ent_Mansoup, ent_Noodle, ent_Thali, ent_Total]
        for i in ent_name:
            i.delete(0, 'end')
            i.insert(0, 0)
        ent_Total['state'] = DISABLED
        clear()
        ent_tbl['state']='readonly'
        
    except ZeroDivisionError:
        messagebox.showinfo('Error Message',"Sir/Ma'am.....\nSorry for not placing your order due to no internet problem.\nPlease try again ! or contect to manager. ")
        

    


def clear():
    """ Clear the other entries of name , phone no , mail, table no , purpose
       on successfullly placing the order"""
    ent_name.delete(0, 'end')
    ent_mail.delete(0, 'end')
    ent_phno.delete(0, 'end')
    ent_pur.current(0)
    ent_tbl.current(0)
    ent_Payment.current(0)

def checkno(ph):
    pattern=re.compile("(0|91)?[6-9][0-9]{9}$")
    return pattern.match(ph)

key = Tk()
key.geometry('1350x750+0+0')  # open window size..
key.title("Project BY Sumit Kumar.")

#selecting an image to set in window
path='C:/Users/wave/Desktop/Internet Exploral/sumit.jpg'
imgg=Image.open(path)
imgg=imgg.resize((1400,650))
imag=ImageTk.PhotoImage(imgg)


# Creat a frame for windows...
FRM = Frame(key, width=1350, height=520, bd=12, relief="flat")
FRM.pack(side=BOTTOM)
key.configure(bg='paleturquoise1')  # window Color..

#placing selected image as a lable i window
lbl=Label(image=imag)
lbl.pack()

# To creat a Heading label..
head = Label(key, text='|_order_counter_|',font='Algerian 20',fg='black',relief='flat',bg='azure3')
head.place(anchor='center', relx=.52, rely=.04)  # placing the label..
lbl_name = Label(key, text='Name :->', font='Algerian 15',
                 bg='azure3', fg='black')
lbl_name.place(anchor='center', relx=.04, rely=.12)

# Creating Labels for Upper Window...
ent_name = Entry(key, bd=4, state=NORMAL, font='Athletic 12', bg='azure3')
ent_name.place(anchor='center', relx=.14, rely=.12, width=150)

lbl_mail = Label(key, text='Email :->', font='Algerian 15',
                 bg='azure3', fg='black')
lbl_mail.place(anchor='center', relx=.267, rely=.12)

ent_mail = Entry(key, bd=4, state=NORMAL, font='Athletic 12', bg='azure3')
ent_mail.place(anchor='center', relx=.376, rely=.12, width=175)

lbl_phno = Label(key, text='Phone No.(+91) : ',
                 font='Algerian 13', bg='azure3', fg='black')
lbl_phno.place(anchor='center', relx=.515, rely=.12)

ent_phno = Entry(key, bd=4, state=NORMAL, font='Athletic 12', bg='azure3')
ent_phno.place(anchor='center', relx=.64, rely=.12, width=165)

lbl_pur = Label(key, text='Purpose :->',
                font='Algerian 15', bg='azure3', fg='black')
lbl_pur.place(anchor='center', relx=.778, rely=.12)

ent_pur = ttk.Combobox(key, textvariable=StringVar(), values=[
                       'Select:-', 'For Packing', 'For Eating'], state='readonly')
ent_pur.place(anchor='center', relx=.91, rely=.12, width=200, height=29)
ent_pur.current(0)

lbl_tbl = Label(key, text='Table No. :->',
                font='Algerian 15', bg='azure3', fg='black')
lbl_tbl.place(anchor='center', relx=.777, rely=.18)

# creat a select list for table Table number
ent_tbl = ttk.Combobox(key, textvariable=StringVar(), values=[
                       'Select:-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'], state='readonly')
ent_tbl.place(anchor='center', relx=.91, rely=.18, width=200, height=29)
ent_tbl.current(0)


# FOr first frame or layer of windows..
frm1 = Frame(FRM, width=450, height=520, bd=12, relief="raise")
frm1.pack(side=LEFT)
frm1.configure(bg='lightsteelblue3')  # Configure the frm1 color

# FOr second frame or layer of windows..
frm2 = Frame(FRM, width=450, height=520, bd=12, relief="raise")
frm2.pack(side=LEFT)
frm2.configure(bg='slategray2')  # Configure the frm1 color

# FOr 3rd frame or layer of windows..
frm3 = Frame(FRM, width=450, height=520, bd=12, relief="raise")
frm3.pack(side=RIGHT)
frm3.configure(bg='lightsteelblue3')  # Configure the frame 3 color

# Labels for  FRAME FIRST SETUP as follows....

lbl_cate1 = Label(frm1, text="BEVERAGES :",
                  font='Algerian 17', bg='snow', fg='black')
lbl_cate1.place(anchor='center', relx=.24, rely=.05, width=200)

lbl_mstea = Label(frm1, text="Masala Tea (Rs.15/-)       :",
                  font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_mstea.place(anchor='center', relx=.24, rely=.25, width=200)

lbl_lassi = Label(frm1, text="Lassi (Rs.40/-)               :",
                  font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_lassi.place(anchor='center', relx=.24, rely=.35, width=200)

lbl_cldcf = Label(frm1, text="Cold Coffee (Rs.40/-)        :",
                  font='Athletic 12', bg='lightsteelblue3', fg='black')  # cldcf= coldcoffee
lbl_cldcf.place(anchor='center', relx=.24, rely=.45, width=200)

lbl_shake = Label(frm1, text="Chocolate Shake (Rs.60/-)  :",
                  font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_shake.place(anchor='center', relx=.24, rely=.55, width=200)

lbl_ice = Label(frm1, text="Ice Cream (Rs.30/-)         :",
                font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_ice.place(anchor='center', relx=.24, rely=.65, width=200)

lbl_htchlt = Label(frm1, text="Hot Chocolate (Rs.50/-)    :",
                   font='Athletic 12', bg='lightsteelblue3', fg='black')  # htchlt=hot coffee
lbl_htchlt.place(anchor='center', relx=.24, rely=.75, width=200)

lbl_htcf = Label(frm1, text="Hot Coffee (Rs.25/-)      :",
                 font='Athletic 12', bg='lightsteelblue3', fg='black')  # htcf = hot coffee
lbl_htcf.place(anchor='center', relx=.24, rely=.85, width=200)


# Labels for FRAME THIRD STEUP....

lbl_fstfod = Label(frm3, text="Fast Food :",
                   font='Algerian 17', bg='snow', fg='black')
lbl_fstfod.place(anchor='center', relx=.25, rely=.05, width=160)

lbl_vbgr = Label(frm3, text="Veg Burger (Rs.40/-)      :",
                 font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_vbgr.place(anchor='center', relx=.25, rely=.25, width=200)

lbl_pbgr = Label(frm3, text="Paneer Burger (Rs.50/-)   :",
                 font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_pbgr.place(anchor='center', relx=.25, rely=.35, width=200)

lbl_vroll = Label(frm3, text="Veg Roll (Rs.30/-)           :",
                  font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_vroll.place(anchor='center', relx=.25, rely=.45, width=200)

lbl_proll = Label(frm3, text="Paneer Roll (Rs.40/-)        :",
                  font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_proll.place(anchor='center', relx=.25, rely=.55, width=200)

lbl_soup = Label(frm3, text="Tomato Soup (Rs.60/-)       :",
                 font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_soup.place(anchor='center', relx=.25, rely=.65, width=200)

lbl_msoup = Label(frm3, text="Manchow Soup (Rs.80/-)     :",
                  font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_msoup.place(anchor='center', relx=.25, rely=.75, width=200)

lbl_noodle = Label(frm3, text="Hakka Noodles (Rs.120\-) :",
                   font='Athletic 12', bg='lightsteelblue3', fg='black')
lbl_noodle.place(anchor='center', relx=.25, rely=.85, width=200)


# Labels for FRAME SECOND SETUP....

lbl_tha = Label(frm2, text="Thali :", font='Algerian 17',
                bg='snow', fg='black')
lbl_tha.place(anchor='center', relx=.25, rely=.05, width=150)

lbl_thali = Label(frm2, text="Paneer Butter Masala Mix\n+\nVeg Dal Fry \n+\n2 Roti + 2 Aalo Paratha\n+\nRice + Salad\n+\nChhas/Sweet\n(Rs.200/-)",
                  font='Athletic 14', bg='slategray2', fg='black')
lbl_thali.place(anchor='center', relx=.3, rely=.4)


lbl_pytm = Label(frm2, text="Payment Mode :",
                 font='Algerian 11', bg='snow', fg='black')
lbl_pytm.place(anchor='center', relx=.25, rely=.7, width=170)

lbl_total = Label(frm2, text="Total :", font='Algerian 11',
                  bg='snow', fg='black')
lbl_total.place(anchor='center', relx=.25, rely=.80, width=170)

# Creating buttons in frame setup 2...

order = Button(frm2, text='Place Order', command=lambda: Check(),
               font='Algerian 14', state=NORMAL, bg='deepskyblue4', fg='white')
order.place(anchor='center', relx=.50, rely=.92)

# creating a Entries in Frame 1

ent_Mtea = Entry(frm1, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Mtea.place(anchor='center', relx=.77, rely=.25, width=155)
ent_Mtea.insert(0, 0)

ent_Lassi = Entry(frm1, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Lassi.place(anchor='center', relx=.77, rely=.35, width=155)
ent_Lassi.insert(0, 0)

ent_Colcof = Entry(frm1, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Colcof.place(anchor='center', relx=.77, rely=.45, width=155)
ent_Colcof.insert(0, 0)

ent_Choshake = Entry(frm1, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Choshake.place(anchor='center', relx=.77, rely=.55, width=155)
ent_Choshake.insert(0, 0)

ent_Icecrm = Entry(frm1, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Icecrm.place(anchor='center', relx=.77, rely=.65, width=155)
ent_Icecrm.insert(0, 0)

ent_Hotcho = Entry(frm1, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Hotcho.place(anchor='center', relx=.77, rely=.75, width=155)
ent_Hotcho.insert(0, 0)

ent_Hotcof = Entry(frm1, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Hotcof.place(anchor='center', relx=.77, rely=.85, width=155)
ent_Hotcof.insert(0, 0)

# Creating Entries for Frame 3.....

ent_Vburg = Entry(frm3, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Vburg.place(anchor='center', relx=.77, rely=.25, width=155)
ent_Vburg.insert(0, 0)

ent_Pburg = Entry(frm3, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Pburg.place(anchor='center', relx=.77, rely=.35, width=155)
ent_Pburg.insert(0, 0)

ent_Vroll = Entry(frm3, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Vroll.place(anchor='center', relx=.77, rely=.45, width=155)
ent_Vroll.insert(0, 0)

ent_Proll = Entry(frm3, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Proll.place(anchor='center', relx=.77, rely=.55, width=155)
ent_Proll.insert(0, 0)

ent_Tmto = Entry(frm3, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Tmto.place(anchor='center', relx=.77, rely=.65, width=155)
ent_Tmto.insert(0, 0)

ent_Mansoup = Entry(frm3, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Mansoup.place(anchor='center', relx=.77, rely=.75, width=155)
ent_Mansoup.insert(0, 0)

ent_Noodle = Entry(frm3, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Noodle.place(anchor='center', relx=.77, rely=.85, width=155)
ent_Noodle.insert(0, 0)


# Creat Entries for Frame 2...

ent_Thali = Entry(frm2, bd=4, state=NORMAL, font='Algerian 25', bg='azure3')
ent_Thali.place(anchor='center', relx=.8, rely=.4, width=70, height=70)
ent_Thali.insert(0, 0)

ent_Total = Entry(frm2, bd=4, state=NORMAL, font='Algerian', bg='azure3')
ent_Total.place(anchor='center', relx=.75, rely=.80, width=165)
ent_Total.insert(0, 0)
# disabled the entry that makes to user read only entry
ent_Total['state'] = DISABLED

ent_Payment = ttk.Combobox(
    frm2, values=['Select:-', 'Cash', 'Debit Card'], state='readonly')
ent_Payment.place(anchor='center', relx=.75, rely=.7, width=165, height=25)
ent_Payment.current(0)




key.mainloop()
