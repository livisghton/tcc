from pydub import AudioSegment
import glob, os
import util.hashmap as hashMap
import numpy as np
#from scipy import signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import scipy.signal as stft


#https://gist.github.com/gchavez2/53148cdf7490ad62699385791816b1ea
#https://ieeexplore.ieee.org/document/4564924   (artigo interessante)
#https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/    (site legal sobre stft)
#https://musicinformationretrieval.com/stft.html

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


def wavGenerete(mp3Files, wavFiles, chordsFiles):
    """
    Faz a segmentacao dos arquivos de audio com base nos arquivos de acordes.\n
    \t-mp3Files: diretorio com os arquivos no formato .mp3;\n
    \t-wavFiles: destivo onde ira ser salvo os arquivos segmentados no formato .wav;\n
    \t-chordsFiles: Arquivo onde esta os mapeamento dos acordes.
    """

    actualDirectory = os.getcwd()        #Salva a posicao do diretorio atual
    number = fileAccount(mp3Files, ".mp3")      #contabiliza a quantidade de arquivos mp3 na pasta mp3Files
    os.chdir(actualDirectory)       #retorna para o diretorio inicial

    hm = hashMap.HashMap()

    i = 0
    #number = 1
    while(i < number):
        name = str(i)

        sound = AudioSegment.from_mp3(mp3Files+name+'.mp3')
        #sound.set_channels(1)                                   #TODO:Verifica se funciona, converter para mono 
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

            #abre a musica e corta um trecho e salva em wav com o nome da nota
            fragment = sound[startTime:endTime]
            fragment.export(wavFiles + chord[0] +  "_in" + str(hm.get(chord)) +".wav", format="wav")

        chords.close
        i = i + 1


def spectrumGeneration(wavFiles, windows, lengthWindows, jumpWindows):
    """
    Gera o espectro de todos os arquivos no diretorio com a configuracao passada.
    \t-wavFiles: diretorio com os arquivos no formato .wav;
    \t-windows: tipo de janela
    \t-lengthWindows: tamanho da janela em milessegundos
    \t-jumpWindows: salto da janela em milessegundos
    """
    actualDirectory = os.getcwd()        #Salva a posicao do diretorio atual
    names = fileNames(wavFiles)      #contabiliza a quantidade de arquivos wav na pasta extract_wav
    os.chdir(actualDirectory)       #retorna para o diretorio inicial


    i = 0
    while(i < len(names)):
        #name = names[i].split("_")
        samplerate, samples = wav.read(wavFiles + names[i])
        if(i == 5):
           #print(samples)
            #f, t, Zxx = stft.stft(samples[0], samplerate, windows)
            f, t, Zxx = stft.stft(samples[0])
            print(Zxx)
            #plt.imshow(float(Zxx))
            #plt.ylabel('Frequency [Hz]')
            #plt.xlabel('Time [sec]')
            #plt.show()
        
        i = i + 1

"""
def spectrumAnalyzer(fs, data):
    frequencies, times, spectrogram = signal.spectrogram(data, fs)
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    #plt.show()
    plt.savefig('spectrumCar1.png', format='png')"""


def main():
    """Funcao para gerar trechos de mp3"""

    #variaveis referente ao diretorio
    mp3Files = "dataset/mp3/"
    chordsFiles = "dataset/chords/"
    wavFiles = "dataset/extract_wav/"

    #variaveis de entrada
    windows = np.blackman(256)
    lengthWindows = 1000        #tamanho da janela em milessegundos
    jumpWindows = 200         #salto da janela em milessegundos


    wavGenerete(mp3Files, wavFiles, chordsFiles)

    spectrumGeneration(wavFiles, windows, lengthWindows, jumpWindows)
    
    
    """
    hm = hashMap.HashMap()
    hm.put("C7_5", 1)
    print(hm.get("C7_5"))
    print(hm.get("D"))"""





if __name__ == "__main__":
    main()