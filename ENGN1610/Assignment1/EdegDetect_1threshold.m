function [J] = EdegDetect_1threshold(I,M_magnitude,threshold)
    
    [rowNum,colNum] = size(I);                                              %calculate the size of the input image
    J = I;
   
    %threshold the M_magnitude by replacing the element smaller than threshold by 0                                                                      
    for i = 1:rowNum                                                       
        for j = 1: colNum
            if M_magnitude(i,j)<threshold
                J(i,j) = 0;
            else
                J(i,j) = 255;
            end
        end
    end
    
end

