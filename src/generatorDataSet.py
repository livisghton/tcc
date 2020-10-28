from pydub import AudioSegment
import glob, os
import util.hashmap as hashMap
import numpy as np
from librosa.feature import chroma_stft
import librosa.display as display
import librosa
import scipy.io.wavfile as wav
from scipy import signal
import matplotlib.pyplot as plt
import time



#https://gist.github.com/gchavez2/53148cdf7490ad62699385791816b1ea
#https://ieeexplore.ieee.org/document/4564924   (artigo interessante)
#https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/    (site legal sobre stft)
#https://musicinformationretrieval.com/stft.html
#https://www.mathworks.com/matlabcentral/fileexchange/45197-short-time-fourier-transform-stft-with-matlab   em matlab


def fileAccount(directory, format):
    """Contabiliza a quantiade de musicas no formato mp3 dentro de um diretorio.
    """
    os.chdir(directory)           #muda o diretorio para directory
    number = 0
    for file in glob.glob("*"+format):
        number = number + 1

    return number


def fileNames(directory):
    """
    Retorna lista com os nomes dos arquivos no diretorio
    """
    os.chdir(directory)           #muda o diretorio para directory
    names = []
    names = os.listdir()
    return names



def readfile(row):
    """
    Retorna a duracao da nota e a nota para esta linha.
    """
    line = row.split()
    start = line[0]
    end = line[1]
    chord = line[2]
    return start, end, chord


def timeToMiliSeconds(start, end):
    """
    Retorna o tempo de inicio e fim em milissegundos.
    """
    startTime = start*1000
    endTime = end*1000
    return int(startTime), int(endTime)


def mapChords(countChordsFile):
    """
    Recebe um arquivo onde contem a contagem de acordes e a quantidade e retorna um map com esses dois valores
    Entrada:
    -countChordsFile: diretorio com o arquivo txt

    Saída:
    -hm: um map de acorde com um inteiro
    """

    arq = open(countChordsFile, 'r')
    hm = hashMap.HashMap()

    for row in arq:
        count = int(row.split(' ')[0])
        chord = row.split(' ')[1].split('\n')[0].replace('/', '|')
        
        hm.put(chord, count)

    return hm
     

def normalizeChordNames(name):
    """
    converte as notas em Bemois notas em sustenidos ou naturais
    """

    newName = ""

    if(name.find('Cb') >= 0):
        newName = 'B' + name.split('b')[1]
    elif(name.find('Db') >= 0):
        newName = 'C#' + name.split('b')[1]
    elif(name.find('Eb') >= 0):
        newName = 'D#' + name.split('b')[1]
    elif(name.find('Fb') >= 0):
        newName = 'E' + name.split('b')[1]
    elif(name.find('Gb') >= 0):
        newName = 'F#' + name.split('b')[1]
    elif(name.find('Ab') >= 0):
        newName = 'G#' + name.split('b')[1]
    elif(name.find('Bb') >= 0):
        newName = 'A#' + name.split('b')[1]
    else:
        newName = name
    
    return newName


def wavGenerete(mp3Files, segmented_audio, chordsFiles, mapChords, limit = 0):
    """
    Faz a segmentacao dos arquivos de audio com base nos arquivos de acordes.\n
    \t-mp3Files: diretorio com os arquivos no formato .mp3;\n
    \t-segmented_audio: destivo onde ira ser salvo os arquivos segmentados no formato .wav;\n
    \t-chordsFiles: Arquivo onde esta os mapeamento dos acordes.
    """
    segmented_audio2 = "dataset/segmented_audio2/"

    actualDirectory = os.getcwd()        #Salva a posicao do diretorio atual
    names = fileNames(mp3Files)      #pega todas as musicas do diretorio
    os.chdir(actualDirectory)       #retorna para o diretorio inicial

    t = 1/44100                     #tempo de amostragem de um cd

    hm = hashMap.HashMap()

    i = 0
    while(i < len(names)):
        name = names[i].split('.mp')[0]

        name = normalizeChordNames(name)            #converte notas
        
        sound = AudioSegment.from_mp3(mp3Files+name+'.mp3')
        
        chords = open(chordsFiles + name+ '.lab')
        
        for row in chords:

            start, end, chord = readfile(row)

            if(not hm.get(chord)):          #Verifica se ja existe o acorde chord
                hm.put(chord, 1)            #Cria uma nova chave
            else:
                k = hm.get(chord)
                k = k + 1
                hm.put(chord, k)            #atualiza a hash

            startTime, endTime = timeToMiliSeconds(float(start), float(end))

            if(t < (endTime - startTime)):      #necessario para nao gerar segmentos menor do que o tempo de amostragem

                #abre a musica e corta um trecho e salva em wav com o nome da nota
                fragment = sound[startTime:endTime]
                # fragment.export(segmented_audio + chord +  "_in" + str(hm.get(chord)) +".wav", format="wav")

                chord = chord.replace('/', '|')

                if(mapChords.get(chord) and mapChords.get(chord) >= limit ):
                    # salva em segmento 1
                    fragment.export(segmented_audio + chord +  "_in" + str(hm.get(chord)) +".wav", format="wav")
                else:
                    # salva em sagmento 2
                    fragment.export(segmented_audio2 + chord +  "_in" + str(hm.get(chord)) +".wav", format="wav")

        chords.close
        i = i + 1

