from django.db import connection

class SQLLogMiddleware:

    def process_response ( self, request, response ):
        for query in connection.queries:
            print query
        return response
