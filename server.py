import http.server
import socketserver
import urllib.parse
import json
import os
import smtplib
from email.message import EmailMessage

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        super().end_headers()

    def do_OPTIONS(self):
        # Respond to preflight requests
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path != '/send-email':
            self.send_error(404, "File not found")
            return
        # Read and parse form data
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length).decode('utf-8')
        fields = urllib.parse.parse_qs(post_data)
        name = fields.get('name', [''])[0]
        email = fields.get('email', [''])[0]
        message = fields.get('message', [''])[0]

        # Build email message
        gmail_user = os.getenv('GMAIL_USER')
        gmail_pass = os.getenv('GMAIL_APP_PASSWORD')
        if not gmail_user or not gmail_pass:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            resp = {'error': 'Server email configuration missing.'}
            self.wfile.write(json.dumps(resp).encode())
            return
        email_msg = EmailMessage()
        email_msg['Subject'] = f'Portfolio Contact from {name}'
        email_msg['From'] = gmail_user
        email_msg['To'] = gmail_user
        email_msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(gmail_user, gmail_pass)
                server.send_message(email_msg)
            # Success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

# Serve static files and handle POST
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT} with COOP/COEP headers")
    httpd.serve_forever()
