from http.server import BaseHTTPRequestHandler, HTTPServer 
import json
from modules.courses import get_courses 
from modules.students import get_students 
from modules.assignments import get_assignments

class Handler(BaseHTTPRequestHandler):    
    def send_json(self, data, status=200):        
        body = json.dumps(data).encode("utf-8")        
        self.send_response(status)        
        self.send_header("Content-Type", "application/json")        
        self.end_headers()        
        self.wfile.write(body)    
        
    def do_GET(self):        
        if self.path == "/":            
            self.send_json({"message": "Simple LMS Backend"})        
        elif self.path == "/health":            
            self.send_json({"status": "ok"})        
        elif self.path == "/courses":            
            self.send_json({"courses": get_courses})        
        elif self.path == "/students":            
            self.send_json({"students": get_students})        
        elif self.path == "/assignments":            
            self.send_json({"assignments": get_assignments})        
        else:            
            self.send_json({"detail": "Not Found"}, 404) 
            
server = HTTPServer(("localhost", 8000), Handler) 
print("Server running at http://localhost:8000") 
server.serve_forever()