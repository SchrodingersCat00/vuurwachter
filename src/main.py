from http.server import BaseHTTPRequestHandler, HTTPServer
import time

from digitemp.master import UART_Adapter
from digitemp.device import DS18B20


bus = UART_Adapter('/dev/ttyUSB0')
sensor = DS18B20(bus)
hostname = '192.168.0.118'
server_port = 8080
print(sensor.get_temperature())


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(f"<p>Temperature: {sensor.get_temperature()}</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostname, server_port), MyServer)
    print("Server started http://%s:%s" % (hostname, server_port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")