function [results] = FindBestMatch(History,Current)
    %Function :     FindBestMatch
    %Description:   Compare the previous results of matching with new
    %               matching results. If, within an area, 2 matching resuls
    %               exist, the one with smaller matching value will be
    %               dropped.
    %Input:         History----Type: matrix of double; Meaning: the matrix
    %                       storing the previous matching results
    %               Current----Type: matrix of double; Meaning: the matrix
    %                       storing the current matching results
    %Output:        results----Type: matrix of double; Meaning: the matrix
    %                       storing the matching results
    
    %get the size of previous matching results
    [row_H,col_H] = size(History);
    %get the size of current matching results
    [row_C,col_C] = size(Current);
    
    %a vector storing whether the result is valid
    status = zeros(row_H + row_C,1);
    
    %get the spec size, within the spec only one matching with largest
    %result will exsit
    windowSize = Current(1,4);
    
    %the previous result will be set to valid initially
    for i = 1:row_H
        status(i) = 1;
    end
    
    %loop every matching result in current results
    for i = 1:row_C
        
        isNew = 1;
        %compare it with every result in previous results
        for j = 1:row_H
            
            %if two matching result exsit near enough
            if abs(Current(i,2)-History(j,2))<windowSize && abs(Current(i,3)-History(j,3))<windowSize
               isNew = 0;
               
               %drop the one with smaller matching value, and save the one
               %with bigger value
               if Current(i,1)> History(j,1)
                    status(row_H+i) = 1;
                    status(j) = 0;
               else
                   status(j) = 1;
               end
               
            end         
        end
        
        %if a new matching result is found, save it
        if isNew == 1
            status(row_H+i) = 1;
        end
    end
    
    %get the total number of matching results
    count = sum(status);
    
    %save the matching results
    results = zeros(count,5);
    
    count = 1;
    %save the matching results from previous results
    for i = 1:row_H
        if status(i) == 1
            results(count,:) = History(i,:);
            count = count+1;
        end
    end
     %save the matching results from current results
    for i = 1:row_C
        if status(row_H+i) == 1
            results(count,:) = Current(i,:);
            count = count+1;
        end
    end
end

