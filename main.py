from tkinter import *
from tkinter import messagebox
from database import Database
from customer import Customer
from history import History
from sqlite3 import IntegrityError
from PIL import ImageTk, Image
from enum import Enum
from tkcalendar import DateEntry


class Window:
    def __init__(self):
        self.database = Database()
        self.root = Tk()
        self.root.title("Patient Record")
        self.__create_top_button()
        self.__create_search_bar()
        self.__create_customer_frame()
        self.__init_customer_table()
        self.root.state('zoomed')
        self.root.mainloop()

    def __create_top_button(self):
        add_patient_btn = Button(self.root, text="Add Patient", padx=10, pady=5, command=lambda: self.customer_form(OperationType.INSERT))
        add_patient_btn.pack(padx=30, pady=10, anchor=W)

    def __create_search_bar(self):
        search_frame = Frame(self.root)
        search_frame.pack(padx=30, pady=10, anchor=W)
        search_label = Label(search_frame, text="Search")
        search_label.grid(row=0, column=0)
        search_box = Entry(search_frame, width=30)
        search_box.grid(row=0, column=1)

        def _search():
            data = self.database.search_customer(search_box.get())
            try:
                self.create_customer_table(data)
            except KeyError:
                print("No search result")

        self.search_img = ImageTk.PhotoImage(Image.open("search.png").resize((20, 20)))
        search_button = Button(search_frame, text="Click", image=self.search_img, command=_search)
        search_button.grid(row=0, column=2)

    def __init_customer_table(self):
        try:
            self.create_customer_table(self.database.get_all_customer())
        except KeyError:
            print("Database is empty")

    def __create_customer_frame(self):
        main_frame = Frame(self.root, relief=GROOVE, bd=1)
        main_frame.pack(padx=30, pady=50, expand=True, fill=BOTH, anchor=W)

        canvas = Canvas(main_frame)
        self.customer_scrollable_frame = Frame(canvas)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        self.customer_scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.customer_scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, expand=True, fill=BOTH)
        scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bound_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        self.customer_scrollable_frame.bind('<Enter>', _bound_to_mousewheel)
        self.customer_scrollable_frame.bind('<Leave>', _unbound_to_mousewheel)

    def __create_history_frame(self, parent):
        main_frame = Frame(parent, relief=GROOVE, bd=1)
        main_frame.pack(padx=30, pady=50, expand=True, fill=BOTH, anchor=W)

        canvas = Canvas(main_frame)
        self.history_scrollable_frame = Frame(canvas)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        self.history_scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.history_scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, expand=True, fill=BOTH)
        scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bound_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        self.history_scrollable_frame.bind('<Enter>', _bound_to_mousewheel)
        self.history_scrollable_frame.bind('<Leave>', _unbound_to_mousewheel)

    def create_customer_table(self, data):
        for widget in self.customer_scrollable_frame.winfo_children():
            widget.destroy()
        name_lbl = Label(self.customer_scrollable_frame, text="Name", relief="raised", width=30)
        name_lbl.grid(row=0, column=0, sticky='nsew')
        ic_lbl = Label(self.customer_scrollable_frame, text="IC", relief="raised", width=20)
        ic_lbl.grid(row=0, column=1, sticky='nsew')
        phone_number_lbl = Label(self.customer_scrollable_frame, text="Phone Number", relief="raised", width=20)
        phone_number_lbl.grid(row=0, column=2, sticky='nsew', ipadx=5)
        address_lbl = Label(self.customer_scrollable_frame, text="Address", relief="raised", width=70)
        address_lbl.grid(row=0, column=3, sticky='nsew')

        if len(data) == 0:
            raise KeyError("Empty Data")

        def create_history_callback(ic):
            def callback():
                self.history_window(ic)
            return callback

        def create_edit_callback(ic):
            def callback():
                row = self.database.get_customer(ic)
                self.customer_form(OperationType.EDIT, row)
                try:
                    self.create_customer_table(self.database.get_all_customer())
                except KeyError:
                    print("Database is empty")
            return callback

        def create_delete_callback(ic):
            def callback():
                self.database.delete_customer(ic)
                try:
                    self.create_customer_table(self.database.get_all_customer())
                except KeyError:
                    print("Database is empty")
            return callback

        for row in range(len(data)):
            for column in range(len(data[0])):
                label = Label(self.customer_scrollable_frame, text=data[row][column], borderwidth=2, relief="ridge")
                label.grid(row=row+1, column=column, sticky="nsew")
            history_btn = Button(self.customer_scrollable_frame, text="History", padx=8, command=create_history_callback(int(data[row][1])))
            history_btn.grid(row=row+1, column=len(data[0])+1)
            edit_btn = Button(self.customer_scrollable_frame, text="Edit", padx=13, command=create_edit_callback(int(data[row][1])))
            edit_btn.grid(row=row + 1, column=len(data[0]) + 2)
            delete_btn = Button(self.customer_scrollable_frame, text="Delete", padx=8, command=create_delete_callback(int(data[row][1])))
            delete_btn.grid(row=row+1, column=len(data[0])+3)

    def create_history_table(self, data):
        for widget in self.history_scrollable_frame.winfo_children():
            widget.destroy()
        date_lbl = Label(self.history_scrollable_frame, text="Date", relief="raised", width=15)
        date_lbl.grid(row=0, column=0, sticky='nsew')
        symptom_lbl = Label(self.history_scrollable_frame, text="Symptom", relief="raised", width=20)
        symptom_lbl.grid(row=0, column=1, sticky='nsew')
        medicine_lbl = Label(self.history_scrollable_frame, text="Medicine", relief="raised", width=20)
        medicine_lbl.grid(row=0, column=2, sticky='nsew', ipadx=5)
        note_lbl = Label(self.history_scrollable_frame, text="Note", relief="raised", width=110)
        note_lbl.grid(row=0, column=3, sticky='nsew')

        if len(data) == 0:
            raise KeyError("Empty History table")

        ic = data[0][5]

        def create_edit_callback(rowid):
            def callback():
                row = self.database.get_history(rowid)
                self.history_form(ic, OperationType.EDIT, row, rowid)
                self.create_history_table(self.database.get_customer_history(ic))
            return callback


        def create_delete_callback(rowid):
            def callback():
                self.database.delete_history(rowid)
                try:
                    self.create_history_table(self.database.get_customer_history(ic))
                except KeyError:
                    print("Database is empty")
            return callback

        for row in range(len(data)):
            for column in range(len(data[0]) - 2):
                label = Label(self.history_scrollable_frame, text=data[row][column+1], borderwidth=2, relief="ridge")
                label.grid(row=row+1, column=column, sticky="nsew")
            edit_btn = Button(self.history_scrollable_frame, text="Edit", padx=13, command=create_edit_callback(int(data[row][0])))
            edit_btn.grid(row=row+1, column=len(data[0])+1)
            delete_btn = Button(self.history_scrollable_frame, text="Delete", padx=11, command=create_delete_callback(int(data[row][0])))
            delete_btn.grid(row=row+1, column=len(data[0])+2)

    def customer_form(self, operation_type, data=None):
        insert_window = Toplevel()
        insert_window.title("Insert Form")

        #labels
        name_lbl = Label(insert_window, text="Name")
        name_lbl.grid(row=0, column=0)
        ic_lbl = Label(insert_window, text="IC")
        ic_lbl.grid(row=1, column=0)
        phone_number_lbl = Label(insert_window, text="Phone Number")
        phone_number_lbl.grid(row=2, column=0)
        address_lbl = Label(insert_window, text="Address")
        address_lbl.grid(row=3, column=0)

        #Insert boxes
        name_entry = Entry(insert_window)
        name_entry.grid(row=0, column=1)
        ic_entry = Entry(insert_window)
        ic_entry.grid(row=1, column=1)
        phone_number_entry = Entry(insert_window)
        phone_number_entry.grid(row=2, column=1)
        address_entry = Entry(insert_window)
        address_entry.grid(row=3, column=1)

        if operation_type == OperationType.EDIT:
            name_entry.insert(0, data[0][0])
            ic_entry.insert(0, data[0][1])
            ic_entry.config(state='disabled')
            phone_number_entry.insert(0, data[0][2])
            address_entry.insert(0, data[0][3])

        #Submit button
        def _patient_submit_btn():
            name = name_entry.get()
            ic = ic_entry.get()
            phone_number = phone_number_entry.get()
            address = address_entry.get()
            customer = Customer(name, ic, phone_number, address)
            if name == "" or ic == "":
                messagebox.showwarning("Empty field", "Must fill in Name and IC")
                insert_window.state('zoomed')
                insert_window.state('normal')
                return
            if len(ic) != 12:
                messagebox.showwarning("IC incorrect length", "Please insert 12 digits IC")
                insert_window.state('zoomed')
                insert_window.state('normal')
                return

            try:
                int(ic)
            except ValueError:
                messagebox.showwarning("IC incorrect format", "Please insert 12 digits IC integer")
                insert_window.state('zoomed')
                insert_window.state('normal')
                return

            try:
                if operation_type == OperationType.INSERT:
                    self.database.insert_customer(customer)
                elif operation_type == OperationType.EDIT:
                    self.database.edit_customer(customer)
            except IntegrityError:
                messagebox.showwarning("IC value error", "IC existed in database")
                insert_window.state('zoomed')
                insert_window.state('normal')
                return
            insert_window.destroy()
            data = self.database.get_all_customer()
            self.create_customer_table(data)
        submit_btn = Button(insert_window, text="Submit", command=_patient_submit_btn)
        submit_btn.grid(row=4, column=2)

    def history_window(self, ic):
        history_window = Toplevel()
        history_window.title("History")
        history_window.state("zoomed")

        add_history_btn = Button(history_window, text="Add history", padx=10, pady=5, command=lambda: self.history_form(ic, OperationType.INSERT))
        add_history_btn.pack(padx=30, pady=10, anchor=W)

        self.__create_history_frame(history_window)
        try:
            self.create_history_table(self.database.get_customer_history(ic))
        except KeyError:
            print("Empty History table")

        back_btn = Button(history_window, text="Back", padx=30, pady=10, command=history_window.destroy)
        back_btn.pack(padx=30, pady=10, anchor=W)

    def history_form(self, ic, operation_type, data=None, rowid=None):
        insert_window = Toplevel()
        insert_window.title("Insert Form")

        #labels
        date_lbl = Label(insert_window, text="Date")
        date_lbl.grid(row=0, column=0)
        symptom_lbl = Label(insert_window, text="Symptom")
        symptom_lbl.grid(row=1, column=0)
        medicine_lbl = Label(insert_window, text="Medicine")
        medicine_lbl.grid(row=2, column=0)
        note_lbl = Label(insert_window, text="Note")
        note_lbl.grid(row=3, column=0)

        #Insert boxes
        cal = DateEntry(insert_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=0, column=1)
        symptom_entry = Entry(insert_window)
        symptom_entry.grid(row=1, column=1)
        medicine_entry = Entry(insert_window)
        medicine_entry.grid(row=2, column=1)
        note_entry = Text(insert_window, height=7, width=20)
        note_entry.grid(row=3, column=1)

        if operation_type == OperationType.EDIT:
            cal.delete(0, END)
            cal.insert(0, data[0][1])
            symptom_entry.insert(0, data[0][2])
            medicine_entry.insert(0, data[0][3])
            note_entry.insert(INSERT, data[0][4])

        #Submit button
        def _insert_history_btn(rowid=None):
            calDate = cal.get()
            symptom = symptom_entry.get()
            medicine = medicine_entry.get()
            note = note_entry.get("1.0", "end-1c")
            history = History(ic, calDate, symptom, medicine, note)

            if calDate == "":
                messagebox.showwarning("Empty field", "Must fill in Date")
                insert_window.state('zoomed')
                insert_window.state('normal')
                return

            if operation_type == OperationType.INSERT:
                self.database.insert_history(history)
            elif operation_type == OperationType.EDIT:
                self.database.edit_history(history, rowid)
            insert_window.destroy()
            data = self.database.get_customer_history(ic)
            self.create_history_table(data)
        if operation_type == OperationType.INSERT:
            submit_btn = Button(insert_window, text="Submit", command=_insert_history_btn)
        elif operation_type == OperationType.EDIT:
            submit_btn = Button(insert_window, text="Submit", command=lambda: _insert_history_btn(rowid))
        submit_btn.grid(row=4, column=2)


class OperationType(Enum):
    INSERT = 1
    EDIT = 2

if __name__ == "__main__":
    window = Window()