def printChroma(chroma):
    """
    Imprime o grafico do groma
    """
    plt.figure(figsize=(10, 4))
    display.specshow(chroma, y_axis='chroma', x_axis='time')
    plt.colorbar()
    plt.title('Chromagram')
    plt.tight_layout()
    plt.show()


def chromaGeneration(segmented_audio, arq, windows='hann', lengthWindows=2048, hopWindows=512, lengthWindowsFeature=44):
    """
    Converte para o dominio da frequencia com STFT e gera a base de dabaBase
    \t-segmented_audio: caminho dos arquivos de audio wav;
    \t-arq: Caminho onde sera gerado o banco de dados;
    \t-windows: tipo de janela Ex: 'blackman', 'hamming', por padao sera hann;
    \t-lengthWindows: tamanho da janela Inteiro. Padrao eh 2048 pontos
    \t-hopWindows: tamanho do salto das janelas. Padrao eh 512 pontos
    \t-lengthWindowsFeature: tamanho da janela para extrair o vetor do chroma. Padrao eh 44 pontos
    """

    actualDirectory = os.getcwd()        #Salva a posicao do diretorio atual
    names = fileNames(segmented_audio)      #pega todos as musicas do diretorio
    os.chdir(actualDirectory)       #retorna para o diretorio inicial

    hm = hashMap.HashMap()

    # arq.write('C, C#, D, D#, E, F, F#, G, G#, A, A#, B, chords\n')    #cabecario do banco de dados

    i = 0
    while(i < len(names)):
        name = names[i].split('.')[0]

        # samplerate, samples = wav.read(segmented_audio + names[i] )     #samplerate tempo de amostragem para 1 seg
        audio, samplerate = librosa.load(segmented_audio + names[i], 44100)
        
        # if(i==0):
        #print(name)
        chroma = chroma_stft(audio, samplerate, None, np.inf, lengthWindows, hopWindows, None, windows)
        # chroma = chroma_stft(audio, samplerate)
        #print(chroma)
        #printChroma(chroma)
        winStart = 0
        winEnd = lengthWindowsFeature        #janela de deslocamento no chroma
        while(winEnd < len(chroma[0])):

            k = 0
            while(k < len(chroma)):
                    mean = np.mean(chroma[k][winStart:winEnd])     #calcula a media do trecho da porcao da lista
                    arq.write(str(round(mean,3)))
                    k = k + 1

                    arq.write(str(', '))

            arq.write(str(name.split('_')[0]))
            arq.write('\n')

            winStart = winEnd
            winEnd = winEnd + lengthWindowsFeature           #atualiza o deslocamento do chroma
        
        if(i==0):
            print(chroma)
            print(len(chroma[1]))
            printChroma(chroma)
            
        i = i + 1


def main():
    """Funcao para gerar trechos de mp3 e espectros stft"""

    #variaveis referente ao diretorio
    mp3Files = "dataset/mp3/"
    chordsFiles = "dataset/chords/"
    segmented_audio = "dataset/segmented_audio/"
    dataBase = "dataset/bd/bd.csv"
    countChords = "dataset/count_chords.txt"

    #variaveis de entrada da STFT
    windows = 'blackman'
    lengthWindows = 500        #tamanho da janela em seg
    hopWindows = 100         #salto da janela em seg
    
    #variaveis de configuracao do chroma
    lengthWindowsFeature = 11

    #variavel para dividir o banco de dados em dois, ou seja, esta variavel e reponsavel para
    #limitar o valor minimo de ocorrencia de um acorde
    limit = 400

    inicio = time.time()

    #carrega a lista de todos acordes
    hm = mapChords(countChords)
    fim = time.time()
    duracao = fim - inicio
    print("Carregamento do Map concluido..., Duracao:  " + str(duracao))

    #fase de segmentacao
    # wavGenerete(mp3Files, segmented_audio, chordsFiles, hm, limit)
    # fim = time.time()
    # duracao = fim - inicio
    # print("Fase de segmentacao concluida..., Duracao: " + str(duracao))

    arq = open(dataBase, 'w')
    #converter para o dominio da frequencia e  generacao dos chromas
    chromaGeneration(segmented_audio, arq, windows, lengthWindows, hopWindows, lengthWindowsFeature)
    fim = time.time()
    duracao = fim - inicio
    print("Geracao do banco de dados finalizado..., Duracao: " + str(duracao))

    arq.close()




if __name__ == "__main__":
    main()