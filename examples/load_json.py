from ConfigParser import ConfigParser

data = ConfigParser.load("Test.json")
print(data.__dict__)
