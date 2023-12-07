from typing import Any
import requests
from tabulate import tabulate
from tkinter import *
from datetime import datetime, timedelta
from tkinter import ttk
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import customtkinter as ctk
import random

class DATA:
    @classmethod
    def initialize(cls, tage):

        # Initialize data from WebUntis API
        cls.days = DATA.mögliche_tage(tage)
        cls.data = DATA.request_data(cls.days, tage)
        cls.clean_data = DATA.cleanup_data(cls.data, cls.days)

    @staticmethod
    def request_data(days, tage):
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        try:
            data = DATA.get_data_from_WebUntis(days, tage)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            
    @staticmethod
    def get_data_from_WebUntis(days, anzahl_tage):
        # Function to retrieve data from the WebUntis API
        
        data = {}
        # Headers, cookies, and parameters for the WebUntis API request
        
        for dates in days:
            
            datum = f"{dates[6:8]}.{dates[4:6]}.{dates[:4]}"  # dates in the format yyyymmdd and should be dd.mm.yyyy
            try:
                first_gui.status_label.config(text=f"Lade Daten für den {datum}")
                root.update()
                
            except Exception:
                pass
        
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
            
            try:
                first_gui.pb['value'] += 100/anzahl_tage
                root.update()
            except Exception:
                pass
            
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
    
    def __init__(self, master):
        
        self.scrollbar_table = ctk.CTkScrollbar(master, button_color= bg_colors['Scrollbar_slider'], button_hover_color= bg_colors['theme'])
        master.style = ttk.Style()
        
        self.keys = []
        
        for key in DATA.clean_data:
            self.keys.append(key)
        
        self.page_number = 1
        self.master = master
        
        self.selected_class = StringVar(master)
        self.selected_class.set('BG 13')
        self.selected_class.trace_add('write', self.update_gui_data)

        self.class_menu = OptionMenu(master, self.selected_class, *self.keys)
        self.class_menu.configure(relief= 'raised', bg= bg_colors['theme'],foreground= fg_colors[bg_colors['theme']], highlightthickness= 0.5)
        self.class_menu.grid(row=2, column=0, columnspan=1, padx= 5, pady= 10, sticky= 'we')
        
        self.day_entry = Entry(master, fg= 'grey')
        self.day_entry.insert(0, 'Neue Anzahl Tage...')
        self.day_entry.bind("<FocusIn>", self.on_entry_click)
        self.day_entry.bind("<FocusOut>", self.on_entry_leave)
        self.day_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        self.day_button = Button(master, text="Daten neu laden", bg= bg_colors['theme'], foreground= fg_colors[bg_colors['theme']])
        self.day_button.config(command= self.reload)
        self.day_button.grid(row=2, column=2, padx=5, pady=5, sticky='we')
        
        self.mode_button = Button(master, text='White', bg= bg_colors['theme'], foreground= fg_colors[bg_colors['theme']])
        self.mode_button.config(command= self.change_mode)
        self.mode_button.grid(row=2, column=3, columnspan=3, padx=5, pady=5, sticky='we')

        # Create a table
        self.table_view = ttk.Treeview(master, columns=(1, 2, 3, 4, 5), show='')
        self.table_view.config(yscrollcommand=self.scrollbar_table.set)
        self.table_view.grid(row=4, column=0, columnspan=3, rowspan= 8)
        
        self.scrollbar_table.configure(command=self.table_view.yview)
        self.scrollbar_table.grid(row=4, column=4, rowspan=8, sticky=NS)
        
        for index, color in enumerate(bg_colors['themes']):
            self.button = Button(bg=color)
            self.button.config(command=lambda i=color: self.change_theme(i))
            self.button.grid(column=5, row=5+index)

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
    
    def change_mode(self):
        if self.mode_button.config('text')[-1]== 'White':
            self.mode_button.config(text='Dark ')
            #White mode
            bg_colors['table_date'] = '#8c8c8c'
            bg_colors['table_odd'] = '#bfbfbf'
            bg_colors['table_even'] = '#f2f2f2'
            bg_colors['bg'] = '#bfbfbf'

        else:
            self.mode_button.config(text='White')
            #Darkmode
            bg_colors['table_date'] = '#0F0F0F'
            bg_colors['table_odd'] = '#1E1E1E'
            bg_colors['table_even'] = '#292929'
            bg_colors['bg'] = '#1E1E1E'
        
        root.configure(bg=bg_colors['bg'])
        self.update_table_view()
        
        
       
    def change_theme(self, theme):
        bg_colors['theme'] = theme
        self.day_button.config(bg= bg_colors['theme'], foreground= fg_colors[bg_colors['theme']])
        self.class_menu.config(bg= bg_colors['theme'], foreground= fg_colors[bg_colors['theme']])
        self.scrollbar_table.configure(button_color= bg_colors['Scrollbar_slider'], button_hover_color= bg_colors['theme'])
        self.mode_button.config(bg= bg_colors['theme'], foreground= fg_colors[bg_colors['theme']])
        root.update()
        self.update_table_view()
      
    def on_entry_click(self, event):
            self.day_entry.delete(0, END)
            self.day_entry.config(fg='black')  # Change text color to black

    def on_entry_leave(self, event):
            self.day_entry.insert(0, "Neue Anzahl Tage...")
            self.day_entry.config(fg='grey')  # Change text color to grey
            
    def set_column_width(self, column, width):
        self.table_view.column(column, width=width)
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

    def reload(self):
        try:
            tage = int(self.day_entry.get())
            root.focus_force()
            self.day_entry.delete(0, END)
            self.day_entry.insert(0, "Neue Anzahl Tage...")
            self.day_entry.config(fg= 'grey')
            self.day_entry.config(state= 'disabled')
            self.day_button.config(text= 'Bitte warten', state= 'disabled')
            self.class_menu.config(state= 'disabled')
            root.update()
            
            DATA.initialize(tage)
            self.update_table_view()
            self.day_entry.config(state= 'normal')
            self.day_button.config(text= 'Daten neu laden', state= 'normal')
            self.class_menu.config(state= 'normal')
            root.update()
            
        except:
            pass
    
    def update_table_view(self, *args):

        self.update_class_menu()
        self.table_view.delete(*self.table_view.get_children())
        selected_klasse = self.selected_class.get()

        # Define tags for alternating row colors
        self.table_view.tag_configure('oddrow', background= bg_colors['table_odd'], foreground= fg_colors[bg_colors['table_odd']])
        self.table_view.tag_configure('evenrow', background= bg_colors['table_even'], foreground= fg_colors[bg_colors['table_even']])  
        self.table_view.tag_configure('date', background= bg_colors['table_date'], foreground= fg_colors[bg_colors['table_date']])
        
                
        table_data = []
        
        self.table_view.insert("", "end", values=self.column_headings, tags=('header',))
        self.table_view.tag_configure('header', background=bg_colors['theme'], foreground= fg_colors[bg_colors['theme']], font=('Helvetica', 10, 'bold'))
        
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

            

    def update_gui_data(self, *args):

        # Check if clean_data is empty, and if so, select data from the next possible date
        if not DATA.clean_data:
            DATA.initialize()
        
        self.update_table_view()

    
