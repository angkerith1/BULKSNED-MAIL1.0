import smtplib
import os
import json
import random
import time
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
import configparser
from datetime import datetime

class UltimateBulkSender:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.initialize_files()
        self.config.read('config.ini')
        
        self.smtp_accounts = self.load_smtp_accounts()
        self.recipients = self.load_recipients()
        self.results = []
        self.lock = threading.Lock()
        
        # Settings
        self.max_workers = int(self.config.get('Settings', 'max_workers', fallback=10))
        self.retries = int(self.config.get('Settings', 'retries', fallback=2))
        self.delay = float(self.config.get('Settings', 'delay', fallback=1))

    def initialize_files(self):
        """Create necessary files if they don't exist"""
        if not os.path.exists('config.ini'):
            self.create_config()
        if not os.path.exists('smtp.txt'):
            self.create_file('smtp.txt', "smtp.example.com|587|user@example.com|password")
        if not os.path.exists('emails.txt'):
            self.create_file('emails.txt', "recipient@example.com")
        if not os.path.exists('email_template.html'):
            self.create_template()

    def create_config(self):
        """Create default config file"""
        self.config['Settings'] = {
            'max_workers': '10',
            'retries': '2',
            'delay': '1'
        }
        self.config['Email'] = {
            'subject': 'Important Message'
        }
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def create_file(self, filename, content):
        """Create file with example content"""
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Created {filename} with example data")

    def create_template(self):
        """Create default email template"""
        template = """<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #0066cc;">Hello!</h1>
        <p>This is an important message for you.</p>
        <p>Thank you for your attention.</p>
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #888;">This is an automated message.</p>
        </div>
    </div>
</body>
</html>"""
        with open('email_template.html', 'w') as f:
            f.write(template)

    def load_smtp_accounts(self):
        """Load SMTP accounts from file"""
        accounts = []
        if os.path.exists('smtp.txt'):
            with open('smtp.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('|')
                        if len(parts) >= 4:  # Requires smtp|port|user|pass
                            accounts.append({
                                'server': parts[0],
                                'port': int(parts[1]),
                                'user': parts[2],
                                'password': parts[3]
                            })
        return accounts

    def load_recipients(self):
        """Load recipient emails from file"""
        recipients = []
        if os.path.exists('emails.txt'):
            with open('emails.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        recipients.append(line)
        return recipients

    def send_email(self, recipient, smtp_account):
        """Send single email with error handling"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = smtp_account['user']
            msg['To'] = recipient
            msg['Subject'] = self.config.get('Email', 'subject', fallback='Important Message')
            
            with open('email_template.html', 'r') as f:
                html_content = f.read()
            
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(smtp_account['server'], smtp_account['port']) as server:
                server.starttls()
                server.login(smtp_account['user'], smtp_account['password'])
                server.send_message(msg)
            
            return True, None
        except Exception as e:
            return False, str(e)

    def process_recipient(self, recipient):
        """Process single recipient with retries"""
        for attempt in range(self.retries + 1):
            smtp_account = random.choice(self.smtp_accounts)
            success, error = self.send_email(recipient, smtp_account)
            
            if success:
                result = {
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success',
                    'recipient': recipient,
                    'smtp_account': smtp_account['user'],
                    'attempt': attempt + 1
                }
                with self.lock:
                    self.results.append(result)
                    print(f"✅ Sent to {recipient} via {smtp_account['user']}")
                return
            
            time.sleep(self.delay * (attempt + 1))  # Exponential backoff
        
        # If all attempts failed
        result = {
            'timestamp': datetime.now().isoformat(),
            'status': 'failed',
            'recipient': recipient,
            'error': error,
            'attempts': self.retries + 1
        }
        with self.lock:
            self.results.append(result)
            print(f"❌ Failed to send to {recipient}: {error}")

    def run_campaign(self):
        """Run the entire email campaign"""
        if not self.smtp_accounts:
            print("⛔ Error: No SMTP accounts configured in smtp.txt")
            print("Format: smtp.server|port|username|password")
            return
        
        if not self.recipients:
            print("⛔ Error: No recipients configured in emails.txt")
            return
        
        print(f"\n🚀 Starting email campaign to {len(self.recipients)} recipients")
        print(f"🔧 Using {len(self.smtp_accounts)} SMTP accounts")
        print(f"⚡ Max workers: {self.max_workers} | Retries: {self.retries} | Delay: {self.delay}s\n")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.process_recipient, self.recipients)
        
        # Save results
        self.save_results()
        
        # Print summary
        successful = sum(1 for r in self.results if r['status'] == 'success')
        elapsed = time.time() - start_time
        print(f"\n📊 Campaign completed in {elapsed:.2f} seconds")
        print(f"✅ Successful: {successful}/{len(self.recipients)}")
        print(f"❌ Failed: {len(self.recipients) - successful}")
        print(f"📁 Results saved to campaign_results.json")

    def save_results(self):
        """Save campaign results to JSON"""
        results = {
            'metadata': {
                'start_time': datetime.now().isoformat(),
                'total_recipients': len(self.recipients),
                'smtp_accounts_used': len(self.smtp_accounts),
                'success_rate': f"{sum(1 for r in self.results if r['status'] == 'success') / len(self.recipients) * 100:.2f}%"
            },
            'results': self.results
        }
        
        with open('campaign_results.json', 'w') as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    print("""
    ██████╗ ██╗   ██╗██╗  ██╗███████╗
    ██╔══██╗██║   ██║██║ ██╔╝██╔════╝
    ██████╔╝██║   ██║█████╔╝ █████╗  
    ██╔══██╗██║   ██║██╔═██╗ ██╔══╝  
    ██████╔╝╚██████╔╝██║  ██╗███████╗
    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝
    Bulk Email Sender v1.0
          DEV BY -> @RITH
    """)
    
    sender = UltimateBulkSender()
    sender.run_campaign()