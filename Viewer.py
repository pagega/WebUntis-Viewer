import requests
from tabulate import tabulate
from tkinter import *
from datetime import datetime, timedelta
from tkinter import ttk

class DATA:
    @classmethod
    def initialize(cls, date=None):
        try:
            if date is None:
                selected_date_str = GUI.selected_date.get()
                parsed_date = datetime.strptime(selected_date_str, "%A, %d.%m.%Y")
                date = parsed_date.strftime("%Y%m%d")
                
        except Exception:
            date = datetime.now().strftime("%Y%m%d")

        cls.data = cls.daten_von_webuntis(date)
        
        cls.substitutions = cls.data['payload']['rows']
        cls.classes = cls.data['payload']['affectedElements']['1']
        cls.clean_data = cls.daten_bereinigen(cls.substitutions, cls.classes)


    @staticmethod
    def daten_von_webuntis(selected_date_str):
        
        try:
            date = int(selected_date_str)
        except Exception:
            parsed_date = datetime.strptime(selected_date_str, "%A, %d.%m.%Y")
            date = parsed_date.strftime("%Y%m%d")
        
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

        response = requests.post(
            'https://kephiso.webuntis.com/WebUntis/monitor/substitution/data',
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )
        
        return response.json()

    @staticmethod
    def daten_bereinigen(Daten, Keys):
        
        Daten_kurz = {}
        
        for klassen in Keys:
            Daten_kurz[klassen] = []
            
        for eintrag in Daten:
            eintrag["data"].insert(0, eintrag["group"])
            for i in range(len(eintrag["data"])):
                eintrag["data"][i] = eintrag["data"][i].replace('<span class="substMonitorSubstElem">', "").replace('</span>', "").replace('<span class="cancelStyle">', '').replace('Raum&auml;nderung', 'Raumänderung')
            Daten_kurz[eintrag["data"][0]].append(eintrag['data'])
            
        return Daten_kurz

    @staticmethod
    def mögliche_tage():
       
        # Funktion, um Samstag und Sonntag zu überspringen
        def naechster_werktag(datum):
            while True:
                datum += timedelta(days=1)
                if datum.weekday() < 5:  # 0-4 sind Montag bis Freitag
                    return datum

        # Aktuelles Datum holen
        heutiges_datum = datetime.now()
        naechste_tage = []
        
        if heutiges_datum.weekday() != 5 and heutiges_datum.weekday() != 6:
            naechste_tage.append(f'{heutiges_datum.strftime('%A')}, {heutiges_datum.day}.{heutiges_datum.month}.{heutiges_datum.year}')
            tage = 13
        else:
            tage = 14
            
        # Liste für die nächsten 5 Werktage erstellen
        
        for _ in range(tage):
            heutiges_datum = naechster_werktag(heutiges_datum)
            naechste_tage.append(f'{heutiges_datum.strftime('%A')}, {heutiges_datum.day}.{heutiges_datum.month}.{heutiges_datum.year}')
             
        return naechste_tage

# Create the GUI
class GUI:
    
    def __init__(self, master):
        
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

        # Tabelle erstellen
        self.table_view = ttk.Treeview(master, columns=(1, 2, 3, 4, 5), show="headings")

        self.column_headings = [
                'Stunde',
                'Raum',
                'Lehrer',
                'Info',
                'Vertretungstext'
        ]
        
        # Überschriften hinzufügen
        for i in range(1, 6):
            self.table_view.heading(i, text=self.column_headings[i - 1])

        # Tabelle anzeigen
        self.table_view.grid(row=4, column=0, columnspan=2)

        # Initial update of the table
        self.update_table_view()
        
    def update_class_menu(self):
        new_keys = DATA.classes
        menu = self.class_menu['menu']
        menu.delete(0, 'end')  # Remove old options

        for key in new_keys:
            menu.add_command(label=key, command=lambda value=key: self.selected_class.set(value))
        if new_keys:
            self.selected_class.set(new_keys[0])


    def update_table_view(self, *args):
        
        self.update_class_menu()
        self.table_view.delete(*self.table_view.get_children())
        selected_klasse = self.selected_class.get()

        # Define tags for alternating row colors
        self.table_view.tag_configure('oddrow', background='#E6F7FF')  # Light Blue
        self.table_view.tag_configure('evenrow', background='#B3D9FF')  # Blue

        for index, row in enumerate(DATA.clean_data[selected_klasse]):
            row.pop(0)
            if index % 2 == 0:
                self.table_view.insert("", "end", values=row, tags=('evenrow',))
            else:
                self.table_view.insert("", "end", values=row, tags=('oddrow',))

    def update_gui_data(self, *args):
        selected_date = self.selected_date.get()
        DATA.initialize(selected_date)
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
