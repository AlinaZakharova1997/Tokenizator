'''
My_server
This module creates a server, which processes requests and sends responses
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from cgi import FieldStorage
import search
from search import SearchEngine
import windows
from windows import Context_Window

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        This function creates a HTML page with button and with field
        '''
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query">
                            <input type="submit" value="Search">
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(html, encoding="UTF-8"))
        
    def do_POST(self):
        form = FieldStorage(fp = self.rfile, self.headers, environment ={'REQUEST_METHOD':'POST'})
        query = str(form.getvalue(“query”))
        my_search = SearchEngine('database')
        final = my_search.unite_extended(query)
        # field, button and query
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query" value = “%s”/>, %s>
                            <input type="submit" value="Search">
                        </form>
                 """, %query, encoding="UTF-8"))
        
        # the beginning of ordered list
        self.wfile.write(bytes('<ol>'), encoding="UTF-8") 
        if not final:
             self.wfile.write('NOT FOUND, SORRY', encoding="UTF-8")
        for filename in final.keys():
            self.wfile.write(bytes('<li><p>"%s"</p></li>'), %filename, encoding="UTF-8")
            # the beginning of unordered list
            self.wfile.write(bytes('<ul>'), encoding="UTF-8") 
            for value in final[filename]:
                hi_str = window.highlight_window()
                self.wfile.write(bytes('<li><p>"%s"</p></li>'), %hi_str, encoding="UTF-8")
            self.wfile.write(bytes('</ul>'), encoding="UTF-8")  
            self.wfile.write(bytes ('</ol></body></html>', encoding="UTF-8"))
     
               
def main():
My_server = HTTPServer(('', 80), RequestHandler)
My_server.serve_forever()

if __name__ == "__main__":
    main()
