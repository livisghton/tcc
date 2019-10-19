%Esta funcao retorna uma lista de acorde com base no mumero de corte
function filterchords = getChordsList(fileName, numberCut)
    
    [number, chords] = textread(fileName,'%d %s');
    
    for i = 1 : size(chords, 1)
        if(i <= numberCut)
            filterchords(i) = chords(i);
        end 
    end
end