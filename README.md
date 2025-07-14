# Ultimate Bulk Email Sender
A powerful Python script for sending bulk emails using multiple SMTP accounts with load balancing, retry mechanism, and detailed reporting.

## Features

- 📧 Send HTML emails to multiple recipients
- ⚖️ Load balancing across multiple SMTP accounts
- 🔄 Automatic retry mechanism for failed sends
- 📊 Detailed campaign reports with success/failure stats
- ⏱️ Multi-threaded for high performance
- 📁 Simple configuration via text files

## Prerequisites

- Python 3.6+
- Required Python packages (install via `pip install -r requirements.txt`):
---

## Installation

### Method 1: Manual Setup
```bash
# Clone repository
git clone https://github.com/angkerith1/BULKSNED-MAIL1.0.git
cd BULKSNED-MAIL1.0

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
