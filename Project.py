from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup 
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder
import os
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.utils import get_color_from_hex
import sqlite3  
import datetime
import pandas as pd

# global conn1,cur1,Date_text  
Date_text = datetime.date.today()

conn1 =sqlite3.connect("Today.db")

cur1 =conn1.cursor()
cur1.execute('''
                    CREATE TABLE IF NOT EXISTS info(Id int ,Date text,Name text,Fat int,Qunatity int ,Rate int ,Total int)''')

#  crete database for store programmer details entry storege



conninfo =sqlite3.connect("Information.db")
corinfo =conninfo.cursor()
corinfo.execute('''CREATE TABLE IF NOT EXISTS info(Id int ,Date text)''')
# corinfo.execute('''INSERT INTO  info(Id,Date ) VALUES (?,?)''',(1,Date_text)) 
result =corinfo.execute('''select Date from info''')
la =[]
for i in result:
    la.append(i[0])

if len(la)==0:
    # corinfo.execute('''CREATE TABLE IF NOT EXISTS info(Id int ,Date text)''')
    corinfo.execute('''INSERT INTO  info(Id,Date ) VALUES (?,?)''',(1,Date_text)) 
    
else:
    Date_text =str(Date_text)
    if la[0]==Date_text:
        pass
    else:
        cur1.execute("drop table info")
        cur1.execute('''
                        CREATE TABLE IF NOT EXISTS info(Id int,Date text,Name text,Fat int,Qunatity int ,Rate int ,Total int)''')
        corinfo.execute("drop table info")
        corinfo.execute('''CREATE TABLE IF NOT EXISTS info(Id int ,Date text)''')
        corinfo.execute('''INSERT INTO  info(Id,Date ) VALUES (?,?)''',(1,Date_text)) 
conninfo.commit()
conninfo.close()
conn1.commit()
conn1.close()   

                 
# crete database for store a/c holder details storege
conn =sqlite3.connect("User_Names.db")  
cur =conn.cursor()
cur.execute('''
                    CREATE TABLE IF NOT EXISTS info(Id int auto_increment,Date text,Name text,Address text,phone int)''')
    
conn.commit()
conn.close() 
Window.clearcolor = get_color_from_hex('#FFC133')
Window.fullscreen =False

Builder.load_file("Project.kv")

class Main_Window(Screen):
    def __init__(self,**kwags):
        super().__init__(**kwags)

class Entry_window(Screen):
    def __init__(self,**kwags):
        super().__init__(**kwags)

    def Total(self):
        try:
            Fat =int(self.ids.Fat_text.text)  
            Quantity =int(self.ids.Quantity_text.text)
            Rate=int(self.ids.Rate_text.text) 
            Total =(Fat*Quantity*Rate)
            Total =str(Total/65)
            self.ids.Total_text.text =Total
        except:
            warning("INVALID ENTRY")
              
    def New(self):
        self.ids.Fat_text.text =""
        self.ids.Quantity_text.text =""
        self.ids.Rate_text.text ="" 
        self.ids.user_text.text =""
        self.ids.Total_text.text =""   
        

    def Save(self):
    
        try:
            if self.ids.Fat_text.text!="" and self.ids.Quantity_text.text!=""and self.ids.Rate_text.text!="" and self.ids.user_text.text!="" :
                
                User_Name =self.ids.user_text.text
                User_Name  =User_Name.lower() 
                User_Name =User_Name.capitalize()
                Fat =int(self.ids.Fat_text.text)  
                Quantity =int(self.ids.Quantity_text.text)
                Rate=int(self.ids.Rate_text.text) 
                Total =(Fat*Quantity*Rate)
                Total =int(Total/65)
                self.ids.Total_text.text =str(Total)        #print total price with save button
        except:
            warning("INVALID ENTRY")
           
        try:
            conncheck =sqlite3.connect("User_Names.db")  
            curcheck  =conncheck .cursor()
            result =curcheck .execute('''
                                        select Name from  info''')
            la =[]                                                       
            for i in result:
                la.append(i[0])
            if User_Name in la:
                conncheck.commit()
                conncheck.close() 

                layout = GridLayout(cols = 1, padding = 10)             
                popupLabel = Label(text ="INFO. WILL BE......") 
                choiceButton = Button(text = "Save",bold="True",font_size=20) 
                closeButton = Button(text = "Close",bold="True",font_size=20) 
                layout.add_widget(popupLabel) 
                layout.add_widget(choiceButton) 
                layout.add_widget(closeButton)        
                popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(300,300))              
                popup.open()  
                closeButton.bind(on_press = popup.dismiss)
                choiceButton.bind(on_release =popup.dismiss ) 
                choiceButton.bind(on_press = save_data(User_Name,Fat,Total,Rate,Quantity)) #call save_data function for info. saveing ,pass variable for data  

            else:
                warning("USER NOT RAGISTERD")
             
        except:
            pass


