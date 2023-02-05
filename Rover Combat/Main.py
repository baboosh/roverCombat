import Workshop as Workshop


class Main:

    def __init__(self):
        self.workshop = Workshop.Workshop()
        


    def GameLoop(self):
        while True:
            self.workshop()



if __name__ == "__main__":
    newWorkshop = Workshop()

    newWorkshop.main()
