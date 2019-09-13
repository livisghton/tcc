from pydub import AudioSegment
import glob, os
import util.hashmap as hashMap
import numpy as np


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


def wavGenerete(mp3Files, wavFiles, chordsFiles):
    """
    Faz a segmentacao dos arquivos de audio com base nos arquivos de acordes.\n
    \t-mp3Files: diretorio com os arquivos no formato .mp3;\n
    \t-wavFiles: destivo onde ira ser salvo os arquivos segmentados no formato .wav;\n
    \t-chordsFiles: Arquivo onde esta os mapeamento dos acordes.
    """

    actualDirectory = os.getcwd()        #Salva a posicao do diretorio atual
    names = fileNames(mp3Files)      #pega todas as musicas do diretorio
    os.chdir(actualDirectory)       #retorna para o diretorio inicial

    hm = hashMap.HashMap()

    i = 0
    while(i < len(names)):
        name = names[i].split('.')[0]
        
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

            #abre a musica e corta um trecho e salva em wav com o nome da nota
            fragment = sound[startTime:endTime]
            fragment.export(wavFiles + chord[0] +  "_in" + str(hm.get(chord)) +".wav", format="wav")

        chords.close
        i = i + 1



def main():
    """Funcao para gerar trechos de mp3 e espectros stft"""

    #variaveis referente ao diretorio
    mp3Files = "dataset/mp3/"
    chordsFiles = "dataset/chords/"
    wavFiles = "dataset/segmented_audio/"

    #variaveis de entrada
    windows = 'blackman'
    lengthWindows = 500        #tamanho da janela em seg
    hopWindows = 100         #salto da janela em seg
    

    #fase de segmentacao
    wavGenerete(mp3Files, wavFiles, chordsFiles)

    #converter para o dominio da frequencia e  generacao dos chromas




if __name__ == "__main__":
    main()