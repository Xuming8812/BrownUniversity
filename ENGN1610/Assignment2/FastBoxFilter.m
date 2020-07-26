function [G] = FastBoxFilter(I,halfSize)
    %Function :     FastBoxFilter
    %Description:   Calculate the convolution of given matrices I and a box
    %               filter B in O(m^2) time complexity independent of the
    %               box size
    %Input:         I----Type: matrix of double; Meaning: the input matrix
    %               B----Type: matrix of double; Meaning: box filter
    %Output:        J----Type: matrix of double; Meaning: convolution of matrix I and box filter B
    
     %get the size of the input matrix
    [rowNum_I,colNum_I] = size(I);
    
    %calculate the integral image of I
    J = IntegralImage(I);
    
    
    G = zeros(rowNum_I,colNum_I);
     
    %store the convolution result in the matrix
    for i = 1:rowNum_I
        for j = 1 : colNum_I
            G(i,j) = BoxFilterSum(J,j-halfSize,i-halfSize,j+halfSize,i+halfSize);
        end
    end
    
    
end

