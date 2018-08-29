
GLOBAL_RET_CODE = 0

class Name:
    def __init__(self, name):
        self.myname = name

    def printaname(self):
        print "Name", self.myname, GLOBAL_RET_CODE

    def main(self):
        self.printaname()

class Person(Name):

    def __init__(self, name, phone):
        Name.__init__(self, name)
        self.myphone = phone
        
    def printaperson(self):
        GLOBAL_RET_CODE = 127
        print "Name", self.myname, "Phone", self.myphone, GLOBAL_RET_CODE

if __name__ == "__main__":
    obj = Person("John", "2598-6313")
    obj.printaname()
    obj.printaperson()