def save_data(User_Name,Fat,Total,Rate,Quantity):#defination of  save_data function for info. saveing ,pass variable for data
    global Date_text 
    conn =sqlite3.connect(f"{User_Name }.db")
    cur =conn.cursor()
    cur.execute('''
                  CREATE TABLE IF NOT EXISTS info(Id integer ,Date text,Name text,Fat int,Qunatity int ,Rate int ,Total int)''')
    r =cur.execute("select id from info")
    lw =[]
    for i in r:
        lw.append(i[0])   
    if len(lw) ==0:
        cur.execute('''INSERT INTO  info(Id,Date ,Name ,Fat ,Qunatity ,Rate ,Total ) VALUES (?,?,?,?,?,?,?)''',(1,Date_text,User_Name,Fat,Quantity,Rate,Total)) 
    else:
        a=lw.pop()
        a=a+1
        cur.execute('''INSERT INTO  info(Id ,Date ,Name ,Fat ,Qunatity ,Rate ,Total ) VALUES (?,?,?,?,?,?,?)''',(a,Date_text,User_Name,Fat,Quantity,Rate,Total)) 

    conn.commit()
    conn.close()
    
    conntoday =sqlite3.connect("Today.db")  
    curtoday  =conntoday.cursor()   
    re =curtoday.execute("select Id from info")
    ls =[]
    for i in re:
        ls.append(i[0])
    if len(ls)==0:
        curtoday.execute('''
                                CREATE TABLE IF NOT EXISTS info(Id int,Date text,Name text,Fat int,Qunatity int ,Rate int ,Total int)''')
        curtoday.execute('''INSERT INTO info(Id ,Date ,Name ,Fat ,Qunatity ,Rate ,Total ) VALUES (?,?,?,?,?,?,?)''',(1,Date_text,User_Name,Fat,Quantity,Rate,Total)) 
    else:
        a =ls.pop()
        a=a+1
        curtoday.execute('''
                                CREATE TABLE IF NOT EXISTS info(Id int,Date text,Name text,Fat int,Qunatity int ,Rate int ,Total int)''')
        curtoday.execute('''INSERT INTO info(Id ,Date ,Name ,Fat ,Qunatity ,Rate ,Total ) VALUES (?,?,?,?,?,?,?)''',(a,Date_text,User_Name,Fat,Quantity,Rate,Total)) 
        # curtoday.execute('''
        #                             CREATE TABLE IF NOT EXISTS info(Id int ,Date text,Name text,Fat int,Qunatity int ,Rate int ,Total int)''')
        # curtoday.execute('''INSERT INTO info(Date ,Name ,Fat ,Qunatity ,Rate ,Total ) VALUES (?,?,?,?,?,?,?)''',(a,Date_text,User_Name,Fat,Quantity,Rate,Total)) 

    conntoday.commit()
    conntoday.close()
    
    
    

