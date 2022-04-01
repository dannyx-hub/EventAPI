from configparser import ConfigParser


def dbconfig(filename="Config.ini", section='postgresql'):
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


def emailconfig(filename='Config.ini', section='email'):
    parser = ConfigParser()
    parser.read(filename)

    email = {}
    if parser.has_section(section):
        parms = parser.items(section)
        for x in parms:
            email[x[0]] = x[1]
    else:
        raise Exception()
    return email


def appconfig(filename='Config.ini', section='app'):
    parser = ConfigParser()
    parser.read(filename)

    app = {}
    if parser.has_section(section):
        parms = parser.items(section)
        for x in parms:
            app[x[0]] = x[1]
    else:
        raise Exception()

    return app