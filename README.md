# Smart Maintenance Scheduler

A professional web application to track equipment and manage maintenance schedules.

## Features

-  Equipment Management - Add, track, and manage equipment
-  Maintenance Scheduling - Automated due date calculations  
-  Service History - Complete records of all work done
-  Dashboard - View stats and recent services
-  Professional UI - Clean, easy-to-use interface

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript

## How to Install

### Step 1: Clone the Repository
```bash
git clone https://github.com/[YOUR-GITHUB-USERNAME]/smart-maintenance-scheduler.git
cd smart-maintenance-scheduler
```

### Step 2: Create Virtual Environment
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# or
source myenv/bin/activate  # Mac/Linux
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Open in Browser
http://localhost:5000

## How to Use

### Adding Equipment
1. Go to Equipment page
2. Click "+ Add Equipment"
3. Fill in equipment details
4. Click "Add Equipment"

### Creating Maintenance Schedules
1. Go to Maintenance page
2. Click "+ Add Maintenance"
3. Enter task name and frequency
4. System auto-calculates due dates

### Recording Services
1. When maintenance is due, click "Complete"
2. Enter technician name, hours, and cost
3. Service is automatically recorded

### Viewing Dashboard
- See total equipment count
- Check overdue maintenance count
- View recent services
- Track total costs

## Project Structure
smart-maintenance-scheduler/
├── app.py                      # Main Flask app
├── database.py                 # Database models
├── requirements.txt            # Python packages
│
├── static/
│   ├── css/
│   │   └── style.css           # Styling
│   └── js/
│       └── script.js           # JavaScript
│
└── templates/
├── base.html               # Navigation
├── dashboard.html          # Home page
├── equipment.html          # Equipment list
├── maintenance.html        # Maintenance tasks
└── service_history.html    # Service records

## Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

## Future Enhancements

- [ ] User authentication and login
- [ ] Email notifications for overdue maintenance
- [ ] Export reports (PDF/CSV)
- [ ] Advanced analytics and charts
- [ ] Mobile app version

## License

MIT License - See LICENSE file for details

## Author

**[Your Name]**
- GitHub: (https://github.com/mehak784)
- Email: 70147062@student.uol.edu.pk

## Support

If you have questions:
1. Check the documentation
2. Open an issue on GitHub
3. Email me directly

