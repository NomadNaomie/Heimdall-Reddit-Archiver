import json
import multiprocessing
from Heimdall import PRAWCore


def start():
    with open("auth.json") as authJson:
        auth=json.load(authJson)
    with open("config.json") as configJSON:
        config=json.load(configJSON)

    Core = PRAWCore.PRAWCore(auth,config)

if __name__ == '__main__':
    start()