class See_window(Screen):
    def __init__(self,**kwags):
        super().__init__(**kwags)

    def Today_Entry(self):
        try:
            conn =sqlite3.connect(f"Today.db")
            cur =conn.cursor()
            self.ids.text_area_today_database.text =""
            cur.execute("select * from info")
            for i in cur.fetchall():
                self.ids.text_area_today_database.insert_text("\n ", from_undo=False)
                self.ids.text_area_today_database.insert_text(f'''\t{i[0]}\t\t{i[1]}\t\t{i[2]} \t\t{i[3]}\t\t\t{i[4]}\t\t\t\t{i[5]}\t\t\t{i[6]}''', from_undo=False)
            conn.commit() 
            conn.close()
        except:
            warning("SOMETHING ROUNG")    
        
                
       
    def See_data_text(self):
        try:
            a=self.ids.See_data_text.text
            if a!="":
                if '-' in a:
                    input_value =a.split("-")
                    length =len(input_value)
                    if length==3:
                        try:
                            conn =sqlite3.connect(f"{input_value[0]}.db")
                            cur =conn.cursor()
                            self.ids.text_area_today_database.text =""
                            cur.execute(f"select * from {input_value[1]+input_value[2]}")
                            for i in cur.fetchall():
                                self.ids.text_area_today_database.insert_text("\n ", from_undo=False)
                                self.ids.text_area_today_database.insert_text(f'''\t\t\t{i[0]}\t\t\t\t{i[1]}\t\t{i[2]} \t\t{i[3]}\t\t\t{i[4]}\t\t\t\t{i[5]}\t\t\t{i[6]}''', from_undo=False)
                            conn.commit() 
                            conn.close()
                        except:
                            pass
                else:
                    conn =sqlite3.connect(f"{a}.db")
                    cur =conn.cursor()
                    self.ids.text_area_today_database.text =""
                    cur.execute("select * from info")
                    for i in cur.fetchall():
                        self.ids.text_area_today_database.insert_text("\n ", from_undo=False)
                        self.ids.text_area_today_database.insert_text(f'''\t\t\t{i[0]}\t\t\t\t{i[1]}\t\t{i[2]} \t\t{i[3]}\t\t\t{i[4]}\t\t\t\t{i[5]}\t\t\t{i[6]}''', from_undo=False)
                    conn.commit() 
                    conn.close()
                    
        except:
            pass     
            
                
    
    def  edit(self):
        database_name =self.ids.See_data_text.text
        
        database_name=database_name.lower()
        database_name=database_name.capitalize()
        if database_name!="":
            layout =BoxLayout(orientation='vertical',spacing =20,padding =20)
            popupLabel = Label(text = "old Detals",bold =True,font_size=20)
            layout.add_widget(popupLabel)
            line_no =TextInput(id="line_num",font_size=20,multiline =False,hint_text="Line Number",size_hint_y=None,height=40,size_hint_x=None,width =300)
            layout.add_widget(line_no)
            popupLabel2 = Label(text = "New Details",bold =True,font_size=20) 
            layout.add_widget(popupLabel2)
            date =TextInput(font_size=20,multiline =False,hint_text="Date",size_hint_y=None,height=40,size_hint_x=None,width =300)
            layout.add_widget(date)
            name =TextInput(font_size=20,multiline =False,hint_text=" Name",size_hint_y=None,height=40,size_hint_x=None,width =300)
            layout.add_widget(name)
            fat =TextInput(font_size=20,multiline =False,hint_text="FAT",size_hint_y=None,height=40,size_hint_x=None,width =300)
            layout.add_widget(fat)
            quantity =TextInput(font_size=20,multiline =False,hint_text=" Quantity",size_hint_y=None,height=40,size_hint_x=None,width =300)
            layout.add_widget(quantity)
            rate =TextInput(font_size=20,multiline =False,hint_text=" Rate",size_hint_y=None,height=40,size_hint_x=None,width =300)
            layout.add_widget(rate)
            choiceButton = Button(text = "Save",bold="True",font_size=20,size_hint_x=None,width =200) 
            layout.add_widget(choiceButton) 
            closeButton = Button(text = "Close",bold="True",font_size=20,size_hint_x=None,width =200) 
            layout.add_widget(closeButton)        
            popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(1300,800))              
            popup.open()    
            closeButton.bind(on_press = popup.dismiss)
            choiceButton.bind(on_release = popup.dismiss)
            choiceButton.bind(on_press= lambda x:edit_1(database_name,date,fat,quantity,rate,name,line_no))






    def  delete(self):
        a=self.ids.See_data_text.text
        if a!="":
            if '-' in a:
                b,b1 =spliter(a)
                conn =sqlite3.connect("User_Names.db")
                cur =conn.cursor() 
                r =conn.execute("select Name from info")
                ls =[]
                for i in r:
                    ls.append(i[0])
                if b1 in ls:
                        # global date2
                        layout = BoxLayout(orientation='vertical',spacing =20) 
                        date2 =TextInput(id='line',font_size=20,multiline =False,hint_text="Enter Id NUmber",size_hint_y=None,height=40,size_hint_x=None,width =350)
                        okButton = Button(text = "Done",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
                        closeButton = Button(text = "Close",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
                        layout.add_widget(date2) 
                        layout.add_widget(okButton)      
                        layout.add_widget(closeButton)    
                        popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(450,350)  )            
                        popup.open()    
                        closeButton.bind(on_press = popup.dismiss)
                        okButton.bind(on_release = popup.dismiss)
                        okButton.bind(on_press=lambda x:delete_Entry_1(date2))  
        

                else:
                    warning("This Is Not A Valid User ")   

                conn.commit()
                conn.close()
            else:
             
                layout = BoxLayout(orientation='vertical',spacing =20) 
                date1 =TextInput(id='line',font_size=20,multiline =False,hint_text="Enter Id NUmber",size_hint_y=None,height=40,size_hint_x=None,width =350)
                okButton = Button(text = "Done",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
                closeButton = Button(text = "Close",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
                layout.add_widget(date1) 
                layout.add_widget(okButton)      
                layout.add_widget(closeButton)    
                popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(450,350)  )            
                popup.open()    
                closeButton.bind(on_press = popup.dismiss)
                okButton.bind(on_release = popup.dismiss)
                okButton.bind(on_press=lambda x:delete_Entry_2(a,date1))  

    def user_list(self):
        try:
            layout = BoxLayout(orientation='vertical',spacing =20) 
            layout_2=GridLayout( size_hint_y= None,height= 25,cols= 5)
            l1=Label(text="ID",font_size=20)
            l2=Label(text="DATE",font_size=20)
            l3=Label(text="NAME",font_size=20)
            l4=Label(text="ADDRESS",font_size=20)
            l5=Label(text="PH.NO.",font_size=20)
            layout_2.add_widget(l1)
            layout_2.add_widget(l2)
            layout_2.add_widget(l3)
            layout_2.add_widget(l4)
            layout_2.add_widget(l5)
            layout.add_widget(layout_2)      
            # root = ScrollView(size_hint=(0.8, 0.5))
            data=TextInput(font_size=20)
            # data.text=""
            # root.add_widget(data)
            closeButton = Button(text = "Close",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
            layout.add_widget(data) 
            layout.add_widget(closeButton)    
            popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(1000,600) )            
            popup.open() 
            x=show_user_list(data)   
            closeButton.bind(on_press = popup.dismiss)
        except:
            warning("Something Roung")
    def print(self):
        print_file_name=self.ids.See_data_text.text
        if print_file_name!="":
            layout = BoxLayout(orientation='vertical',spacing =20) 
            date1=Label(text="Are You Sure To Print ",font_size=20)
            okButton = Button(text = "Done",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
            closeButton = Button(text = "Close",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
            layout.add_widget(date1) 
            layout.add_widget(okButton)      
            layout.add_widget(closeButton)    
            popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(250,250)  )            
            popup.open()    
            closeButton.bind(on_press = popup.dismiss)
            okButton.bind(on_release = popup.dismiss)
            # okButton.bind(on_press=self.delete_crete())
            okButton.bind(on_press=lambda x:print_1(print_file_name))

def show_user_list(data):
    try:
        conn =sqlite3.connect(f"User_Names.db")
        cur =conn.cursor()
        
        data.text="   bbc cbnx"
        r =cur.execute("select * from info")
        data.text="  "
        for i in cur.fetchall():
            data.insert_text("\n ")
            data.insert_text(f'''\t\t{i[0]}\t\t\t{i[1]}\t\t{i[2]} \t\t\t\t\t{i[3]}\t\t\t\t\t{i[4]}''')
              
        conn.commit() 
        conn.close()  
        return 0
    except:
        warning("Something Roung")
        return 0
def print_1(print_file_name):
    if '-' in print_file_name:
        try:
            file_name =print_file_name.split("-")
            if len(file_name)==3:
                datebase_name =file_name[0]
                datebase_name=datebase_name.lower()
                datebase_name=datebase_name.capitalize()
                name =datebase_name+"-"+file_name[1]+"-"+file_name[2]
                os.startfile(f"{name}.csv")
                # os.startfile(f"{x3}.xlsx")     
        except:
            file_name =print_file_name.split("-")
            if len(file_name)==3:
                datebase_name =file_name[0]
                datebase_name=datebase_name.lower()
                datebase_name=datebase_name.capitalize()
                table_name =file_name[1]+file_name[2]
                csv_name =datebase_name+"-"+file_name[1]+"-"+file_name[2]
                # name,database_name=spliter(print_file_name)
                conn =sqlite3.connect(f"{datebase_name}.db")
                cur =conn.cursor()
                df =pd.read_sql(f"select * from {table_name}",conn)
                df.to_csv(f"{csv_name}.csv",index =False)
                # df.to_exel(f"{csv_name}.xlsx")
                
                os.startfile(f"{csv_name}.csv")
                # os.startfile(f"{csv_name}.xlsx")
                
                conn.commit()
                conn.close()       
    else:
        try:
            print_file_name =print_file_name.lower()
            print_file_name =print_file_name.capitalize()
            conn =sqlite3.connect(f"{print_file_name}.db")
            cur =conn.cursor()
            Qunatity_total=conn.execute("select Qunatity from info")
            sum1=0
            for i in Qunatity_total:
                sum1=sum1+i[0]
                
            total=conn.execute("select Total from info")
            sum2=0
            for i in total:
                sum2=sum2+i[0]
            
            id=""
            User_Name=""
            Fat=""
            Rate=""
            conn.execute('''INSERT INTO info(Id ,Date ,Name ,Fat ,Qunatity ,Rate ,Total ) VALUES (?,?,?,?,?,?,?)''',(id,Date_text,User_Name,Fat,sum1,Rate,sum2))   
            
            df =pd.read_sql("select * from info",conn)
            x = datetime.datetime.now()
            x1 =str(x.year)
            x2 =x.strftime("%B")
            x2=x2.lower()
            x3 =print_file_name+"-"+x2+"-"+x1

            df.to_csv(f"{x3}.csv")
            # df.to_exel(f"{x3}.xlsx")
            x4 =x2+x1
            cur.execute(f" ALTER TABLE info RENAME TO {x4};")
            conn.commit()
            conn.close()
                    
            os.startfile(f"{x3}.csv")
            # os.startfile(f"{x3}.xlsx")
        except:
            pass      


def edit_1(database_name,date,fat,quantity,rate,name,line_no):
    try:
        conn =sqlite3.connect(f"{database_name}.db")
        cur =conn.cursor()
        if line_no.text!="":
            line_no =int(line_no.text)
            result =cur.execute("select Id from info")
            ls =[]
            for i in result:
                ls.append(i[0])
            if line_no in ls:
                try:
                    if fat.text!="":
                        fat =int(fat.text)
                        cur.execute(f'''Update info set Fat ={fat} where id = {line_no}''')
                    
                    if quantity.text!="":
                        quantity =int(quantity.text)
                        cur.execute(f'''Update info set Qunatity ={quantity} where id = {line_no}''')  
                        
                    if rate.text!="":
                        rate =int(rate.text)
                        cur.execute(f'''Update info set Rate  ={rate} where id = {line_no}''')
                    
                    if name.text!="":
                        name =name.text
                        cur.execute(f'''Update info set Name={name} where id = {line_no}''')    
                        
                    if date.text!="":
                        date =date.text
                        cur.execute(f'''Update info set Date ={date} where id = {line_no}''') 
                        
                    if  rate.text!="" and quantity.text!="" and fat.text!="": 
                        fat =int(fat.text)
                        quantity =int(quantity.text)
                        rate =int(rate.text)
                        total =fat*quantity*rate
                        total =int(total/65)
                        print(total)
                        # cur.execute(f'''Update info set Total ={total} where id = {line_no}''')  
                    warning("Edit Successfully")   
                except:
                    pass
        conn.commit()
        conn.close()

    except:
        pass
 


def delete_Entry_2(datebase_name,date1):
    try:
        line_number =date1.text
        conn =sqlite3.connect(f"{datebase_name}.db")
        cur=conn.cursor()
        conn.execute( f"delete from info where Id ={line_number}")
        conn.commit()
        conn.close()
        warning("Delete Successfully")
    except:
        warning("Error")
def delete_Entry_1(date2):
    line_number=date2.text
    try: 
        cur =conn.cursor() 
        conn.execute( f"delete from info where Id ={line_number}")
        conn.commit()
        conn.close()
    except:
        warning("Error ")  

class Crate_Window(Screen):
    def __init__(self,**kwags):
        super().__init__(**kwags)
   

    def new(self):
        self.ids.Serch_text.text=""
        self.ids.Address_text.text=""
        self.ids.ph_text.text=""
    
    def Create_new(self):
        try:
            if self.ids.Serch_text.text!="" and self.ids.Address_text.text!=""and self.ids.ph_text.text!="":
                User_entry_text =self.ids.Serch_text.text
                Address_text =self.ids.Address_text.text
                ph_text  =int(self.ids.ph_text.text)
        except:
            warning("INVALID ENTRY")
        
        try: 
            User_entry_text  =User_entry_text.lower()   
            User_entry_text  =User_entry_text.capitalize()
            conn =sqlite3.connect("User_Names.db")
            cur =conn.cursor()
            result =cur.execute('''select Name from info''')
            ls=[]
            for i in result:
                ls.append(i[0])   
            if User_entry_text in ls:
                warning("TRY ANOTHER NAME")
            else:
                conn.commit()
                r2 =cur.execute("select id from info")
                lwa =[]
                for i in r2:
                    lwa.append(i[0])  
                if len(lwa) ==0:  
                    cur.execute('''insert into info(Id,Date,Name,Address,Phone)values(?,?,?,?,?)''',(1,Date_text,User_entry_text,Address_text,ph_text))
                    warning("SAVE SUCCESSFULLY")
                else:
                    a2=lwa.pop()
                    a2=a2+1
                    cur.execute('''insert into info(Id,Date,Name,Address,Phone)values(?,?,?,?,?)''',(a2,Date_text,User_entry_text,Address_text,ph_text))

                    warning("SAVE SUCCESSFULLY")
            conn.commit()
            conn.close()        
        except:
            warning("SOMETHING ROUNG")

  
    def Delete_crete(self):
        layout = BoxLayout(orientation='vertical',spacing =20) 
        date1 =TextInput(id='line',font_size=20,multiline =False,hint_text="Enter Name",size_hint_y=None,height=40,size_hint_x=None,width =350)
        okButton = Button(text = "Done",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
        closeButton = Button(text = "Close",bold="True",font_size=20,size_hint_y=None,height=40,size_hint_x=None,width =100) 
        layout.add_widget(date1) 
        layout.add_widget(okButton)      
        layout.add_widget(closeButton)    
        popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(450,350)  )            
        popup.open()    
        closeButton.bind(on_press = popup.dismiss)
        okButton.bind(on_release = popup.dismiss)
        okButton.bind(on_press=lambda x:delete_crete(date1))
     
s =ScreenManager()
s.add_widget(Main_Window(name ="Main_Window"))
s.add_widget(Entry_window(name ="Entry_window"))
s.add_widget(See_window(name ="See_window"))
s.add_widget(Crate_Window(name ="Crate_Window"))


def delete_crete(date1):
    input_data =date1.text
    input_data  =input_data .lower()   
    input_data   =input_data .capitalize()
    
    conn =sqlite3.connect("User_Names.db")
    try:
        cur =conn.cursor()
        result =cur.execute('''select Name from info''')
        ls=[]
        
        for i in result:
            ls.append(i[0])   
        if input_data in ls:
            conn.execute('DELETE FROM info WHERE Name = (?)', (input_data,)) 
            conn1=sqlite3.connect(f"{input_data}.db")
            cur1 =conn1.cursor()
            try:
                cur1.execute('''drop table info''')
            except:
                pass    
            conn1.commit()
            conn1.close()
            warning("Delete Successfully")
        else:
            warning("User not Ragisterd")

    except:
        pass
    conn.commit()
    conn.close()    
        
    
def spliter(a): 
    r =a.split('-')
    lenght =len(r)
    r[0]=r[0].lower()
    r[0]=r[0].capitalize()
    if lenght==3:
        b =r[0]+"-"+r[1]+"-"+r[2]
        return b,r[0]
    


def warning(a):
    layout = GridLayout(cols = 1, padding = 10) 
    popupLabel = Label(text = f"{a}") 
    closeButton = Button(text = "Close",bold="True",font_size=20) 
    layout.add_widget(popupLabel) 
    layout.add_widget(closeButton)        
    popup = Popup(title ='SURBHI DAIRY', content = layout,size_hint =(None, None), size =(250,250))              
    popup.open()    
    closeButton.bind(on_press = popup.dismiss)


class myclass(App):
    def build(self):
        self.title ="Rohit Dairy"
        return s

if __name__ == "__main__":
    myclass().run()        