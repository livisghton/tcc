function fileList = findChords(filterchords, chord)
    
    fileList = 0;
    
    length(filterchords)
    
     for i = 1 : length(filterchords)
         filterchords(i)
         if(strcmp(filterchords(i), chord))
             fileList = 1;
         end
     end
end