import requests
from tabulate import tabulate
from tkinter import *
from datetime import datetime, timedelta
from tkinter import ttk
import pprint

class DATA:
    @classmethod
    def initialize(cls, date=None):
        try:
            # If date is not provided, use the selected date from the GUI
            if date is None:
                selected_date_str = GUI.selected_date.get()
                parsed_date = datetime.strptime(selected_date_str, "%A, %d.%m.%Y")
                date = parsed_date.strftime("%Y%m%d")
                
        except Exception:
            # If an exception occurs, use the current date
            date = datetime.now().strftime("%Y%m%d")

        # Initialize data from WebUntis API
        cls.data = cls.get_data_from_WebUntis(date)
        
        # Extract relevant information from the API response
        cls.substitutions = cls.data['payload']['rows']
        cls.classes = cls.data['payload']['affectedElements']['1']
        cls.clean_data = cls.cleanup_data(cls.substitutions, cls.classes)


    @staticmethod
    def get_data_from_WebUntis(selected_date_str):
        # Function to retrieve data from the WebUntis API
        
        try:
            date = int(selected_date_str)
        except Exception:
            parsed_date = datetime.strptime(selected_date_str, "%A, %d.%m.%Y")
            date = parsed_date.strftime("%Y%m%d")
        
        # Headers, cookies, and parameters for the WebUntis API request
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
            'date': date,
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
        
        return response.json()

    @staticmethod
    def cleanup_data(Daten, Keys):
        # Function to clean and organize the retrieved data
        
        Daten_kurz = {}
        
        for klassen in Keys:
            Daten_kurz[klassen] = []
            
        for eintrag in Daten:
            for i in range(len(eintrag["data"])):
                eintrag["data"][i] = eintrag["data"][i].replace('<span class="substMonitorSubstElem">', "").replace('</span>', "").replace('<span class="cancelStyle">', '').replace('Raum&auml;nderung', 'Raumänderung')
            Daten_kurz[eintrag['group']].append(eintrag['data'])
            
        return Daten_kurz

    @staticmethod
    def mögliche_tage():
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
            naechste_tage.append(f'{heutiges_datum.strftime('%A')}, {heutiges_datum.day}.{heutiges_datum.month}.{heutiges_datum.year}')
            tage = 13
        else:
            tage = 14
            
        # Create a list for the next 5 workdays
        
        for _ in range(tage):
            heutiges_datum = naechster_werktag(heutiges_datum)
            naechste_tage.append(f'{heutiges_datum.strftime('%A')}, {heutiges_datum.day}.{heutiges_datum.month}.{heutiges_datum.year}')
             
        return naechste_tage

# Create the GUI
class GUI:
    
    def __init__(self, master):
        # Initialize the GUI
        
        self.selected_date = StringVar()
        
        self.master = master
        
        self.selected_class = StringVar(master)
        self.selected_class.set(DATA.classes[0])

        self.empty_label = Label(root, bg= 'white', height=1)
        self.empty_label.grid(row=1)
        
        self.selected_date = StringVar(master)
        self.selected_date.set(DATA.mögliche_tage()[0])

        self.selected_class.trace_add('write', self.update_gui_data)
        self.selected_date.trace_add('write', self.update_gui_data)

        self.class_menu = OptionMenu(master, self.selected_class, *DATA.classes)
        self.date_menu = OptionMenu(master, self.selected_date, *DATA.mögliche_tage())
        
        self.class_menu.configure(relief= 'raised', bg= 'white', highlightthickness= 0.5, highlightbackground= 'black')
        self.date_menu.configure(relief= 'raised', bg= 'white', highlightthickness= 0.5, highlightbackground= 'black')

        self.class_menu.grid(row=2, column=0)
        self.date_menu.grid(row=2, column=1)
        
        self.empty_label.grid(row=3)

        # Create a table
        self.table_view = ttk.Treeview(master, columns=(1, 2, 3, 4, 5), show="headings")

        self.column_headings = [
                'Stunde',
                'Raum',
                'Lehrer',
                'Info',
                'Vertretungstext'
        ]
        
        # Add headings
        for i in range(1, 6):
            self.table_view.heading(i, text=self.column_headings[i - 1])

        # Display the table
        self.table_view.grid(row=4, column=0, columnspan=2)

        # Initial update of the table
        self.update_table_view()
        
    def update_class_menu(self):
        # Update the class menu options
        new_keys = DATA.classes
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
        # Update the table view
        self.update_class_menu()
        self.table_view.delete(*self.table_view.get_children())
        selected_klasse = self.selected_class.get()

        # Define tags for alternating row colors
        self.table_view.tag_configure('oddrow', background='#E6F7FF')  # Light Blue
        self.table_view.tag_configure('evenrow', background='#B3D9FF')  # Blue

        for index, row in enumerate(DATA.clean_data[selected_klasse]):
            if index % 2 == 0:
                self.table_view.insert("", "end", values=row, tags=('evenrow',))
            else:
                self.table_view.insert("", "end", values=row, tags=('oddrow',))

    def update_gui_data(self, *args):
        # Update GUI data based on selected date and class
        selected_date = self.selected_date.get()
        DATA.initialize(selected_date)

        # Check if clean_data is empty, and if so, select data from the next possible date
        if not DATA.clean_data:
            next_possible_date = DATA.mögliche_tage()[1]  # Select the date from the next day
            DATA.initialize(next_possible_date)
            self.selected_date.set(next_possible_date)  # Update selected date in the GUI

        self.update_table_view()

        
# Initialize the data after the GUI is set up
DATA.initialize()

# Create the main Tkinter window
root = Tk()
root.configure(bg='white')

# Create an instance of the GUI class
gui = GUI(root)
# Start the Tkinter event loop
root.mainloop()
