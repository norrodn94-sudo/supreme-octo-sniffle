"""
HVAC Management System - Main Application
Combines Lead Generation, Dispatch, and GPS tracking
"""

import json
from datetime import datetime
from hvac_lead_generator import HVACLeadGenerator
from hvac_dispatch_system import DispatchSystem, Technician, Job

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {{title}}")
    print("="*60 + "\n")

def run_lead_generator():
    """Run the HVAC Lead Generator."""
    print_header("HVAC LEAD GENERATOR")
    
    generator = HVACLeadGenerator()
    
    # Add sample leads
    print("Adding sample leads...\n")
    
    lead1 = generator.add_lead(
        name='John Smith',
        email='john@example.com',
        phone='555-0123',
        address='123 Main St, Springfield, IL',
        service_type='maintenance',
        budget=500
    )
    print(f"✓ Lead added: {{lead1.name}} - ID: {{lead1.id}}")
    
    lead2 = generator.add_lead(
        name='Jane Doe',
        email='jane@example.com',
        phone='555-0456',
        address='456 Oak Ave, Springfield, IL',
        service_type='installation',
        budget=5000
    )
    print(f"✓ Lead added: {{lead2.name}} - ID: {{lead2.id}}")
    
    lead3 = generator.add_lead(
        name='Bob Johnson',
        email='bob@example.com',
        phone='555-0789',
        address='789 Elm St, Springfield, IL',
        service_type='repair',
        budget=1200
    )
    print(f"✓ Lead added: {{lead3.name}} - ID: {{lead3.id}}")
    
    # Update statuses
    print("\nUpdating lead statuses...\n")
    generator.update_lead_status(lead1.id, 'contacted')
    print(f"✓ {{lead1.name}} status updated to: contacted")
    
    generator.update_lead_status(lead2.id, 'qualified')
    print(f"✓ {{lead2.name}} status updated to: qualified")
    
    # Add notes
    print("\nAdding notes to leads...\n")
    generator.add_lead_notes(lead1.id, 'Customer interested in spring maintenance package')
    print(f"✓ Notes added to {{lead1.name}}")
    
    generator.add_lead_notes(lead2.id, 'High-value lead, schedule follow-up call')
    print(f"✓ Notes added to {{lead2.name}}")
    
    # Print statistics
    print_header("LEAD STATISTICS")
    stats = generator.get_statistics()
    print(json.dumps(stats, indent=2))
    
    # Export leads
    print("\nExporting leads to JSON...\n")
    generator.export_leads('hvac_leads_export.json')
    print("✓ Leads exported to hvac_leads_export.json")
    
    return generator

def run_dispatch_system():
    """Run the HVAC Dispatch System."""
    print_header("HVAC DISPATCH SYSTEM")
    
    dispatch = DispatchSystem()
    
    # Add technicians
    print("Adding technicians...\n")
    
    tech1 = Technician('Alice Martinez', ['HVAC', 'Installation', 'Maintenance'])
    dispatch.add_technician(tech1)
    print(f"✓ Technician added: {{tech1.name}}")
    
    tech2 = Technician('Bob Wilson', ['HVAC', 'Repair', 'Troubleshooting'])
    dispatch.add_technician(tech2)
    print(f"✓ Technician added: {{tech2.name}}")
    
    tech3 = Technician('Carol Davis', ['HVAC', 'Installation', 'Inspection'])
    dispatch.add_technician(tech3)
    print(f"✓ Technician added: {{tech3.name}}")
    
    # Add jobs
    print("\nAdding jobs...\n")
    
    job1 = Job(101, (40.7128, -74.0060))  # NYC Coordinates
    dispatch.add_job(job1)
    print(f"✓ Job {{job1.job_id}} added - Location: NYC (40.7128, -74.0060)")
    
    job2 = Job(102, (34.0522, -118.2437))  # LA Coordinates
    dispatch.add_job(job2)
    print(f"✓ Job {{job2.job_id}} added - Location: LA (34.0522, -118.2437)")
    
    job3 = Job(103, (41.8781, -87.6298))  # Chicago Coordinates
    dispatch.add_job(job3)
    print(f"✓ Job {{job3.job_id}} added - Location: Chicago (41.8781, -87.6298)")
    
    # Assign technicians
    print("\nAssigning technicians to jobs...\n")
    for job in dispatch.jobs:
        dispatch.assign_technician(job)
        if job.technician:
            print(f"✓ Job {{job.job_id}} assigned to {{job.technician.name}}")
    
    # Calculate distances
    print_header("GPS DISTANCE CALCULATIONS")
    
    locations = {
        'NYC': (40.7128, -74.0060),
        'LA': (34.0522, -118.2437),
        'Chicago': (41.8781, -87.6298)
    }
    
    print("Distance between locations:\n")
    distance_nyc_la = dispatch.calculate_distance(locations['NYC'], locations['LA'])
    print(f"NYC to LA: {{distance_nyc_la:.2f}} km")
    
    distance_nyc_chicago = dispatch.calculate_distance(locations['NYC'], locations['Chicago'])
    print(f"NYC to Chicago: {{distance_nyc_chicago:.2f}} km")
    
    distance_chicago_la = dispatch.calculate_distance(locations['Chicago'], locations['LA'])
    print(f"Chicago to LA: {{distance_chicago_la:.2f}} km")
    
    return dispatch

def main():
    """Main application entry point."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     HVAC MANAGEMENT SYSTEM - LEAD & DISPATCH APP         ║")
    print("║          Lead Generation + Dispatch + GPS Tracking       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    try:
        # Run lead generator
        generator = run_lead_generator()
        
        # Run dispatch system
        dispatch = run_dispatch_system()
        
        # Summary
        print_header("APPLICATION SUMMARY")
        print(f"✓ Total Leads Generated: {{len(generator.leads)}}")
        print(f"✓ Total Technicians: {{len(dispatch.technicians)}}")
        print(f"✓ Total Jobs Dispatched: {{len(dispatch.jobs)}}")
        print(f"✓ Timestamp: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
        
        print("\n✓ Application completed successfully!")
        print("\nOutput files generated:")
        print("  - hvac_leads_export.json (Lead data)")
        
    except Exception as e:
        print(f"\n✗ Error running application: {{str(e)}}")
        print("Make sure all dependencies are installed: pip install geopy")

if __name__ == '__main__':
    main()