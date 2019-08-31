
class Stft:

    def __init__(self, signal, samplingRate, window, hop, nttt):
        """
        construtor de stft:
        signal - signal in the time domain
        win - tipo de janela
        hop - tamanho do salto
        nfft - numeros de pontos de nfft
        samplingRate - taxa de amostragem
        """
        self.signal = signal
        self.samplingRate = samplingRate
        self.window = window
        self.hop = hop
        self.nttt = nttt

    
    def calculateStft():

        #calcula o tamanho do sinal
        sigLen = len(self.signal)

        #Calcula o tamanho da janela
        winLen = len(self.window)





