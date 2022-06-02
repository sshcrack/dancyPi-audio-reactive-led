from bruh.testclass import TestChildClass


class TestHaha:
    def __init__(self, lol):
        self.modes = {"testclass": TestChildClass()}
        self.lol = lol

    def run(self):
        print(f"{self.lol}: {self.modes}")


class Lil(TestHaha):
    def __init__(self, lol):
        super().__init__(lol)


e = Lil("1")
e.run()
x = Lil("2")
x.run()
e.run()
x.run()
