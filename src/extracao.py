from pydub import AudioSegment
import glob, os
import util.hashmap

#https://gist.github.com/gchavez2/53148cdf7490ad62699385791816b1ea
#https://ieeexplore.ieee.org/document/4564924   (artigo interessante)
#https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/    (site legal sobre stft)
#https://musicinformationretrieval.com/stft.html

def musicAccount(src):
    """Retorna a quantiade de musicas no formato mp3 dentro de um diretorio.
    """
    os.chdir(src)           #muda o diretorio para src
    number = 0
    for file in glob.glob("*.mp3"):
        number = number + 1

    return number


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


def main():
    """Funcao para gerar trechos de mp3"""
    """
    src = "dataset/mp3/"
    dst = "dataset/wav/"

    startMin = 0
    startSec = 50

    endMin = 1
    endSec = 20

    # Time to miliseconds
    startTime = startMin*60*1000+startSec*1000
    endTime = endMin*60*1000+endSec*1000

    # Opening file and extracting segment
    song = AudioSegment.from_mp3( src+'0'+'.mp3' )
    extract = song[startTime:endTime]
    
    # Saving
    extract.export( '0'+'_extract.mp3', format="mp3")
    """

    src = "dataset/mp3/"
    chordsFile = "dataset/chords/"
    dst = "dataset/extract_wav/"
    mp3 = ".mp3"

    actualDirectory = os.getcwd()        #Salva o diretorio atual

    #number = musicAccount(src)

    os.chdir(actualDirectory)       #retorna para o diretorio inicial

    i = 0
    number = 1
    while(i < number):
        name = str(i)

        sound = AudioSegment.from_mp3(src+name+mp3)
        chords = open(chordsFile + name+ '.lab')
        
        j=0
        for row in chords:
            start, end, chord = readfile(row)
            
            startTime, endTime = timeToMiliSeconds(float(start), float(end))

            #abre a musica e corta um trecho e salva em wav com o nome da nota
            fragment = sound[startTime:endTime]
            fragment.export(dst + str(j) + "_" +chord[0] +".wav", format="wav")
            j=j+1
            #print(fragment)



        chords.close
        i = i + 1





if __name__ == "__main__":
    main()