"""
HVAC Management System - GUI Application
A complete desktop application for managing HVAC leads and dispatch
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
from hvac_lead_generator import HVACLeadGenerator, HVACLead
from hvac_dispatch_system import DispatchSystem, Technician, Job

class HVACManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HVAC Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize systems
        self.lead_generator = HVACLeadGenerator()
        self.dispatch_system = DispatchSystem()
        
        # Style configuration
        self.setup_styles()
        
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.leads_frame = ttk.Frame(self.notebook)
        self.dispatch_frame = ttk.Frame(self.notebook)
        self.gps_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.leads_frame, text="Lead Management")
        self.notebook.add(self.dispatch_frame, text="Dispatch")
        self.notebook.add(self.gps_frame, text="GPS Tracking")
        self.notebook.add(self.reports_frame, text="Reports")
        
        # Setup each tab
        self.setup_leads_tab()
        self.setup_dispatch_tab()
        self.setup_gps_tab()
        self.setup_reports_tab()
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
    
    def setup_leads_tab(self):
        """Setup the Lead Management tab."""
        # Title
        title = ttk.Label(self.leads_frame, text="Lead Management System", style='Header.TLabel')
        title.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.leads_frame, text="Add New Lead")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create form fields
        fields = ['Name', 'Email', 'Phone', 'Address', 'Service Type', 'Budget']
        self.lead_entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(input_frame, text=f"{field}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            if field == 'Service Type':
                var = tk.StringVar()
                combo = ttk.Combobox(input_frame, textvariable=var, 
                                    values=['maintenance', 'repair', 'installation', 'inspection'],
                                    width=30)
                combo.grid(row=i, column=1, padx=5, pady=5)
                self.lead_entries[field] = var
            else:
                entry = ttk.Entry(input_frame, width=32)
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.lead_entries[field] = entry
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Lead", command=self.add_lead).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_lead_form).pack(side=tk.LEFT, padx=5)
        
        # Leads list frame
        list_frame = ttk.LabelFrame(self.leads_frame, text="Current Leads")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for leads
        columns = ('ID', 'Name', 'Phone', 'Service', 'Budget', 'Status')
        self.leads_tree = ttk.Treeview(list_frame, columns=columns, height=10)
        self.leads_tree.column('#0', width=0, stretch=tk.NO)
        for col in columns:
            self.leads_tree.column(col, anchor=tk.W, width=150)
            self.leads_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.leads_tree.yview)
        self.leads_tree.configure(yscroll=scrollbar.set)
        
        self.leads_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(self.leads_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Update Status", command=self.update_lead_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Export Leads", command=self.export_leads).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_leads_list).pack(side=tk.LEFT, padx=5)
    
    def setup_dispatch_tab(self):
        """Setup the Dispatch tab."""
        title = ttk.Label(self.dispatch_frame, text="Dispatch Management", style='Header.TLabel')
        title.pack(pady=10)
        
        # Technician frame
        tech_frame = ttk.LabelFrame(self.dispatch_frame, text="Technicians")
        tech_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(tech_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tech_name = ttk.Entry(tech_frame, width=30)
        self.tech_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(tech_frame, text="Skills:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.tech_skills = ttk.Entry(tech_frame, width=30)
        self.tech_skills.grid(row=1, column=1, padx=5, pady=5)
        self.tech_skills.insert(0, "HVAC, Installation, Maintenance")
        
        ttk.Button(tech_frame, text="Add Technician", command=self.add_technician).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Technician list
        tech_list_frame = ttk.LabelFrame(self.dispatch_frame, text="Available Technicians")
        tech_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tech_listbox = tk.Listbox(tech_list_frame, height=8)
        scrollbar = ttk.Scrollbar(tech_list_frame, orient=tk.VERTICAL, command=self.tech_listbox.yview)
        self.tech_listbox.configure(yscroll=scrollbar.set)
        
        self.tech_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_gps_tab(self):
        """Setup the GPS Tracking tab."""
        title = ttk.Label(self.gps_frame, text="GPS Distance Calculator", style='Header.TLabel')
        title.pack(pady=10)
        
        # Location 1
        loc1_frame = ttk.LabelFrame(self.gps_frame, text="Location 1")
        loc1_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(loc1_frame, text="Latitude:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.loc1_lat = ttk.Entry(loc1_frame, width=30)
        self.loc1_lat.grid(row=0, column=1, padx=5, pady=5)
        self.loc1_lat.insert(0, "40.7128")
        
        ttk.Label(loc1_frame, text="Longitude:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.loc1_lon = ttk.Entry(loc1_frame, width=30)
        self.loc1_lon.grid(row=1, column=1, padx=5, pady=5)
        self.loc1_lon.insert(0, "-74.0060")
        
        # Location 2
        loc2_frame = ttk.LabelFrame(self.gps_frame, text="Location 2")
        loc2_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(loc2_frame, text="Latitude:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.loc2_lat = ttk.Entry(loc2_frame, width=30)
        self.loc2_lat.grid(row=0, column=1, padx=5, pady=5)
        self.loc2_lat.insert(0, "34.0522")
        
        ttk.Label(loc2_frame, text="Longitude:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.loc2_lon = ttk.Entry(loc2_frame, width=30)
        self.loc2_lon.grid(row=1, column=1, padx=5, pady=5)
        self.loc2_lon.insert(0, "-118.2437")
        
        # Calculate button
        ttk.Button(self.gps_frame, text="Calculate Distance", command=self.calculate_distance).pack(pady=10)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.gps_frame, text="Result")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.distance_result = tk.Text(result_frame, height=10, width=60)
        self.distance_result.pack(fill=tk.BOTH, expand=True)
    
    def setup_reports_tab(self):
        """Setup the Reports tab."""
        title = ttk.Label(self.reports_frame, text="System Reports", style='Header.TLabel')
        title.pack(pady=10)
        
        # Report buttons
        button_frame = ttk.Frame(self.reports_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Lead Statistics", command=self.show_lead_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Dispatch Summary", command=self.show_dispatch_summary).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="System Overview", command=self.show_system_overview).pack(side=tk.LEFT, padx=5)
        
        # Report display
        report_frame = ttk.LabelFrame(self.reports_frame, text="Report Output")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.report_text = tk.Text(report_frame, height=20, width=80)
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscroll=scrollbar.set)
        
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Lead Management Methods
    def add_lead(self):
        """Add a new lead."""
        try:
            name = self.lead_entries['Name'].get()
            email = self.lead_entries['Email'].get()
            phone = self.lead_entries['Phone'].get()
            address = self.lead_entries['Address'].get()
            service_type = self.lead_entries['Service Type'].get()
            budget_str = self.lead_entries['Budget'].get()
            
            if not all([name, email, phone, address, service_type]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            budget = float(budget_str) if budget_str else None
            
            lead = self.lead_generator.add_lead(name, email, phone, address, service_type, budget)
            messagebox.showinfo("Success", f"Lead '{name}' added successfully!")
            self.clear_lead_form()
            self.refresh_leads_list()
        except ValueError:
            messagebox.showerror("Error", "Budget must be a valid number")
    
    def clear_lead_form(self):
        """Clear all lead form fields."""
        for field in self.lead_entries.values():
            if isinstance(field, ttk.Entry):
                field.delete(0, tk.END)
            elif isinstance(field, ttk.Combobox):
                field.set('')
    
    def refresh_leads_list(self):
        """Refresh the leads list display."""
        for item in self.leads_tree.get_children():
            self.leads_tree.delete(item)
        
        for lead in self.lead_generator.leads:
            self.leads_tree.insert('', tk.END, values=(
                lead.id[:8],
                lead.name,
                lead.phone,
                lead.service_type,
                f"${lead.budget}" if lead.budget else "N/A",
                lead.status
            ))
    
    def update_lead_status(self):
        """Update selected lead status."""
        selection = self.leads_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a lead")
            return
        
        # Create status window
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Lead Status")
        status_window.geometry("300x150")
        
        ttk.Label(status_window, text="New Status:").pack(pady=10)
        status_var = tk.StringVar()
        combo = ttk.Combobox(status_window, textvariable=status_var,
                            values=['new', 'contacted', 'qualified', 'converted', 'lost'],
                            width=27)
        combo.pack(pady=5)
        
        def apply_status():
            new_status = status_var.get()
            if new_status:
                # Find lead by index and update
                for i, lead in enumerate(self.lead_generator.leads):
                    if lead.id[:8] == self.leads_tree.item(selection[0])['values'][0]:
                        self.lead_generator.update_lead_status(lead.id, new_status)
                        messagebox.showinfo("Success", "Lead status updated!")
                        self.refresh_leads_list()
                        status_window.destroy()
                        break
        
        ttk.Button(status_window, text="Apply", command=apply_status).pack(pady=10)
    
    def export_leads(self):
        """Export leads to JSON file."""
        if not self.lead_generator.leads:
            messagebox.showwarning("Warning", "No leads to export")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            self.lead_generator.export_leads(filename)
            messagebox.showinfo("Success", f"Leads exported to {filename}")
    
    # Dispatch Methods
    def add_technician(self):
        """Add a new technician."""
        name = self.tech_name.get()
        skills_str = self.tech_skills.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter technician name")
            return
        
        skills = [s.strip() for s in skills_str.split(',')]
        tech = Technician(name, skills)
        self.dispatch_system.add_technician(tech)
        
        messagebox.showinfo("Success", f"Technician '{name}' added!")
        self.tech_name.delete(0, tk.END)
        self.refresh_technician_list()
    
    def refresh_technician_list(self):
        """Refresh technician list display."""
        self.tech_listbox.delete(0, tk.END)
        for tech in self.dispatch_system.technicians:
            self.tech_listbox.insert(tk.END, f"{tech.name} - Skills: {', '.join(tech.skills)}")
    
    # GPS Methods
    def calculate_distance(self):
        """Calculate distance between two locations."""
        try:
            lat1 = float(self.loc1_lat.get())
            lon1 = float(self.loc1_lon.get())
            lat2 = float(self.loc2_lat.get())
            lon2 = float(self.loc2_lon.get())
            
            loc1 = (lat1, lon1)
            loc2 = (lat2, lon2)
            
            distance = self.dispatch_system.calculate_distance(loc1, loc2)
            
            result_text = f"""
