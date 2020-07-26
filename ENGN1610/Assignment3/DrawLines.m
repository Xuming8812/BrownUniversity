function [I] = DrawLines(I,p);
    %Function :     DrawLines
    %Description:   Adding the calculated path onto the original image
    %Input:         I----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %               p----Type:vector of integers; Meaning: the vector
    %                       stored the shortest path
    %Output:        I----Type: matrix of integers; Meaning: the input image
    %                       with the pixels on the path marked with 255(white)
    
    %calculate size of matrix I
    [rowNum_I,colNum_I] = size(I);
    
    %get the length of the path
    rowNum_P = size(p);
       
    %mark the boundary by setting the pixel to 255
    for i = 1 : rowNum_P
        
        %change the index of vertex back to pixel coordinates
       col = mod(p(i),rowNum_I);
       row = floor(p(i)/rowNum_I)+1;
       
       %mark the pixel by 255
       I(row,col) = 255;        
    end
    % show the picture with the boundary
    %imshow(I);
end

