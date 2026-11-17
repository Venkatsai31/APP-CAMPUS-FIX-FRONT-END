import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ================= DATA =================

reports = []
next_id = 1

ISSUES = [
    "Electrical Problem",
    "Fan Not Working",
    "AC Not Working",
    "Light Not Working",
    "Projector Problem",
    "Computer Not Working",
    "Wi-Fi Problem",
    "Water Leakage",
    "Plumbing Problem",
    "Washroom Problem",
    "Furniture Damage",
    "Door / Window Damage",
    "Cleaning Required",
    "Drinking Water Problem",
    "Other"
]

TEAMS = [
    "Electrical Team",
    "Plumbing Team",
    "IT Support Team",
    "Cleaning Team",
    "Civil Maintenance Team",
    "General Maintenance Team"
]

BG = "#F3F5FA"
NAVY = "#10172B"
BLUE = "#315FEA"
WHITE = "#FFFFFF"
TEXT = "#263247"


# ================= MAIN APPLICATION =================

class CampusFix:

    def __init__(self, root):

        self.root = root
        self.root.title("CampusFix - University Maintenance System")
        self.root.geometry("1250x760")
        self.root.minsize(1050, 650)
        self.root.configure(bg=BG)

        self.role = "Student"
        self.current_page = "Dashboard"

        self.setup_styles()
        self.create_topbar()
        self.create_sidebar()
        self.create_main_area()

        self.show_page("Dashboard")

    # ================= STYLES =================

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground=TEXT,
            fieldbackground="white",
            rowheight=38,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#EAF0FA",
            foreground="#263247",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCE7FF")],
            foreground=[("selected", "#172B4D")]
        )

        style.configure("TCombobox", padding=6)

    # ================= TOP BAR =================

    def create_topbar(self):

        top = tk.Frame(self.root, bg=WHITE, height=65)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)

        tk.Label(
            top,
            text="CAMPUSFIX",
            font=("Segoe UI", 19, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(side="left", padx=25)

        tk.Label(
            top,
            text="University Issue Reporting & Maintenance",
            font=("Segoe UI", 10),
            bg=WHITE,
            fg="#758198"
        ).pack(side="left", padx=15)

        self.role_var = tk.StringVar(value="Student")

        role_box = ttk.Combobox(
            top,
            textvariable=self.role_var,
            values=["Student", "Admin", "Maintenance"],
            state="readonly",
            width=16
        )

        role_box.pack(side="right", padx=25, pady=15)
        role_box.bind(
            "<<ComboboxSelected>>",
            self.change_role
        )

        tk.Label(
            top,
            text="PORTAL:",
            bg=WHITE,
            fg="#64748B",
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

    # ================= SIDEBAR =================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=NAVY,
            width=210
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.menu_frame = tk.Frame(
            self.sidebar,
            bg=NAVY
        )

        self.menu_frame.pack(
            fill="both",
            expand=True,
            pady=20
        )

    def refresh_sidebar(self):

        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        menus = {

            "Student": [
                ("Dashboard", "▦"),
                ("Report a Problem", "+"),
                ("My Reports", "☷")
            ],

            "Admin": [
                ("Dashboard", "▦"),
                ("All Complaints", "☷"),
                ("Maintenance Teams", "⚙")
            ],

            "Maintenance": [
                ("Dashboard", "▦"),
                ("Assigned Tasks", "🔧")
            ]
        }

        tk.Label(
            self.menu_frame,
            text=self.role.upper() + " MENU",
            bg=NAVY,
            fg="#8492AC",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=20, pady=(5, 18))

        for name, symbol in menus[self.role]:

            active = name == self.current_page

            btn = tk.Button(
                self.menu_frame,
                text=f"   {symbol}    {name}",
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                bg=BLUE if active else NAVY,
                fg=WHITE if active else "#BBC6D9",
                activebackground="#263B67",
                activeforeground=WHITE,
                bd=0,
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=14,
                command=lambda p=name: self.show_page(p)
            )

            btn.pack(fill="x", padx=8, pady=3)

    # ================= MAIN AREA =================

    def create_main_area(self):

        self.main = tk.Frame(
            self.root,
            bg=BG
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

    def clear_main(self):

        for widget in self.main.winfo_children():
            widget.destroy()

    def change_role(self, event=None):

        self.role = self.role_var.get()
        self.current_page = "Dashboard"

        self.show_page("Dashboard")

    def show_page(self, page):

        self.current_page = page

        self.refresh_sidebar()
        self.clear_main()

        if page == "Dashboard":
            self.dashboard()

        elif page == "Report a Problem":
            self.student_form()

        elif page == "My Reports":
            self.student_reports()

        elif page == "All Complaints":
            self.admin_complaints()

        elif page == "Maintenance Teams":
            self.admin_complaints()

        elif page == "Assigned Tasks":
            self.maintenance_tasks()

    # ================= COMMON COMPONENTS =================

    def heading(self, title, subtitle):

        tk.Label(
            self.main,
            text=title,
            font=("Segoe UI", 23, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            self.main,
            text=subtitle,
            font=("Segoe UI", 10),
            bg=BG,
            fg="#758198"
        ).pack(anchor="w", pady=(5, 18))

    def card(self, parent=None):

        if parent is None:
            parent = self.main

        return tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground="#E0E5EF",
            highlightthickness=1,
            padx=18,
            pady=12
        )

    def button(self, parent, text, command, color=BLUE):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=18,
            pady=9,
            cursor="hand2"
        )

    def label(self, parent, text):

        tk.Label(
            parent,
            text=text,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(6, 3))

    def make_table(self, parent, columns):

        frame = tk.Frame(parent, bg=WHITE)
        frame.pack(fill="both", expand=True)

        table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for col in columns:

            table.heading(col, text=col)
            table.column(
                col,
                width=130,
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=table.yview
        )

        table.configure(
            yscrollcommand=scroll.set
        )

        table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        return table

    # ================= DASHBOARD =================

    def dashboard(self):

        self.heading(
            self.role + " Dashboard",
            "Welcome to CampusFix - Campus Maintenance Management."
        )

        if self.role == "Student":

            total = len(reports)

            solved = sum(
                r["status"] == "Issue Solved"
                for r in reports
            )

            pending = total - solved

        elif self.role == "Admin":

            total = len(reports)

            solved = sum(
                r["status"] == "Issue Solved"
                for r in reports
            )

            pending = sum(
                r["status"] != "Issue Solved"
                for r in reports
            )

        else:

            total = sum(
                r["team"] != "Not Assigned"
                for r in reports
            )

            solved = sum(
                r["status"] == "Awaiting Admin Confirmation"
                for r in reports
            )

            pending = sum(
                r["status"] == "Assigned"
                for r in reports
            )

        stats = tk.Frame(self.main, bg=BG)
        stats.pack(fill="x", pady=10)

        self.stat(stats, "Total Reports / Tasks", total, BLUE)
        self.stat(stats, "Pending / Assigned", pending, "#E69A28")
        self.stat(stats, "Completed / Awaiting", solved, "#159B78")

        if self.role == "Student":

            self.button(
                self.main,
                "+ Report New Problem",
                lambda: self.show_page("Report a Problem")
            ).pack(anchor="w", pady=15)

        elif self.role == "Admin":

            self.button(
                self.main,
                "View All Complaints",
                lambda: self.show_page("All Complaints")
            ).pack(anchor="w", pady=15)

        else:

            self.button(
                self.main,
                "View Assigned Tasks",
                lambda: self.show_page("Assigned Tasks")
            ).pack(anchor="w", pady=15)

    def stat(self, parent, title, value, color):

        box = tk.Frame(
            parent,
            bg=WHITE,
            padx=20,
            pady=15,
            highlightbackground="#E0E5EF",
            highlightthickness=1
        )

        box.pack(
            side="left",
            fill="x",
            expand=True,
            padx=6
        )

        tk.Label(
            box,
            text=title,
            bg=WHITE,
            fg="#758198",
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Label(
            box,
            text=str(value),
            bg=WHITE,
            fg=color,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", pady=5)

    # ================= STUDENT FORM =================

    def student_form(self):

        self.heading(
            "Report a Problem",
            "Enter the location and details of the campus issue."
        )

        form = self.card()
        form.pack(fill="both", expand=True)

        tk.Label(
            form,
            text="New Maintenance Complaint",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(0, 5))

        # BUILDING

        self.label(form, "Building / Block")

        self.building = ttk.Entry(
            form,
            font=("Segoe UI", 10)
        )
        self.building.pack(fill="x", ipady=3)

        # ROOM NUMBER

        self.label(form, "Room Number")

        self.room = ttk.Entry(
            form,
            font=("Segoe UI", 10)
        )
        self.room.pack(fill="x", ipady=3)

        # PROBLEM CATEGORY

        self.label(form, "Problem Category")

        self.issue = ttk.Combobox(
            form,
            values=ISSUES,
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.issue.pack(fill="x", ipady=3)

        # PROBLEM DETAILS

        self.label(form, "Problem Details")

        self.details = tk.Text(
            form,
            height=2,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            wrap="word"
        )

        self.details.pack(fill="x", pady=4)

        # SUBMIT BUTTON

        self.button(
            form,
            "SUBMIT COMPLAINT",
            self.submit_report,
            BLUE
        ).pack(anchor="e", pady=8)

    # ================= SUBMIT REPORT =================

    def submit_report(self):

        global next_id

        building = self.building.get().strip()
        room = self.room.get().strip()
        issue = self.issue.get()
        details = self.details.get(
            "1.0", "end"
        ).strip()

        if not all([
            building,
            room,
            issue,
            details
        ]):

            messagebox.showwarning(
                "Missing Information",
                "Please complete all fields."
            )

            return

        reports.append({

            "id": next_id,
            "building": building,
            "room": room,
            "issue": issue,
            "details": details,
            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            ),
            "status": "Pending Admin Review",
            "team": "Not Assigned",
            "work_note": ""

        })

        next_id += 1

        messagebox.showinfo(
            "Success",
            "Your complaint has been submitted successfully!"
        )

        self.show_page("My Reports")

    # ================= STUDENT REPORT HISTORY =================

    def student_reports(self):

        self.heading(
            "My Reports",
            "Track your complaints and their latest status."
        )

        card = self.card()
        card.pack(fill="both", expand=True)

        table = self.make_table(
            card,
            ("ID", "Building", "Room", "Problem", "Date", "Status")
        )

        for r in reports:

            table.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["building"],
                    r["room"],
                    r["issue"],
                    r["date"],
                    r["status"]
                )
            )

    # ================= ADMIN COMPLAINTS =================

    def admin_complaints(self):

        self.heading(
            "All Student Complaints",
            "Review complaints, assign teams and verify completed work."
        )

        card = self.card()
        card.pack(fill="both", expand=True)

        table = self.make_table(
            card,
            (
                "ID",
                "Building",
                "Room",
                "Problem",
                "Status",
                "Team"
            )
        )

        for r in reports:

            table.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["building"],
                    r["room"],
                    r["issue"],
                    r["status"],
                    r["team"]
                )
            )

        self.admin_table = table

        tk.Label(
            card,
            text="ADMIN ACTIONS",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(12, 5))

        row = tk.Frame(card, bg=WHITE)
        row.pack(fill="x")

        self.team_choice = ttk.Combobox(
            row,
            values=TEAMS,
            state="readonly",
            width=25
        )

        self.team_choice.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.button(
            row,
            "Assign Team",
            self.assign_team
        ).pack(side="left", padx=5)

        self.button(
            row,
            "Confirm Resolution",
            self.confirm_resolution,
            "#159B78"
        ).pack(side="left", padx=5)

        self.button(
            row,
            "View Details",
            self.view_details,
            "#64748B"
        ).pack(side="left", padx=5)

    # ================= SELECT REPORT =================

    def selected_report(self, table):

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Complaint",
                "Please select a complaint from the table."
            )

            return None

        report_id = int(
            table.item(selected[0])["values"][0]
        )

        return next(
            (
                r for r in reports
                if r["id"] == report_id
            ),
            None
        )

    # ================= ASSIGN MAINTENANCE TEAM =================

    def assign_team(self):

        r = self.selected_report(
            self.admin_table
        )

        if not r:
            return

        team = self.team_choice.get()

        if not team:

            messagebox.showwarning(
                "Select Team",
                "Please select a maintenance team."
            )

            return

        if r["status"] != "Pending Admin Review":

            messagebox.showwarning(
                "Cannot Assign",
                "Only pending complaints can be assigned."
            )

            return

        r["team"] = team
        r["status"] = "Assigned"

        messagebox.showinfo(
            "Assigned",
            f"Complaint #{r['id']} assigned to {team}."
        )

        self.show_page("All Complaints")

    # ================= VIEW COMPLAINT DETAILS =================

    def view_details(self):

        r = self.selected_report(
            self.admin_table
        )

        if not r:
            return

        details = (
            f"Complaint ID: {r['id']}\n"
            f"Building: {r['building']}\n"
            f"Room: {r['room']}\n"
            f"Problem: {r['issue']}\n"
            f"Description: {r['details']}\n"
            f"Maintenance Team: {r['team']}\n"
            f"Status: {r['status']}\n"
            f"Maintenance Note: {r['work_note']}"
        )

        messagebox.showinfo(
            "Complaint Details",
            details
        )

    # ================= MAINTENANCE TASKS =================

    def maintenance_tasks(self):

        self.heading(
            "Maintenance Tasks",
            "View assigned problems and submit work completion reports."
        )

        card = self.card()
        card.pack(fill="both", expand=True)

        table = self.make_table(
            card,
            (
                "ID",
                "Building",
                "Room",
                "Problem",
                "Team",
                "Status"
            )
        )

        for r in reports:

            if r["team"] != "Not Assigned":

                table.insert(
                    "",
                    "end",
                    values=(
                        r["id"],
                        r["building"],
                        r["room"],
                        r["issue"],
                        r["team"],
                        r["status"]
                    )
                )

        self.maintenance_table = table

        tk.Label(
            card,
            text="WORK COMPLETION REPORT",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(12, 5))

        self.work_details = tk.Text(
            card,
            height=3,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.work_details.pack(fill="x", pady=6)

        self.button(
            card,
            "Submit Resolution to Admin",
            self.resolve_task,
            "#159B78"
        ).pack(anchor="e", pady=8)

    # ================= RESOLVE MAINTENANCE TASK =================

    def resolve_task(self):

        r = self.selected_report(
            self.maintenance_table
        )

        if not r:
            return

        if r["status"] != "Assigned":

            messagebox.showwarning(
                "Invalid Action",
                "This task is not currently assigned."
            )

            return

        note = self.work_details.get(
            "1.0", "end"
        ).strip()

        if not note:

            messagebox.showwarning(
                "Missing Details",
                "Enter the work completion details."
            )

            return

        r["work_note"] = note

        r["status"] = "Awaiting Admin Confirmation"

        messagebox.showinfo(
            "Submitted",
            "Resolution report sent to admin successfully."
        )

        self.show_page("Assigned Tasks")

    # ================= ADMIN FINAL CONFIRMATION =================

    def confirm_resolution(self):

        r = self.selected_report(
            self.admin_table
        )

        if not r:
            return

        if r["status"] != "Awaiting Admin Confirmation":

            messagebox.showwarning(
                "Not Ready",
                "Maintenance team has not submitted the resolution yet."
            )

            return

        answer = messagebox.askyesno(
            "Confirm Resolution",
            "Have you verified that this problem is solved?"
        )

        if answer:

            r["status"] = "Issue Solved"

            messagebox.showinfo(
                "Confirmed",
                "Issue closed successfully! Student can now see Issue Solved."
            )

            self.show_page("All Complaints")


# ================= RUN APPLICATION =================

if __name__ == "__main__":

    root = tk.Tk()

    # OPEN APPLICATION IN MAXIMIZED WINDOW

    root.state("zoomed")

    app = CampusFix(root)

    root.mainloop()