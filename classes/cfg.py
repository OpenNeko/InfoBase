class ConfigError(Exception):
    def __init__(self, option, expect):
        self.a = option
        self.e = expect

    def __str__(self):
        return "Config error: {0} expected to be {1}".format(self.a, self.e)

class Config:
    def __init__(self, cfg_file):
        self.f = cfg_file
        self.info = self.parse()

    def parse(self):
        strs = 'nick', 'ident', 'real_name', 'server', 'channels'
        lists = 'owner_host'
        bools = 'ssl'
        ints = 'port'
        infos = {}

        with open(self.f, "r") as f:
            for i in f:
                i = i.split("=", 1)
                opt = i[0].strip()
                val = i[1].strip()

                if opt in strs:
                    infos[opt] = val

                elif opt in bools:
                    if val.lower() == 'on':
                        infos[opt] = True
                    elif val.lower() == 'off':
                        infos[opt] = False
                    else:
                        raise ConfigError(opt, 'on or off')

                elif opt in ints:
                    try:
                        int(val)
                    except ValueError:
                        raise ConfigError(opt, 'a number')
                    else:
                        infos[opt] = int(val)

                elif opt in lists:
                    tmp = val.split(",")
                    for i in enumerate(tmp):
                        tmp[i[0]] = i[1].strip()
                    infos[opt] = tmp

                else:
                    pass

        return infos
