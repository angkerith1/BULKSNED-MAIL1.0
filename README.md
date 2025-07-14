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
# BUKE Email Sender

A robust Python solution for sending bulk emails with multi-SMTP load balancing, automatic retries, and detailed analytics.

---

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
   - [SMTP Accounts](#1-smtp-accounts-configuration)
   - [Recipients List](#2-recipients-configuration)
   - [Email Template](#3-email-template-configuration)
   - [App Settings](#4-application-settings)
3. [Usage](#usage)
4. [Sample Output](#sample-output)
5. [Reports](#reports)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Installation

### Method 1: Manual Setup
```bash
# Clone repository
git clone https://github.com/yourusername/ultimate-bulk-sender.git
cd ultimate-bulk-sender

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
