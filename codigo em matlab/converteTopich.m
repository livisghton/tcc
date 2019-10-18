%"""Converter uma lista de musica em wav para pitch

%diretorio dos arquivos .wav
dirWav = 'database/wav';
fileWav = '*.wav';
appendFullPath = 0;

%Carrega todos os arquivos que tem os arcordes
fileMusic = getAllFiles(dirWav, fileWav, appendFullPath);

for i=1 : numel(fileMusic) % loop through each file
    fname = fullfile(dirWav,fileMusic{i}); % fullname of the file
    fname
end