# HVAC Management System

A complete **desktop application** for managing HVAC leads, dispatch, and GPS tracking.

## 🎯 Features

### 📋 Lead Management
- Add and track HVAC leads with contact information
- Manage lead status (new → contacted → qualified → converted → lost)
- Add notes and follow-up information
- Filter leads by status or service type
- View high-value leads by budget
- Export leads to JSON format

### 🚗 Dispatch System
- Add and manage technician profiles
- Assign technicians to jobs based on skills
- Track assigned jobs per technician
- Job scheduling with time windows
- Real-time technician availability

### 📍 GPS Tracking & Distance Calculation
- Calculate distances between GPS coordinates using Haversine formula
- Route optimization for efficient dispatching
- Real-time location tracking
- Support for real-world coordinates

### 📊 Reports & Analytics
- Lead statistics and potential revenue tracking
- Dispatch summary reports
- System overview dashboard
- Service type breakdown
- Status distribution analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/norrodn94-sudo/hvac-app.git
cd hvac-app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

**Option 1: GUI Desktop App (Recommended)**
```bash
python app.py
```
This launches the interactive graphical interface with all features.

**Option 2: Command-Line Demo**
```bash
python main.py
```
This runs an automated demo showing all system capabilities.

---

## 📁 Project Structure

```
hvac-app/
├── app.py                      # GUI Desktop Application (tkinter)
├── main.py                     # Command-line Interface
├── hvac_lead_generator.py      # Lead Management Module
├── hvac_dispatch_system.py     # Dispatch & GPS Module
├── requirements.txt            # Python Dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 📖 Usage Guide

### GUI Application (app.py)

**1. Lead Management Tab**
- Fill in lead details (name, email, phone, address, service type, budget)
- Click "Add Lead" to add to system
- View all leads in the table
- Select a lead and click "Update Status" to change status
- Click "Export Leads" to save to JSON file
- Click "Refresh" to update the display

**2. Dispatch Tab**
- Enter technician name and skills (comma-separated)
- Click "Add Technician" to register
- View available technicians in the list

**3. GPS Tracking Tab**
- Enter two GPS coordinates (latitude, longitude)
- Click "Calculate Distance" to get the distance in km and miles
- Pre-populated with NYC to LA example

**4. Reports Tab**
- Click "Lead Statistics" for revenue and status breakdown
- Click "Dispatch Summary" to see technician assignments
- Click "System Overview" for complete system status

### Command-Line Interface (main.py)

Run the automated demo:
```bash
python main.py
```

This will:
- Create sample leads
- Update lead statuses
- Add technician notes
- Display lead statistics
- Create technicians and jobs
- Assign technicians to jobs
- Calculate GPS distances
- Generate a summary report

---

## 🔧 Dependencies

- **geopy 2.3.0** - For GPS distance calculations using Haversine formula
- **tkinter** - For GUI (included with Python)

All dependencies are listed in `requirements.txt`

---

## 💡 Example Workflow

1. **Add Leads:**
   - Launch app: `python app.py`
   - Go to Lead Management tab
   - Add 3-5 sample leads with different service types

2. **Set Up Technicians:**
   - Go to Dispatch tab
   - Add technicians with relevant skills (HVAC, Installation, Repair, etc.)

3. **Calculate Distances:**
   - Go to GPS Tracking tab
   - Enter customer and technician locations
   - Get distance in km and miles

4. **View Reports:**
   - Go to Reports tab
   - Check lead statistics and potential revenue
   - View dispatch summary

5. **Export Data:**
   - Return to Lead Management tab
   - Click "Export Leads" to save as JSON

---

## 📊 Sample Data

The application comes with pre-configured examples:

**Sample Locations (GPS):**
- New York: 40.7128, -74.0060
- Los Angeles: 34.0522, -118.2437
- Chicago: 41.8781, -87.6298

**Sample Service Types:**
- Maintenance
- Repair
- Installation
- Inspection

**Lead Status Flow:**
- New → Contacted → Qualified → Converted/Lost

---

## 🐛 Troubleshooting

**Problem: "ModuleNotFoundError: No module named 'geopy'"**
```bash
pip install geopy==2.3.0
```

**Problem: "tkinter not found" (Linux)**
```bash
sudo apt-get install python3-tk
```

**Problem: GUI doesn't open**
- Make sure Python 3.7+ is installed
- Try running: `python --version`

**Problem: App crashes when calculating distance**
- Ensure you enter valid numeric coordinates
- Latitude range: -90 to 90
- Longitude range: -180 to 180

---

## 📈 Future Enhancements

Potential features for future versions:
- Database integration (SQLite/PostgreSQL)
- Email notifications for lead updates
- SMS alerts for dispatch updates
- Map visualization with real-time tracking
- Advanced route optimization algorithm
- Mobile app integration
- API for third-party integration
- User authentication and permissions
- Scheduled job reminders

---

## 📝 License

This project is open source and available for personal and commercial use.

---

## 👤 Author

**norrodn94-sudo**
- GitHub: [@norrodn94-sudo](https://github.com/norrodn94-sudo)
- Repository: [hvac-app](https://github.com/norrodn94-sudo/hvac-app)

---

## 📞 Support

For issues, feature requests, or questions:
1. Check the Troubleshooting section above
2. Review the code comments in each Python file
3. Open an issue on GitHub

---

## 🎓 Learning Resources

This project demonstrates:
- Object-Oriented Programming (OOP) in Python
- GUI development with tkinter
- File I/O and JSON handling
- Geospatial calculations
- Data management and statistics
- Business logic implementation

---

**Version:** 1.0.0  
**Last Updated:** April 2026  
**Status:** ✅ Production Ready
