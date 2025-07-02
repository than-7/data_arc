def add(x,y):
    return x+y
def subtract(x,y):
    return x-y
def multiple(x,y):
    return x*y
def divide(x,y):
    if y == 0:
        return "Error--! Division by zero"
    return x/y
def calculator():
    print("Simple  CLI Calculator")
    print("Operations")
    print("1.ADD (+)")
    print("2.SUBTRACT (-)")
    print("3.MULTIPLE (*)")
    print("4.DIVIDE (/)")
    print("5.Quit")

    while True:
        choice = input("\nChoose operation (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting calculator. Goodbye")
            break

        if choice in ['1','2','3','4']:
            try:
                num1 = float(input("Enter 1 num:"))
                num2 = float(input("Enter 2 Num:"))
            except ValueError:
                print("invalid input please enter numbers")
                continue
        if choice == '1':
            result = add(num1,num2)
            operator = '+'
        elif choice =='2':
            result=subtract(num1,num2)
            operator = '-'
        elif choice == '3':
            result = multiple(num1,num2)
            operator = '*'
        elif choice =='4':
            result = divide(num1,num2)
            operator='/'

        print(f"{num1}{operator} {num2}={result}")
    else:
        print("Inavalid choice")

if __name__== "__main__":
    calculator()
    