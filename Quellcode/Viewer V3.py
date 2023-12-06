from typing import Any
import requests
from tabulate import tabulate
from tkinter import *
from datetime import datetime, timedelta
from tkinter import ttk
import customtkinter as ctk
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class DATA:
    @classmethod
    def initialize(cls, tage):

        # Initialize data from WebUntis API
        cls.days = DATA.mögliche_tage(tage)
        cls.data = DATA.request_data(cls.days)
        cls.clean_data = DATA.cleanup_data(cls.data, cls.days)

    @staticmethod
    def request_data(days):
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        try:
            data = DATA.get_data_from_WebUntis(days)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            
    @staticmethod
    def get_data_from_WebUntis(days):
        # Function to retrieve data from the WebUntis API
        
        data = {}
        # Headers, cookies, and parameters for the WebUntis API request
        
        for dates in days:
        
            #Place cUrl command after:
            cookies = {
                'traceId': 'c6d915932d178a01b45014d09ed504ce9c790385',
                'schoolname': '"_YmJzIGZyaWVzb3l0aGU="',
                'traceId': 'c6d915932d178a01b45014d09ed504ce9c790385',
                'schoolname': '"_YmJzIGZyaWVzb3l0aGU="',
                'JSESSIONID': 'C16CF01D56D67A725BD1F196F4CB1CEA',
            }

            headers = {
                'authority': 'kephiso.webuntis.com',
                'accept': '*/*',
                'accept-language': 'de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,es-ES;q=0.6,es;q=0.5,en-US;q=0.4',
                'content-type': 'application/json',
                'dnt': '1',
                'origin': 'https://kephiso.webuntis.com',
                'referer': 'https://kephiso.webuntis.com/WebUntis/monitor?school=BBS%20Friesoythe&monitorType=subst&format=Vertretung%20heute',
                'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            params = {
                'school': 'BBS Friesoythe',
            }

            json_data = {
                'formatName': 'Vertretung morgen',
                'schoolName': 'BBS Friesoythe',
                'date': dates,
                'dateOffset': 0,
                'strikethrough': True,
                'mergeBlocks': True,
                'showOnlyFutureSub': True,
                'showBreakSupervisions': False,
                'showTeacher': True,
                'showClass': False,
                'showHour': True,
                'showInfo': True,
                'showRoom': True,
                'showSubject': False,
                'groupBy': 1,
                'hideAbsent': True,
                'departmentIds': [],
                'departmentElementType': -1,
                'hideCancelWithSubstitution': True,
                'hideCancelCausedByEvent': False,
                'showTime': False,
                'showSubstText': True,
                'showAbsentElements': [1, 2],
                'showAffectedElements': [1, 2],
                'showUnitTime': True,
                'showMessages': True,
                'showStudentgroup': False,
                'enableSubstitutionFrom': True,
                'showSubstitutionFrom': 1700,
                'showTeacherOnEvent': False,
                'showAbsentTeacher': True,
                'strikethroughAbsentTeacher': True,
                'activityTypeIds': [],
                'showEvent': False,
                'showCancel': True,
                'showOnlyCancel': False,
                'showSubstTypeColor': False,
                'showExamSupervision': False,
                'showUnheraldedExams': False,
            }

            # Make a POST request to the WebUntis API
            response = requests.post(
                'https://kephiso.webuntis.com/WebUntis/monitor/substitution/data',
                params=params,
                cookies=cookies,
                headers=headers,
                json=json_data,
            )
            
            data[dates] = response.json()
            
        #cUrl should end here. your script-block should look nearly the same as the one here
        return data

    @staticmethod
    def cleanup_data(data,days):
        #First sort data to classes.
        group_dict = {}
        for day in days:
            data[day] = data[day]['payload']['rows']
            for dicts in data[day]:
                del dicts['cssClasses']
                del dicts['cellClasses']
                key = dicts['group']
                group_dict.setdefault(key, {}).setdefault(day, []).append(dicts['data'])
                
        for classes in group_dict:
            for dates in group_dict[classes]:
                for elements in group_dict[classes][dates]:
                    
                    for i in range(len(elements)):
                        elements[i] = elements[i].replace('<span class="substMonitorSubstElem">', "").replace('</span>', "").replace('<span class="cancelStyle">', '').replace('Raum&auml;nderung', 'Raumänderung')

        return group_dict
            
    
    @staticmethod
    def mögliche_tage(iterations):
        # Function to get a list of possible dates for the GUI
       
        # Function to skip Saturday and Sunday
        def naechster_werktag(datum):
            while True:
                datum += timedelta(days=1)
                if datum.weekday() < 5:  # 0-4 are Monday to Friday
                    return datum

        # Get the current date
        heutiges_datum = datetime.now()
        naechste_tage = []
        
        if heutiges_datum.weekday() != 5 and heutiges_datum.weekday() != 6:
            naechste_tage.append(datetime.now().strftime('%Y%m%d'))
            tage = iterations - 1
        else:
            tage = iterations
            
        
        for _ in range(tage):
            heutiges_datum = naechster_werktag(heutiges_datum)
            naechste_tage.append(heutiges_datum.strftime('%Y%m%d'))
        
        return naechste_tage
    
    def umwandeln_datum(datum_integer):
        
        tage = {
            'Monday': 'Montag,',
            'Tuesday': 'Dienstag,',
            'Wednesday': 'Mittwoch,',
            'Thursday': 'Donnerstag,',
            'Friday': 'Freitag,'
        }
        
        # Formatierung des Datums als String
        datum_str = str(datum_integer)
        
        # Konvertierung des Strings in ein datetime-Objekt
        datum_obj = datetime.strptime(datum_str, '%Y%m%d')
        
        # Extrahiere Wochentag, Tag, Monat, Jahr als Liste
        datum_liste = ['date', 'Datum: ', tage[datum_obj.strftime('%A')], f'{datum_obj.day}.{datum_obj.month}.{datum_obj.year}']

        return datum_liste


