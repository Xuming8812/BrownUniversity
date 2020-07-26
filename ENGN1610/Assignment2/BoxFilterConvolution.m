function [J] = BoxFilterConvolution(I,s)
	%Function :     BoxFilterConvolution
    %Description:   Calculate the convolution of given matrices I and a box
    %               filter B in O(m^2) time complexity independent of the
    %               box size
    %Input:         I----Type: matrix of double; Meaning: the input matrix
    %               B----Type: matrix of double; Meaning: box filter
    %Output:        J----Type: matrix of double; Meaning: convolution of matrix I and box filter B
       
    [rowNum_I,colNum_I] = size(I); 
    
    halfWindowSize = s+1;
    %store the Sum(Sum(I(i,j))) in G(i,j)
    
    %expand the matrix I by padding 0, note the l+1 rows should be
    %added at either side of I and l+1 columns should be added at
    %either side
    G = zeros(rowNum_I+2*halfWindowSize,colNum_I+2*halfWindowSize);
    
    for i = halfWindowSize+1:halfWindowSize+rowNum_I
        for j = halfWindowSize+1:halfWindowSize+colNum_I
            G(i,j) = I(i-halfWindowSize,j-halfWindowSize);
        end
    end
 
    %deal with the first column
    for i = 2+halfWindowSize:rowNum_I+2*halfWindowSize
        G(i,1+halfWindowSize) = G(i,1+halfWindowSize) + G(i-1,1+halfWindowSize);
    end
     %deal with the first row
    for i = 2+halfWindowSize:colNum_I+2*halfWindowSize
        G(1+halfWindowSize,i) = G(1+halfWindowSize,i) + G(1+halfWindowSize,i-1);
    end
    %caclulate the sum(sum(I(i,j)))
    for i = 2+halfWindowSize:rowNum_I+2*halfWindowSize
        for j = 2+halfWindowSize:colNum_I+2*halfWindowSize
            G(i,j) = G(i,j)+G(i-1,j)+G(i,j-1)-G(i-1,j-1);
        end
    end
    %the output matrix
    J = zeros(rowNum_I+2*halfWindowSize,colNum_I+2*halfWindowSize);
    %calculate the sum of a matrix with the center of (i,j) and half window
    %size of l
    for i = 1+halfWindowSize:rowNum_I+halfWindowSize
        for j = 1+halfWindowSize:colNum_I+halfWindowSize                             
            J(i,j) = G(i+s,j+s) + G(i-s-1,j-s-1)-G(i-s-1,j+s)-G(i+s,j-s-1);            
        end
    end
    %return the valid part int the center of the matrix
    J = J(1+halfWindowSize:rowNum_I+halfWindowSize,1+halfWindowSize:colNum_I+halfWindowSize);
end

