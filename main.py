from http.server import HTTPServer
from api.index import handler

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 10000), handler)
    print("Server running on port 10000")
    server.serve_forever()
