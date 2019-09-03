from prozor import Prozor

def main():

    prozor = Prozor()
    prozor.root.mainloop()
    print(prozor.get_p())

    # abc = [1,2,3,4,5,6]
    #
    # for i in range(len(abc)):
    #     abc[i] = chr(abc[i]+64)
    #
    # print(abc)

if __name__ == '__main__':
    main()
