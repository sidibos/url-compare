import cowsay

def main():
    animal = input("name of the animal: ")
    word   = input("says: ")

    char_names = ['beavis', 'cheese', 'daemon', 'cow', 'dragon', 'ghostbusters', 'kitty', 'meow', 'milk', 'pig', 'stegosaurus', 'stimpy', 'trex', 'turkey', 'turtle', 'tux']

    if animal in char_names:
        print(cowsay.get_output_string(animal, animal.capitalize() + ' says: ' + word))
    else:
        cowsay.cow(word)



if __name__ == "__main__":
    main()