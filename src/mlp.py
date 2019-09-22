from sklearn.neural_network import multilayer_perceptron as mlp


def main():
    dataBase = "dataset/bd/bd.txt"

    bd = open(dataBase, 'r')

    for linha in bd:
        print(linha)
    bd.close()


if __name__ == "__main__":
    main()