from configparser import ConfigParser

def config(filename="Config.ini",section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        parms = parser.items(section)
        for x in parms:
            db[x[0]] = x[1]
    else:
        raise Exception()
    return db

test = config()
print(test)