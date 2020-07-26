function [H] = Convolution(I,J)
	%Function :     Convolution
    %Description:   Calculate the convolution of given matrices I and J. To
    %               deal with the boundary condition, expand the
    %               matrix I by adding a circle of '0' around it.
    %Input:         I----Type: matrix of integers; Meaning: first input matrix
    %               J----Type: matrix of double; Meaning: second input matrix
    %Output:        H----Type: matrix of double; Meaning: convolution of matrix I and matrix J  

    [rowNum_I,colNum_I] = size(I);                                          %calculate size of matrix I
    [rowNum_J,colNum_J] = size(J);                                          %calculate size of matrix J
    
    %expand the matrix I by padding 0, note the (rowNum_J-1) rows should be
    %added at either side of I and (colwNum_J-1) columns should be added at
    %either side
    M = zeros(rowNum_I+2*(rowNum_J-1),colNum_I + 2*(colNum_J-1));
    H = M;
    for i = rowNum_J:rowNum_I+rowNum_J-1
        for j = colNum_J:colNum_I+colNum_J-1
            M(i,j) = I(i - rowNum_J+1,j-colNum_J+1);
        end
    end
    
    %flip the matrix J by 180deg
    J = rot90(J,2);
    
    
    result = 0;
    %align the center of the matrix J to each element from matrix I
    for i = rowNum_J:rowNum_I+rowNum_J-1
        for j = colNum_J:colNum_I + colNum_J-1
            %include the matrix which has the same size with matrix J and
            %centered with the element from matrix I
            temp = M(i-floor(rowNum_J/2):i+floor(rowNum_J/2),j-floor(colNum_J/2):j+floor(colNum_J/2));           
            %calculate the sum of product between corresponding elements
            result = sum(sum(temp.*J));
            %save result in the expanded matrix
            H(i,j) = result;
            result = 0;
        end
    end
    %return the center part of the expanded matrix which is the result of
    %convolution of I and J
    H = H(rowNum_J:rowNum_I+rowNum_J-1,colNum_J:colNum_I+colNum_J-1);
end

