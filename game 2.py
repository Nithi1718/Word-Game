#Game using python looping statement
a=1
b=input("May i know the name of the brave player? ")
print("Welcome "+b)
while a>=1:
    print(""" Press the below things to play the game
    1.start
    2.end""")
    b=int(input("Enter to begin or exit: "))
    if b==1:
        print("""Follow the instructions to start
        1.move forward
        2.move backward
        3.move right
        4.move left
        5.exit""")
        n=1
        while n>=1:
            c = int(input("Enter the index number: "))
            if c==1:
                life=100
                play_time=10
                print(f"life={life},play time={play_time}")
            elif c==2:
                life=50
                play_time=20
                print(f"life={life},play time={play_time}")
            elif c==3:
                life=75
                play_time=15
                print(f"life={life},play time={play_time}")
            elif c==4:
                life=90
                play_time=25
                print(f"life={life},play time={play_time}")
            elif c==5:
                print()
                print("Nice match")
                exit()
            else:
                print()
                print("Invalid input")
                print("start again")
                print()

                break
        n+=1
    elif b==2:
        print()
        print("Well played, better luck next time")
        exit()
    else:
        print()
        print("invalid entry, try again")
        print()
    a+=1