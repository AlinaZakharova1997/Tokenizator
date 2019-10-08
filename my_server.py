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
                            <br>
                            <br>
                            <label for="limit">
                            Docs per page
                            <input type="number" name="limit"  placeholder="limit">
                            </label>
                            <label for="offset">
                            Start from doc number
                            <input type="number" name="offset"  placeholder="offset">
                            </label>
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(html, encoding="utf-8"))

    def do_POST(self):
        '''
        This function sends search results
        '''
       
        form = FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        query = str(form.getvalue('query'))
        limit = int(form.getvalue('limit'))
        if not limit:
            limit = 5
        offset = int(form.getvalue('offset'))
        if not offset:
            offset = 0
        my_search = SearchEngine('TolstoyDataBase')
        print(query)
        final = my_search.unite_extended(query, 3)
        # field, button and query
        self.send_response(250)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query" value="%s"/>
                            <input type="submit" value="Search"/>
                            <br>
                            <br>
                            <label for="limit">
                            Docs per page
                            <input type="number" name="limit" placeholder="limit" value="%d"/>
                            </label>
                            <label for="offset">
                            Start from doc number
                            <input type="number" name="offset" placeholder="offset"value="%d"/>
                            </label>
                """ % (query,limit,offset), encoding="utf-8"))
        # the beginning of ordered list
        self.wfile.write(bytes('<ol>', encoding="utf-8")) 
        if not final:
            self.wfile.write(bytes('NOT FOUND, SORRY', encoding="utf-8"))
        for number,filename in enumerate (final):
            if number >= offset and number < limit+offset:
                self.wfile.write(bytes('<li><p>%s</p>' % filename, encoding ="utf-8"))
                # the beginning of unordered list
                self.wfile.write(bytes('<ul>', encoding="utf-8"))
                for window in final[filename]:
                    hi_str = window.highlight_window()
                    self.wfile.write(bytes('<li><p>%s</p></li>' % hi_str, encoding="utf-8"))
                self.wfile.write(bytes('</ul>', encoding="utf-8"))
            if number == limit+offset:
                break
        self.wfile.write(bytes("""</ol</form></body></html>""", encoding="utf-8"))


def main():
    my_server = HTTPServer(('', 80), RequestHandler)
    my_server.serve_forever()

if __name__ == "__main__":
    main()
