function [J] = IntegralImage(I)
	%Function :     IntegralMap
    %Description:   Calculate the Integral Image of given matrices I.
    %Input:         I----Type: matrix of integers; Meaning: the input matrix
    %Output:        J----Type: matrix of double; Meaning: integral image
    %                    of I;
    
    %get the size of the input matrix
    [rowNum_I,colNum_I] = size(I); 
    
    J = double(I);
   
    %store the Sum(Sum(I(i,j))) in G(i,j)
     
    %deal with the first column
    for i = 2:rowNum_I
        J(i,1) = J(i,1) + J(i-1,1);
    end
     %deal with the first row
    for i = 2:colNum_I
        J(1,i) = J(1,i) + J(1,i-1);
    end
    
    %calculate the sum(sum(I(i£¬j)))
    for i = 2:rowNum_I
        for j = 2:colNum_I
            J(i,j) = J(i,j)+J(i-1,j)+J(i,j-1)-J(i-1,j-1);
        end
    end   
end

