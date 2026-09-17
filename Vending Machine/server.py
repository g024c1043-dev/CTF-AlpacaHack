import os

FLAG = os.getenv("FLAG", "Alpaca{dummy}")

class VendingMachine:
    def __init__(self):
        self.stock = 'a'*30 + 'b'*60 + 'c'*20 + 'd'*50 + 'e'*40 + 'f' # 'aaa...eeef'
        self.item_names = {
            'a': 'apple juice',
            'b': 'banana juice',
            'c': 'coke',
            'd': 'draft beer',
            'e': 'energy drink',
            'f': 'flag'
        }

    def print_menu(self):
        print("Please select an item.")
        print("-" * 16)
        for mark, name in self.item_names.items():
            print(f"{mark}: {name}")
        print("x: exit")
        print("-" * 16)

    def buy(self, mark:str):
        # check choice
        if mark not in ['a', 'b', 'c', 'd', 'e']: # No 'f'? Hmm...
            print("Invalid choice.")
            return
        # check stock
        if len(self.stock) <= 0:
            print("All sold out.")
            return
        # find the location of the product
        loc = self.stock.find(mark)
        # take the product from stock
        stock_list = list(self.stock)
        item = stock_list.pop(loc)
        self.stock = ''.join(stock_list)
        # dispense the product
        name = self.item_names[item]
        print(f"You bought {name}.")
        if item == 'f':
            print(f"Flag:", FLAG)
        else:
            print("Thank you!")

def main():
    vm = VendingMachine()
    vm.print_menu()
    while True:
        mark = input("your choice> ").lower()
        if mark == "x":
            print("Bye.")
            break
        vm.buy(mark)

if __name__ == '__main__':
    main()