GPS Distance Calculation
========================

Location 1: {lat1}, {lon1}
Location 2: {lat2}, {lon2}

Distance: {distance:.2f} km
Distance: {distance * 0.621371:.2f} miles

Calculation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            self.distance_result.delete(1.0, tk.END)
            self.distance_result.insert(1.0, result_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid latitude/longitude values")
    
    # Report Methods
    def show_lead_stats(self):
        """Show lead statistics."""
        stats = self.lead_generator.get_statistics()
        report = f"""
LEAD STATISTICS REPORT
======================

Total Leads: {stats['total_leads']}
Average Budget: ${stats['average_budget']:.2f}
Total Potential Revenue: ${stats['total_potential_revenue']:.2f}

Status Breakdown:
{json.dumps(stats['status_breakdown'], indent=2)}

Service Type Breakdown:
{json.dumps(stats['service_breakdown'], indent=2)}

Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def show_dispatch_summary(self):
        """Show dispatch summary."""
        report = f"""
DISPATCH SUMMARY REPORT
======================

Total Technicians: {len(self.dispatch_system.technicians)}
Total Jobs: {len(self.dispatch_system.jobs)}

Technicians:
"""
        for tech in self.dispatch_system.technicians:
            report += f"\n  - {tech.name}"
            report += f"\n    Skills: {', '.join(tech.skills)}"
            report += f"\n    Assigned Jobs: {len(tech.assigned_jobs)}\n"
        
        report += f"""
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def show_system_overview(self):
        """Show complete system overview."""
        report = f"""
SYSTEM OVERVIEW REPORT
======================

LEAD MANAGEMENT
===============
Total Leads: {len(self.lead_generator.leads)}
Total Potential Revenue: ${self.lead_generator.get_statistics()['total_potential_revenue']:.2f}

DISPATCH MANAGEMENT
===================
Total Technicians: {len(self.dispatch_system.technicians)}
Total Jobs: {len(self.dispatch_system.jobs)}

SYSTEM STATUS
=============
System Status: OPERATIONAL
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Application Version: 1.0.0
        """
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)


def main():
    root = tk.Tk()
    app = HVACManagementApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
