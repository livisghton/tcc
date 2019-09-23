from sklearn.neural_network import multilayer_perceptron as mlp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import pandas as pd
import time

def main():
    dataBase = "dataset/bd/bd.csv"
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "chords"]

    bd = pd.read_csv(dataBase, names=name)
    # print(bd.head())

    X = bd.drop("chords", axis = 1)
    y = bd["chords"]

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    #normaliza os dados
    scaler = StandardScaler()
    scaler.fit(X_train)
    StandardScaler(copy=True, with_mean=True, with_std=True)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    inicio = time.time()
    #cria um modelo de treinamento
    mlp = MLPClassifier(hidden_layer_sizes=(13,40,13),max_iter=500)

    #Treina a rede com os dados
    mlp.fit(X_train,y_train)

    predictions = mlp.predict(X_test)
    
    fim = time.time()
    duracao = fim - inicio
    print("Fim do treinamento..., Duracao: " + str(duracao)+"\n")

    print(confusion_matrix(y_test,predictions))
    print(classification_report(y_test,predictions))

if __name__ == "__main__":
    main()