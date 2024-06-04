# from typing import Literal
from twilio.rest import Client, TwilioException
from secret import Configuration
from colorama import Fore, init
from bs4 import BeautifulSoup
from lxml import etree
import requests
import os

init(autoreset=True)


class CreateConnection:
    def connect(self):
        """Connect python to Twilio REST API

        return:
            boolean: True for success and False for failure
        """
        try:
            print(f"{Fore.LIGHTCYAN_EX}Connecting to Twilio...\r", end="")
            self.__client = Client(Configuration.SID, Configuration.AUTH_TOKEN)
            print(f"{Fore.LIGHTGREEN_EX}Connected Successfully...")
            return 1
        except TwilioException as e:
            print(f"{Fore.LIGHTRED_EX}{str(e)}")
            return 0
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}{str(e)}")
            return 0

    def send_message(self, message: str, to: str = Configuration.RECEIVER, subject: str = "Update For Novel"):
        """Sends message to the user from parameter<to>

        Args:
            message (str): Text Message which is to be sent to receiver
            to (str, optional): Verified Phone number (for trial account) otherwise regular phone number of receiver. 
                Defaults to Configuration.RECEIVER.
        return:
            boolean: True for success and False for failure
        """
        print(f"{Fore.LIGHTCYAN_EX}Sending message to {to}\r", end="")
        try:
            message = self.__client.messages.create(
                body=subject + "\n" + message,
                from_=Configuration.PHONE,
                to=to,
            )
            if message.status:
                print(
                    f"{Fore.LIGHTGREEN_EX}Message has been sent successfully to {to}")
                print(f"{Fore.LIGHTBLUE_EX}SID {message.sid}")
                return 1
            print(f"{Fore.LIGHTRED_EX}Sending message to {to} failed", end="")
            return 0
        except TwilioException as e:
            print(f"{Fore.LIGHTRED_EX}{str(e)}")
            return 0
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}{str(e)}")
            return 0


class CONSTANTS:
    CHAPTER = 3062 - 1
    URL_PATTERN = "https://boxnovel.com/novel/versatile-mage-boxnovel/chapter-%s/"


class WebScrapeConfig:
    def setChapter(self, chapter_no: str = CONSTANTS.CHAPTER) -> None:
        setattr(CONSTANTS, 'CHAPTER', chapter_no)

    def getUrl(self) -> str:
        return CONSTANTS.URL_PATTERN % CONSTANTS.CHAPTER

    @property
    def updateChapterCounter(self) -> None:
        self.setChapter(str(int(CONSTANTS.CHAPTER) + 1))


class Scraper(WebScrapeConfig):
    def __init__(self) -> None:
        super().__init__()
        self.messenger = CreateConnection()
        self.isConnected = self.messenger.connect()

    def startScraping(self):
        response: requests.Response = requests.get(self.getUrl())
        soup: BeautifulSoup = BeautifulSoup(
            response.text, features='html.parser')
        targets: list[etree._Element] = etree.HTML(str(soup)).xpath(
            "/html/body/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div[1]/div[1]")
        output = ""
        for target in targets:
            p_attributes: list[etree._Element] = target.findall('p')
            for attribute in p_attributes:
                output += f"{attribute.text}\n\n"
        print(output)

    def isReleased(self, notify: bool = False):
        response: requests.Response = requests.get(self.getUrl())
        soup: BeautifulSoup = BeautifulSoup(
            response.text, features='html.parser')
        targets: list[etree._Element] = etree.HTML(str(soup)).xpath(
            "/html/body/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div/div[3]/div/div[2]")
        print(len(targets))
        if len(targets) > 0:
            a_tag: str = targets[0].find(
                'a').attrib['title'].replace("Chapter ", "").strip()
            self.setChapter(a_tag)
            if self.isConnected and notify:
                self.messenger.send_message(
                    f"New Chapter {a_tag} has been released.")
            return True
        return False


if __name__ == '__main__':
    import time
    scraper = Scraper()
    while True:
        scraper.isReleased(True)
        time.sleep(10 * 60)
