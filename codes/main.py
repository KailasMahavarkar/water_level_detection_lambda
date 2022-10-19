from hcsr04 import HCSR04
from time import sleep
import time

ultra = HCSR04(trigger_pin=2, echo_pin=4, echo_timeout_us=10000)
depth = 20

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(1024)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    
def trigger_hook(level, distance):
    return http_get(f"https://eoyes0r78a0d3k.m.pipedream.net/level={level}&distance={distance}")


def web_page(level, distance, timestamp):
    # led.value()
       
    html = (
        """
       <html>
	<head>
		<title>ESP Web Server</title>

		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="icon" href="data:," />

		<style>
			html {
				font-family: Helvetica;
				display: inline-block;
				margin: 0px auto;
				text-align: center;
			}
			h1 {
				color: #0f3376;
				padding: 2vh;
			}
			p {
				font-size: 1.5rem;
			}
			.button {
				display: inline-block;
				background-color: #e7bd3b;
				border: none;
				border-radius: 4px;
				color: white;
				padding: 16px 40px;
				text-decoration: none;
				font-size: 30px;
				margin: 2px;
				cursor: pointer;
			}
			.button2 {
				background-color: #4286f4;
			}
		</style>
	</head>

	<body>
		<h1>Water Level Detection</h1>
        <p>
            Water height in container is: <strong>""" + str(distance) + """</strong>
        </p>
        <p>
            Level of water remaining in cm: <strong>""" + str(level) + """</strong>
        </p>
        <p>
            Timestamp: <strong>""" + str(timestamp) + """</strong>
        </p>
        <p>
            <a href="/"><button class="button">Refresh</button></a>
        </p>
    </body>
</html>
        """
    )
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

def normalize(value, minimum, maximum):
	return ((value - minimum) / (maximum - minimum))

distance = 0
real_distance = 0
level = 0
level_real = 0

next_update = 30

rtime = int(time.time() % 120)

print("beginning the loop !")
while True:
    distance = ultra.distance_cm()
    real_distance = (depth - distance)
    level = (real_distance / depth) * 100
    real_level = level - 3
    
    # run this hook every 2 minutes
    rtime = int(time.time())
    
    if (rtime % 120 == 0):
        sleep(1)
        print(f"triggering hook")
        trigger_hook(real_level, real_distance)

    
    if (rtime % 10 == 0):
        sleep(1)
        print(f">   time now: ", time.time())
        print(f">>  water in tank: {real_distance} cm")
        print(f">>> water percentage: {level_real}\n\n")
    
    
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    request = str(request)
    #print("Content = %s" % request)

    response = web_page(real_distance, real_level, rtime)
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
