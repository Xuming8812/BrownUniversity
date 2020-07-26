function [J] = Dilate(I,d);
    %Function :     Dilate
    %Description:   Dilate the input image I
    %Input:         I----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %               d----Type:int; Meaning: the dilation width
    %Output:        J----Type: matrix of integers; Meaning: the dilated 
    %                       result of Image I  

    %calculate the distance map of image I   
    I = DistanceMap(I);
     %calculate the size of image I
    [rowNum_I,colNum_I] = size(I);
    
    J = zeros(rowNum_I,colNum_I);
    % loop all pixels in distance map and if the distance of this pixel to
    % edge is smaller width, set the corresponding pixel in result matrix
    % by 1
    for i = 1: rowNum_I
        for j = 1 : colNum_I
            if I(i,j)<d
                J(i,j) = 1;
            end        
        end        
    end
end

