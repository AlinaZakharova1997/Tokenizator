from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from cgi import FieldStorage
from windows import Context_Window
from search import SearchEngine
import time

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
        # TIME HAS STARTED
        start_time = time.time()
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
        docs_list = []
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
            # я добавляю к лимиту единицу, это чтобы листать цитаты
            # (если есть еще одна после лимита, то можно листать, иначе - кнопка не горит!!! и врут календари)))    
            docs_list.append((doclim+1,docset))   
            num += 1
        print(docs_list,'docs_list')
        my_search = SearchEngine('TolstoyDataBase')
        # print(query)
        # еще одна пара, чтобы искать следущий документ
        doc_limof = []
        for pair in docs_list:
            doc_limof.append(pair)
        doc_limof.append((3,0))    
        print(doc_limof,'doc_limof')
        # здесь лимит по цитатам + 1
        final = my_search.qulim_search(query, 1, limit+1, offset, doc_limof)
        # условия горения кнопок по документам
        '''print(offset, 'offset')
        if offset == 0:
            self.wfile.write(bytes(""" <input type="submit" name="action"  value="to the beginning" disabled/>
                                       <input type="submit" name="action"  value="back"disabled/>""", encoding="UTF-8"))
        else:
            self.wfile.write(bytes(""" <input type="submit" name="action"  value="to the beginning"/>
                                       <input type="submit" name="action"  value="back"/>""", encoding="UTF-8"))
        print(len(final), 'len of final')    
        if len(final) < limit+1:
            self.wfile.write(bytes(""" <input type="submit" name="action"  value="forward" disabled/>""", encoding="UTF-8"))
        else:
            self.wfile.write(bytes(""" <input type="submit" name="action"  value="forward"/>""", encoding="UTF-8"))'''
            
        # the beginning of ordered list
        self.wfile.write(bytes('<ol>', encoding="utf-8")) 
        if not final:
            self.wfile.write(bytes('NOT FOUND, SORRY', encoding="utf-8"))
        # делаю срез, чтобы взять лимит минус 1 результатов, лимит+1 результат не надо показывать, он в уме
        for number,filename in enumerate(sorted(final)[:-1]):
            # create limit and offset for each document for it to have it's personal ones
            quote_lim = doc_limof[number][0]
            quote_offset = doc_limof[number][1]
            self.wfile.write(bytes('<li><p>%s</p>' % filename, encoding ="utf-8"))
            self.wfile.write(bytes("""
                                      <label for="doc%dlim"> Quotes per doc
                                      <input type="number" name="doc%dlim"  value="%d"/>
                                      </label>
                                      <input type="hidden" name="doc%dset"  value="%d"/>
                                  """% (number, number, quote_lim-1, number, quote_offset), encoding="utf-8"))
            
            # условия горения кнопок по цитатам
            print(quote_offset,'quote_offset')
            if quote_offset == 0:
                self.wfile.write(bytes(""" <input type="submit" name="action"  value="to the beginning"disabled/>
                                       <input type="submit" name="action"  value="back"disabled/>""", encoding="UTF-8"))
            else:
                self.wfile.write(bytes(""" <input type="submit" name="action"  value="to the beginning"/>
                                       <input type="submit" name="action"  value="back"/>""", encoding="UTF-8"))
            print(len(final[filename]),'len(final[filename])')
            print(quote_lim, 'quote_lim')
            if len(final[filename]) < quote_lim:
                self.wfile.write(bytes(""" <input type="submit" name="action"  value="forward"disabled/>""", encoding="UTF-8"))
            else:
                self.wfile.write(bytes(""" <input type="submit" name="action"  value="forward"/>""", encoding="UTF-8"))    
            # the beginning of unordered list
            self.wfile.write(bytes('<ul>', encoding="utf-8"))
            # вывожу цитаты до лимита по цитатам - 1
            for num, quote in enumerate (final[filename][:-1]):
                self.wfile.write(bytes('<li><p>%s</p></li>' % quote, encoding="utf-8"))
            self.wfile.write(bytes('</ul>', encoding="utf-8"))
        self.wfile.write(bytes("""</ol</form></body></html>""", encoding="utf-8"))
        print('time:', time.time() - start_time)
def main():
    my_server = HTTPServer(('', 80), RequestHandler)
    my_server.serve_forever()

if __name__ == "__main__":
    main()

