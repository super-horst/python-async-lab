import http.client


REQUESTS=50000

if __name__ == "__main__":
    connection = http.client.HTTPConnection('localhost:8080')
    for i in range(REQUESTS):
        connection.request("GET", "/some.file")
        response = connection.getresponse().read()