class Startup:
    
    def __init__(self, master):
        
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", background=bg_colors['theme'], troughcolor=bg_colors['bg'])
        
        self.status_label = Label(master, text="Lade Daten, bitte Warten...", bg=bg_colors['bg'], foreground= fg_colors[bg_colors['bg']], justify= 'center')
        self.pb = ttk.Progressbar(
            root,
            orient='horizontal',
            mode='determinate',
            length=280,
            style= 'red.Horizontal.TProgressbar'
        ) 
        
        tage = 3
        self.status_label.pack()
        self.pb.pack()

        # Schedule the initialize method after a short delay
        root.after(100, self.initialize_data, tage)
        
    def initialize_data(self, tage):
        DATA.initialize(tage)
        self.status_label.destroy()
        self.pb.destroy()
        root.after(200)
        gui = GUI(root)
        root.geometry('')

bg_colors = {
    'table_date': '#0F0F0F',
    'table_odd': '#1E1E1E',
    'table_even': '#292929',
    'theme': '',
    'Scrollbar_slider': '#4d4d4d',
    'bg': '#1E1E1E',
    'themes': ['#00ffff', '#0000ff', '#000000', '#ff0000', '#ffff00', '#00ff00', '#ffffff']
    } 

fg_colors = {
    '#0F0F0F': 'white',
    '#1E1E1E': 'white',
    '#292929': 'white',
    '#00ffff': 'black',
    '4d4d4d': 'white',
    '#0000ff':'black',
    '#000000': 'white',
    '#ffff00': 'black',
    '#ffffff': 'black',
    '#00ff00': 'black',
    '#ff0000': 'black',
    '#8c8c8c': 'black',
    '#bfbfbf': 'black',
    '#f2f2f2': 'black'
    }
colors = []
for color in fg_colors.keys():
    colors.append(color)
    
bg_colors['theme'] = random.choice(colors)
        
root = Tk()
root.configure(bg=bg_colors['bg'])
root.geometry("410x100")
first_gui = Startup(root)
root.mainloop()
