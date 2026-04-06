# HVAC Dispatch System

"""
This module provides features for managing HVAC dispatch including:
- Technician Assignment
- Route Optimization
- Job Scheduling
- Location Tracking
- Distance Calculations
"""

import geopy.distance
import datetime

class Technician:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        self.assigned_jobs = []

class Job:
    def __init__(self, job_id, location, technician=None):
        self.job_id = job_id
        self.location = location
        self.technician = technician
        self.scheduled_time = None

    def schedule_job(self, scheduled_time):
        self.scheduled_time = scheduled_time

class DispatchSystem:
    def __init__(self):
        self.technicians = []
        self.jobs = []

    def add_technician(self, technician):
        self.technicians.append(technician)

    def add_job(self, job):
        self.jobs.append(job)

    def assign_technician(self, job):
        for technician in self.technicians:
            # Simple assignment logic based on available skills
            if technician.skills:  # Placeholder condition
                job.technician = technician
                technician.assigned_jobs.append(job)
                break

    def calculate_distance(self, loc1, loc2):
        return geopy.distance.distance(loc1, loc2).km

    def optimize_routes(self):
        # Placeholder for route optimization logic
        pass

# Example Usage
if __name__ == '__main__':
    dispatch_system = DispatchSystem()
    tech1 = Technician('Alice', ['HVAC', 'Electrical'])
    dispatch_system.add_technician(tech1)
    job1 = Job(1, (40.7128, -74.0060)) # New York Coordinates
    dispatch_system.add_job(job1)
    dispatch_system.assign_technician(job1)
    print(f"Job {job1.job_id} assigned to {job1.technician.name}")
    
    # Calculating distance
    distance = dispatch_system.calculate_distance((40.7128, -74.0060), (34.0522, -118.2437)) # NY to LA
    print(f"Distance from NY to LA: {distance} km")