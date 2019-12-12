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
                            <input type="submit" name="action" value="to the beginning">
                            <input type="submit" name="action" value="back">
                            <input type="submit" name="action" value="forward">
                            <br>
                            <br>
                            <label for="limit">
                            Docs per page
                            <input type="number" name="limit"  placeholder="limit">
                            </label>
                            <input type="hidden" name="offset"  placeholder="offset">
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

        limit = form.getvalue("limit")
        if not limit:
            limit = 3
        else:
            limit = int(limit)
        offset = form.getvalue("offset")
        if not offset or int(offset) < 0:
            offset = 0
        else:
            offset = int(offset)
        doc_act = form.getvalue("action")    
        if doc_act == "back" and offset != 0:
            offset = offset - limit   
        elif doc_act  == "forward":
            offset = offset + limit
        elif doc_act == "to the beginning":
            offset = 0
        # field, button and query
        self.send_response(250)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query" value="%s"/>
                            <input type="submit" name="search"  value="Search"/>
                            <input type="submit" name="action"  value="to the beginning"/>
                            <input type="submit" name="action"  value="back"/>
                            <input type="submit" name="action"  value="forward"/>
                            <br>
                            <br>
                            <label for="limit">
                            Docs per page
                            <input type="number" name="limit" placeholder="limit" value="%d"/>
                            </label>
                            <input type="hidden" name="offset" placeholder="offset"value="%d"/>
                """ % (query, limit, offset), encoding="utf-8"))    
        # I start seraching doclim and docset circle from zero
        num = 0
        # my list of (doclim,docset) pairs
        doc_limof = []
        while num < limit:
            quote_act = form.getvalue("action%d" % num)
            doclim = form.getvalue('doc%dlim' % num)
            # print(doclim, 'doclim')
            docset = form.getvalue('doc%dset' % num)
            # print(docset,'docset')
            if not doclim:
                doclim = 3
            else:
                doclim = int(doclim)
            if not docset:
                docset = 0
            else:
                docset = int(docset)
            if docset < 0:
                docset = 0
            if quote_act == "back" and docset != 0:
                docset = docset - doclim
            elif quote_act == "forward":
                docset = docset + doclim
            elif quote_act == "to the beginning":
                docset = 0    
            doc_limof.append((doclim,docset))   
            num += 1
            
        my_search = SearchEngine('TolstoyDataBase')
        # print(query)
        final = my_search.qulim_search(query, 1, limit, offset, doc_limof)
        
        # the beginning of ordered list
        self.wfile.write(bytes('<ol>', encoding="utf-8")) 
        if not final:
            self.wfile.write(bytes('NOT FOUND, SORRY', encoding="utf-8"))
        for number,filename in enumerate (sorted(final)):
            # create limit and offset for each document for it to have it's personal ones
            quote_lim = doc_limof[number][0]
            quote_offset = doc_limof[number][1]
            self.wfile.write(bytes('<li><p>%s</p>' % filename, encoding ="utf-8"))
            self.wfile.write(bytes("""
                                      <input type="submit" name="action%d"  value="to the beginning"/>
                                      <input type="submit" name="action%d"  value="back"/>
                                      <input type="submit" name="action%d"  value="forward"/>
                                      <label for="doc%dlim"> Quotes per doc
                                      <input type="number" name="doc%dlim"  value="%d"/>
                                      </label>
                                      <input type="hidden" name="doc%dset"  value="%d"/>
                                  """% (number, number,  number, number, number, quote_lim, number, quote_offset), encoding="utf-8"))
            # the beginning of unordered list
            self.wfile.write(bytes('<ul>', encoding="utf-8"))
            for quote in final[filename]:
                self.wfile.write(bytes('<li><p>%s</p></li>' % quote, encoding="utf-8"))
            self.wfile.write(bytes('</ul>', encoding="utf-8"))
            # тут дизейблить кнопки по цитатам
        self.wfile.write(bytes("""</ol</form></body></html>""", encoding="utf-8"))
        # тут разбить на два до ол и потом до формы и между дизейблить кнопки по документам

def main():
    my_server = HTTPServer(('', 80), RequestHandler)
    my_server.serve_forever()

if __name__ == "__main__":
    main()

