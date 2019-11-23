from sklearn.neural_network import multilayer_perceptron as mlp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import pandas as pd
import time
import util.hashmap as hashMap


def readfile(row):
    '''
    Faz a leitura de um arquivo e retorna o acorde e as features

    Retorno:
    -chord
    -features
    '''

    line = row.split(',')
    chord = row.split(',')[12]
    
    i=0
    feature = ""
    while(i<12):
        feature = feature + line[i]+", "
        i = i +1

    return chord, feature


def normalizesDatabase(dataBase, newDataBase, samples):
    '''
    Balanceao do banco de dados com a quantidade do munero de samples
    '''

    bd = open(dataBase, 'r')
    nbd = open(newDataBase, 'w')

    hm = hashMap.HashMap()

    for row in bd:
        chord, feature = readfile(row)

        if(not hm.get(chord)):          #Verifica se ja existe o acorde chord
                hm.put(chord, 1)            #Cria uma nova chave
        else:
            k = hm.get(chord)
            if(samples > k):
                l = "" + feature + chord
                nbd.write(l)
                k = k + 1
                hm.put(chord, k)            #atualiza a hash


    bd.close()
    nbd.close()


def main():
    dataBase = "dataset/bd/bd_CLP.csv"
    newDataBase = "dataset/bd/bd_CLP1.csv"
    outPut = "mlp_CLP.txt"
    arq = open(outPut, 'w')
    samples = 3500



    normalizesDatabase(dataBase, newDataBase, samples)

    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "chords"]

    bd = pd.read_csv(newDataBase, names=name)
    # print(bd.head())

    X = bd.drop("chords", axis = 1)
    y = bd["chords"]

    inicio = time.time()
    i = 0
    duracao = 0 

    while(i < 3):
        arq.write("Interacao: " +str(i) + "\n")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

        #normaliza os dados
        scaler = StandardScaler()
        scaler.fit(X_train)
        StandardScaler(copy=True, with_mean=True, with_std=True)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        
        #cria um modelo de treinamento
        #mlp = MLPClassifier(hidden_layer_sizes=(13,40,13),max_iter=10000)
        mlp = MLPClassifier(hidden_layer_sizes=(61),max_iter=1000)
        #colocar os novos casos de testes aqui a baixo
        # mlp = MLPClassifier(hidden_layer_sizes=(120, 120, 180,120, 60),max_iter=1000000)

        print("Iteracao: " + str(i+1) + " de 30")
        #Treina a rede com os dados
        mlp.fit(X_train,y_train)

        predictions = mlp.predict(X_test)
        #print(predictions)
        
        fim = time.time()
        duracao = fim - inicio
        
        
        #print(confusion_matrix(y_test,predictions))
        # print(classification_report(y_test,predictions))

        #arq.write(str(confusion_matrix(y_test,predictions)) + "\n")
        arq.write(str(classification_report(y_test,predictions))+ "\n")
        i = i + 1
    print("Fim do treinamento..., Duracao: " + str(duracao)+"\n")
    #print("Terminou a execucao!!!")

if __name__ == "__main__":
    main()