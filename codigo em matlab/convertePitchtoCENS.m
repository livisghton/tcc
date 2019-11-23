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

%diretorio de saida .txt
dirOut = 'database/dataset/bd_CENS.csv';
dirOutFilter = 'database/dataset/bdFilter_CENS.csv';
bd = fopen(dirOut, 'w' );
bdFilter = fopen(dirOutFilter, 'w' );

%Carrega todos os arquivos que tem as features
%dirFileNames = getAllFiles(dirWav, fileWav, appendFullPath);

%name = strcat('',dirFileNames(1:end-4));

%carrega todos os arquivos .lab
dirFileNames = getAllFiles(dirLab, fileLab, appendFullPath);

%filtra a quantidade de acordes
filePath = 'database\dataset\count_chords.txt';
numberCut = 20;
filterchords = getChordsList(filePath, numberCut);

for n=1:size(dirFileNames,1)
    n
    %gera o nomes dos arquivos
    name = strcat('',dirFileNames{n}(1:end-4));
    
    %Gera o path para carregar as features
    nameFeature = strcat(strcat(dirFeature, name),strcat('_pitch_4410',fileFeature(2:end)));
    load(nameFeature)
    
    %abrir aquivos lab
    nameMusic = strcat(strcat(dirLab, name), fileLab(2:end));
    [tempoInicio, tempoFim, chords] = textread(nameMusic,'%f %f %s');
    
    %paremetros apara ajustar o choma CENS
    parameter.winLenSmooth = 10;
    parameter.downsampSmooth = 1;
    parameter.featureRate = sideinfo.pitch.featureRate;
    [f_CENS,sideinfo] = pitch_to_CENS(f_pitch,parameter,sideinfo);
    
    %visualizacao do CENS
    parameter.featureRate = sideinfo.CENS.featureRate;
    parameter.xlabel = 'Time [Seconds]';
    parameter.title = sprintf('CENS %d %d chromagram',parameter.winLenSmooth,parameter.downsampSmooth);
    %if(n==1)
     %   visualizeChroma(f_CENS,parameter);
    %end
    t = 0.0;     %reponsavel por contar o tempo na matriz do chroma
    k = 1;       %index da matriz do chroma
    for i = 1 : length(tempoFim)
        for j = k : length(f_CENS)
            if( round(tempoInicio(i), 1) <= t && round(tempoFim(i), 1) > t && (findChords(filterchords,chords(i))==1) )

                chord = f_CENS(1:end, k).';
                
                exemplo = '';
                for x = 1 : length(chord)
                    exemplo = strcat(exemplo, strcat(num2str(chord(x)), ','));
                end
                exemplo = strcat(exemplo, chords(i));
                fprintf(bd, '%s\n', exemplo{:});
                
            elseif (round(tempoInicio(i), 1) <= t && round(tempoFim(i), 1) > t && findChords(filterchords,chords(i))==0)
                %armazenar as notas que
                chordFilter = f_CENS(1:end, k).';
                
                exemploFilter = '';
                for x = 1 : length(chordFilter)
                    exemploFilter = strcat(exemploFilter, strcat(num2str(chordFilter(x)), ','));
                end
                exemploFilter = strcat(exemploFilter, chords(i));
                fprintf(bdFilter, '%s\n', exemploFilter{:});
            else 
                break;
            end
            t = t + 0.1;
            k = k+1;
        end
        
    end
end
fclose(bd);
fclose(bdFilter);
fim = 'terminou!!!'
