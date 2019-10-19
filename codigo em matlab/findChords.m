function fileList = findChords(filterchords, chord)
    
    fileList = 0;
    
     for i = 1 : length(filterchords)
         if(strcmp(filterchords(i), chord))
             fileList = 1;
         end
     end
end