%converte os pitch em chroma CENS
clear;
close all hidden;

%diretorio dos arquivos .wav
dirFeature = 'database/dataFeature/';
fileFeature = '*.mat';
appendFullPath = 0;

%diretorio dos arquivos .lab
dirLab = 'database/lab/';
fileLab = '*.lab';

secondName = '_4410';
%Carrega todos os arquivos que tem as features
%dirFileNames = getAllFiles(dirWav, fileWav, appendFullPath);

%name = strcat('',dirFileNames(1:end-4));

%carrega todos os arquivos .lab
dirFileNames = getAllFiles(dirLab, fileLab, appendFullPath);


for n=1:size(dirFileNames,1)
    
    %gera o nomes dos arquivos
    name = strcat('',dirFileNames{n}(1:end-4));
    
    
    %Gera o path para carregar as features
    nameFeature = strcat(strcat(dirFeature, name),strcat('_pitch_4410',fileFeature(2:end)));
    nameFeature
    load(nameFeature)
    
    
    %abrir aquivos lab
    nameMusic = strcat(strcat(dirLab, name), fileLab(2:end));
    [tempoInicio, tempoFim, nota] = textread(nameMusic,'%f %f %s');
    
    
    %paremetros apara ajustar o choma CENS
    parameter.winLenSmooth = 10;
    parameter.downsampSmooth = 1;
    parameter.featureRate = sideinfo.pitch.featureRate;
    [f_CENS,sideinfo] = pitch_to_CENS(f_pitch,parameter,sideinfo);
    
    %visualizacao do CENS
    parameter.featureRate = sideinfo.CENS.featureRate;
    parameter.xlabel = 'Time [Seconds]';
    parameter.title = sprintf('CENS %d %d chromagram',parameter.winLenSmooth,parameter.downsampSmooth);
    %visualizeChroma(f_CENS,parameter);
    
    
    t = 0.0
    k = 1
    for i = 1 : size(tempoFim, 1)
        for j = k : size(f_CENS, 1)

            if(round(tempoFim(i), 2) > tround(tempoFim(i), 2) > t)
                nota(k)
                t = t + 0.1
                k = k+1
                %Salvar em um arquivo .csv
                %criar um hashMap par evitar notas muito pequena
            end
        end
        
    end
end