# Create the GUI
class GUI:
    
    def __init__(self, master_root):
        
        self.date_color = '#0F0F0F'
        self.odd_color = '#1E1E1E'
        self.even_color = '#292929'
        self.scrollbar_color = ''
        self.heading_color = '#FF7832'
        self.class_menu_color = '#FF7832'
        
        self.master = ctk.CTkScrollableFrame(master_root,
                                    orientation=VERTICAL,
                                    fg_color='teal',
                                    scrollbar_button_color='orange',
                                    scrollbar_button_hover_color='darkorange',
                                    corner_radius=10
                                    )
        
        # Initialize the GUI
        self.keys = []
        
        for key in DATA.clean_data:
            self.keys.append(key)
        
        self.page_number = 1
        self.master = self.master
        
        self.selected_class = StringVar(self.master)
        self.selected_class.set('BG 13')
        self.selected_class.trace_add('write', self.update_gui_data)

        self.class_menu = OptionMenu(self.master, self.selected_class, *self.keys)
        self.class_menu.configure(relief= 'raised', bg= self.class_menu_color, highlightthickness= 0.5, highlightbackground= 'black', foreground = 'white')
        self.class_menu.grid(row=2, column=0, columnspan=3, padx= 500, sticky= 'we')
        
        self.empty_label = Label(root, bg= '#1E1E1E', height=1)
        self.empty_label.grid(row=1, column=0, sticky= 'we')
        self.empty_label.grid(row=3, column=0, sticky= 'we')

        # Create a table
        self.table_view = ttk.Treeview(self.master, columns=(1, 2, 3, 4, 5), show='')
        self.table_view.grid(row=4, column=0, columnspan=1)
        
        
        self.master.grid()
        '''scrollbar_table = Scrollbar(self.master, orient=VERTICAL,)
        scrollbar_table.config(command=self.table_view.yview, bg = 'black', activebackground= 'black')
        scrollbar_table.grid(row=4, column=1, rowspan= 1, sticky= NS)'''


        self.column_headings = [
                'Stunde',
                'Raum',
                'Lehrer',
                'Info',
                'Vertretungstext'
        ] 
        
        self.set_column_width(1, 100)  # Adjust the width of the first column
        self.set_column_width(2, 150)   # Adjust the width of the second column
        self.set_column_width(3, 150)  # Adjust the width of the third column
        self.set_column_width(4, 350)  # Adjust the width of the fourth column
        self.set_column_width(5, 350)  # Adjust the width of the fifth column
        

    def set_column_width(self, column, width):
        self.table_view.column(column, width=width)
        
        # Initial update of the table
        self.update_table_view()
        
    def update_class_menu(self):
        # Update the class menu options
        new_keys = self.keys
        current_value = self.selected_class.get()

        menu = self.class_menu['menu']
        menu.delete(0, 'end')  # Remove old options

        for key in new_keys:
            menu.add_command(label=key, command=lambda value=key: self.selected_class.set(value))

        if new_keys:
            # Check if the current value is in the new keys, and if not, set the default value
            if current_value not in new_keys:
                self.selected_class.set(new_keys[0])
            else:
                self.selected_class.set(current_value)

    def update_table_view(self, *args):

        self.update_class_menu()
        self.table_view.delete(*self.table_view.get_children())
        selected_klasse = self.selected_class.get()

        # Define tags for alternating row colors
        self.table_view.tag_configure('oddrow', background= self.odd_color, foreground= 'white')
        self.table_view.tag_configure('evenrow', background= self.even_color, foreground= 'white')  
        self.table_view.tag_configure('date', background= self.date_color, foreground= 'white')
        self.table_view.tag_configure('empty', background='#919191')
        
                
        table_data = []
        
        self.table_view.insert("", "end", values=self.column_headings, tags=('header',))
        self.table_view.tag_configure('header', background=self.heading_color, foreground='white', font=('Helvetica', 10, 'bold'))
        
        for dates in DATA.clean_data[selected_klasse]:
            table_data.append(DATA.umwandeln_datum(dates))
            for lists in DATA.clean_data[selected_klasse][dates]:
                table_data.append(lists)
        
        for index, content in enumerate(table_data):
                
                if content[0] == 'empty':
                    self.table_view.insert("", "end", values= [], tags=('empty'))
                elif content[0] == 'date':
                    self.table_view.insert("", "end", values=content[1:], tags=('date',))
                    index = 0
                else:
                    if index % 2 == 0:
                        self.table_view.insert("", "end", values=content, tags=('evenrow',))
                    else:
                        self.table_view.insert("", "end", values=content, tags=('oddrow',))
                        
                index += 1
                
        self.master.config()
            

    def update_gui_data(self, *args):

        # Check if clean_data is empty, and if so, select data from the next possible date
        if not DATA.clean_data:
            DATA.initialize()
        
        self.update_table_view()

    
