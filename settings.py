from configparser import ConfigParser, SectionProxy as Section


class Setting(object):
    def __init__(self, fname="settings.ini"):
        self.fname = fname
        self.parser = ConfigParser()

        self._read()
        self._proxy = self.__dict__

    @property
    def __dict__(self):
        return dict((k, self._parse_any(v)) for k, v in {**self.parser}.items())

    @property
    def conf(self):
        return self._proxy

    def _read(self):
        self.parser.read(self.fname, encoding="UTF-8")

    @staticmethod
    def is_numeric(inp: str):
        try:
            float(inp)
            return True
        except:
            return False

    @classmethod
    def _parse_any(cls, inp):
        if isinstance(inp, Section):
            return dict((k, cls._parse_any(v)) for k, v in {**inp}.items())

        if isinstance(inp, str):
            if "," in inp:
                return [cls._parse_any(x.strip()) for x in inp.split(",")]

            if cls.is_numeric(inp):
                return cls._parse_any(float(inp))

            return inp

        if isinstance(inp, float):
            return int(inp) if inp // 1 == inp else inp

        return inp

    def save(self):
        if self.__dict__ != self._proxy:
            parser = ConfigParser()
            parser.read_dict(self._proxy)
            self.parser = parser
            self.parser.write(open(self.fname, "w", encoding="UTF-8"))
