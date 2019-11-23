from pydub import AudioSegment
import glob, os


def fileNames(directory):
    """
    Retorna lista com os nomes dos arquivos no diretorio
    """
    os.chdir(directory)           #muda o diretorio para directory
    names = []
    names = os.listdir()
    return names



def mp3ToWav(mp3Files, wavFiles):
    """
    Converte todos os arquivo mp3 dentro de um diretorio para wav
    \t-mp3Files: diretorio com os arquivos no formato .mp3;\n
    \t-wavFiles: destivo onde ira ser salvo os arquivos segmentados no formato .wav;\n
    """

    actualDirectory = os.getcwd()        #Salva a posicao do diretorio atual
    names = fileNames(mp3Files)
    os.chdir(actualDirectory)       #retorna para o diretorio inicial

    i = 0
    while(i < len(names)):
        name = names[i].split(".")[0]
        if i == 0:
            print(mp3Files + name + '.mp3')
            #sound = AudioSegment.from_mp3(mp3Files + name+'.mp3')
            #sound.export(name+".wav", format="wav")

        i = i+1



def main():
    """Funcao para gerar trechos de mp3 e espectros stft"""

    #variaveis referente ao diretorio
    mp3Files = "database/mp3/"
    wavFiles = "database/wav/"

    mp3ToWav(mp3Files, wavFiles)



if __name__ == "__main__":
    main()