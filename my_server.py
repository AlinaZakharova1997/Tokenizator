from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from cgi import FieldStorage
from windows import Context_Window
from search import SearchEngine


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        This function creates a HTML page with button and with some field
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
        self.wfile.write(bytes(html, encoding="utf-8"))

    def do_POST(self):
        form = FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        query = str(form.getvalue('query'))
        my_search = SearchEngine('TolstoyDataBase')
        final = my_search.unite_extended(query, 3)
        # field, button and query
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query" value = "%s"/>
                            <input type="submit" value="Search">
                        </form>
                 """ % query, encoding="utf-8"))
        
        # the beginning of ordered list
        self.wfile.write(bytes('<ol>', encoding="utf-8")) 
        if not final:
             self.wfile.write('NOT FOUND, SORRY', encoding="utf-8")
        for filename in final:
            self.wfile.write(bytes('<li><p> %s </p></li>' % filename, encoding="utf-8"))
            # the beginning of unordered list
            self.wfile.write(bytes('<ul>', encoding="utf-8")) 
            for window in final[filename]:
                hi_str = window.highlight_window()
                self.wfile.write(bytes('<li><p> %s </p></li>' % hi_str, encoding="utf-8"))
            self.wfile.write(bytes('</ul>', encoding="utf-8"))  
        self.wfile.write(bytes ('</ol></body></html>', encoding="utf-8"))

def main():
    my_server = HTTPServer(('', 80), RequestHandler)
    my_server.serve_forever()

if __name__ == "__main__":
    main()