class Startup:
    
    def __init__(self, master):
        
        self.master = master
        self.welcome_label = Label(master, text= "Willkommen, gebe hier die Anzahl der Tage ein die geladen werden sollen :)", bg='#1E1E1E', foreground= 'white')
        self.entry = Entry(master)
        self.confirm_button = Button(master,text= "Bestätige hier", command=self.confirm_clicked, bg='#FF7832', foreground= 'white')
        
        self.status_label = Label(master, text="Lade Daten, bitte Warten...", bg='#1E1E1E', foreground= 'white', justify= 'center') 
        
        self.welcome_label.grid(row=0, column=0, padx= 5, pady= 5)
        self.entry.grid(row=1, column=0, sticky= 'we', padx= 5, pady= 5)
        self.confirm_button.grid(row=2, column=0, sticky= 'we', padx= 5, pady= 5)
        
    def confirm_clicked(self):
        tage = int(self.entry.get())
        self.welcome_label.destroy()
        self.entry.destroy()
        self.confirm_button.destroy()
        self.status_label.pack()

        # Schedule the initialize method after a short delay
        root.after(100, self.initialize_data, tage)

    def initialize_data(self, tage):
        DATA.initialize(tage)
        root.destroy()
        
    def update_data(self, data):
        self.status_label.config(self.master, text=data)


root = Tk()
root.configure(bg='#1E1E1E')
root.geometry("410x100")
first_gui = Startup(root)
root.mainloop()


root = Tk()
root.configure(bg='#1E1E1E')
gui = GUI(root)
root.mainloop()
