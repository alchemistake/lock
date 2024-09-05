from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import time
import os
import signal
import sys
from urllib.parse import parse_qs, urlparse
from db import init_db, increment_click, get_clicks_data, get_user_total_clicks
from datetime import datetime


def email_to_user_name(email):
    name_parts = email.split('.')
    capitalized_name = ' '.join(part.capitalize() for part in name_parts)
    return capitalized_name

def shame_table():
    current_date = datetime.now()
    clicks_data = get_clicks_data()
    html_content = '<div class="shame-table">'
    html_content += f'<h1>Table of Shame - {current_date.strftime("%Y/%m")}</h1>'
    html_content += '<ol>'
    for row in clicks_data:
        capitalized_name = email_to_user_name(row[0])
        html_content += f"<li>{capitalized_name} left their computer unlocked {row[3]} times</li>"
    html_content += "</ol></div>"
    return html_content

class LockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/stats":
            self.send_stats_page()
        elif parsed_path.path == "/":
            self.send_main_page()
        elif parsed_path.path == "/favicon.ico":
            self.send_response(200)
            self.send_header("Content-type", "image/x-icon")
            self.end_headers()
            with open("static/favicon.ico", "rb") as favicon_file:
                self.wfile.write(favicon_file.read())
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"")

    def send_main_page(self):
        with open("templates/template.html", "r") as file:
            template = file.read()

        if "X-Goog-Authenticated-User-Email" in self.headers:
            email = self.headers["X-Goog-Authenticated-User-Email"].split(":")[1].split("@")[0]
            increment_click(email)
            user_total_clicks = get_user_total_clicks(email)
            capitalized_name = email_to_user_name(email)
            email_message = f"{capitalized_name}. In total you failed {user_total_clicks} times."
        else:
            email_message = "No authenticated user email found."

        html_content = template.replace("{{email_message}}", email_message)
        html_content = html_content.replace("{{shame_table}}", shame_table())

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode())

    def send_stats_page(self):
        with open("templates/shame.html", "r") as file:
            template = file.read()
        
        html_content = template.replace("{{shame_table}}", shame_table())
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode())

def run_server(port=8000):
    init_db()
    server_address = ("", port)
    httpd = HTTPServer(server_address, LockHandler)
    print(f"Server running on port {port}...")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
