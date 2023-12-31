from macros import Products, ServingSize

def main():
    foods = [Products("Meat", 100, ServingSize("g", 25), 10, 20, 70), Products("Bread", 50, ServingSize("g", 20), 5, 40, 5)]
    data = foods[0].get_food()
    data = foods[1].get_food(data)
    print(data)

if __name__ == "__main__":
    main()