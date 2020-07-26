function [J] = DistanceMap(I);
    %Function :     DistanceMap
    %Description:   Calculate the distance map of input image I
    %Input:         I----Type: matrix of integers; Meaning: the input image
    %Output:        J----Type: matrix of integers; Meaning: the distance 
    %                       map of Image I  
        
    %calculate size of matrix I
    [rowNum_I,colNum_I] = size(I);

    J = zeros(rowNum_I,colNum_I);
    
    %set the initial values of the distance map, if a pixel is not edge,
    %then the initial distance will be set to infinite
    for i = 1:rowNum_I    
        for j = 1:colNum_I       
            if I(i,j) == 0
                J(i,j) = 1e5;
            end       
        end       
    end
    
    %two pass to calculate the distance
    %first pass to compare the distance with the left and upper neighbors
    for i = 1:rowNum_I 
        for j = 1:colNum_I
            temp1 = 1e5;
            temp2 = 1e5;
            temp3 = J(i,j);
            if i>1
                temp1 = J(i-1,j)+1;
            end
            
            if j>1
                temp2 = J(i,j-1)+1;
            end
                
            J(i,j) = min(temp3,min(temp1,temp2));
         
        end
    end
    %second pass to compare the distance with the right and lower neighbors
    for i = rowNum_I:-1:1
        for j = colNum_I:-1: 1
            temp1 = 1e5;
            temp2 = 1e5;
            temp3 = J(i,j);
            if i<rowNum_I
                temp1 = J(i+1,j)+1;
            end
            
            if j<colNum_I
                temp2 = J(i,j+1)+1;
            end
                
            J(i,j) = min(temp3,min(temp1,temp2));
         
        end
    end
end

