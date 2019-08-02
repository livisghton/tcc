from pydub import AudioSegment
import glob, os

def musicAccount(src):
    """Retorna a quantiade de musicas no formato mp3 dentro de um diretorio
    """
    os.chdir(src)           #muda o diretorio para src
    number = 0
    for file in glob.glob("*.mp3"):
        number = number + 1

    return number


def main():
    """Função principal do projeto
    """
    src = "dataset/mp3/"
    dst = "dataset/wav/"
    mp3 = ".mp3"

    actualDirectory = os.getcwd()        #Salva o diretorio atual

    number = musicAccount(src)

    os.chdir(actualDirectory)       #retorna para o diretorio inicial

    i = 0
    while(i < number):
        name = str(i)
        sound = AudioSegment.from_mp3(src+name+mp3)
        sound.export(dst + name +".wav", format="wav")
        i = i+1

if __name__ == "__main__":
    main()