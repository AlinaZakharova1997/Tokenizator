'''
My_server
This module creates a server, which processes requests and sends responses
'''

from http.server import BaseHTTPRequestHandler, HTTPServer

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
               
def main():
My_server = HTTPServer(('', 80), RequestHandler)
My_server.serve_forever()

if __name__ == "__main__":
    main()
