

class AClass(object):
    def __init__(self, string):
        self.param_1 = 'param 1'
        self.param_2 = 'param 2'
        self.string = string

    def do(self):
        print self.param_1, self.param_2, self.string


class BClass(AClass):
    def __init__(self):
        AClass.__init__(self, 'cool')
        self.param_2 = ' moded two '

    def do(self):
        print 'going on moded do'
        print self.param_1
        print self.param_2
        print self.string


def main():
    a = AClass('w')
    b = BClass()

    a.do()
    b.do()


if __name__ == '__main__':
    main()
