%converte todos arquivo wav em chroma Livisghton
clear;
close all hidden;

%diretorio dos arquivos .wav
dirWav = 'database/wav/';
fileWav = '*.wav';
appendFullPath = 0;

%Carrega todos os arquivos que tem os arcordes
dirFileNames = getAllFiles(dirWav, fileWav, appendFullPath);


for n=1:size(dirFileNames,1)
    clear parameter;
    parameter.message = 1;
    
    %Faz a leitura dos arquivo wav
    [f_audio,sideinfo] = wav_to_audio('', dirWav, dirFileNames{n});
        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Estimation of the global tuning of the recording and selection of
    % an appropriate filterbank for use in the next step
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    clear parameter
    shiftFB = estimateTuning(f_audio);
    fprintf('Using filterbank number: %d\n',shiftFB);

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Compute pitch features
    % 
    % Input: audio file of format: mono, 22050 Hz
    %
    % Output: sequence of pitch vectors 
    %         (specified by N x 120 matrix f_pitch)
    %         Only subband for MIDI pitches 21 to 108 are computed, the
    %         other subbands are set to zero.
    %
    % Parameter: parameter.win_len specifies window length (in samples)
    %            with window overlap of half size  
    %            Example: audio sampling rate: 22050 Hz
    %                     parameter.win_len = 4410
    %                     Resulting feature rate: 10 Hz
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    clear parameter
    parameter.winLenSTMSP = 4410;
    parameter.fs = sideinfo.wav.fs;
    parameter.save = 1;
    parameter.saveDir = 'database/dataFeature/';
    parameter.saveFilename = dirFileNames{n}(1:end-4);
    parameter.shiftFB = shiftFB;
    parameter.saveAsTuned = 1;
    [f_pitch,sideinfo] = audio_to_pitch_via_FB(f_audio,parameter,sideinfo);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Visualization of pitch decomposition (f_pitch)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    parameter.usePitchNameLabels = 1;
    parameter.title = 'Logarithmic compression of amplitude';
    parameter.featureRate = sideinfo.pitch.featureRate;
    parameter.xlabel = 'Time [Seconds]';
    parameter.ylabel = 'Pitch';
    visualizePitch(log(5*f_pitch+1),parameter);
end