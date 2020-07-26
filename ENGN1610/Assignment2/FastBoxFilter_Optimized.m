function [G] = FastBoxFilter_Optimized(I,halfSize,windowCoordinate)
    %Function :     FastBoxFilter
    %Description:   Calculate the convolution of given matrices I and a box
    %               filter B in O(m^2) time complexity independent of the
    %               box size
    %Input:         I----Type: matrix of double; Meaning: the input matrix
    %               B----Type: matrix of double; Meaning: box filter
    %Output:        J----Type: matrix of double; Meaning: convolution of matrix I and box filter B
    
     %get the size of the input matrix
    [rowNum_I,colNum_I] = size(I);
    
    %a parameter to judge whether the window is matched perfectly
    localMin = 200;
    
    %calculate the integral image of I
    J = IntegralImage(I);
    
    
    G = zeros(rowNum_I,colNum_I);
     
    %store the convolution result in the matrix
    for i = 1:rowNum_I
        for j = 1 : colNum_I
            
            localSum = BoxFilterSum(J,windowCoordinate(i,j,1),windowCoordinate(i,j,2),windowCoordinate(i,j,3),windowCoordinate(i,j,4));
            
            % if the local sum is below threshold, all the elements in the
            % window will share the same threhold
            if localSum<localMin
                for m = windowCoordinate(i,j,2):windowCoordinate(i,j,4)
                    for n = windowCoordinate(i,j,1):windowCoordinate(i,j,3)
                        if  localSum< G(m,n)|| G(m,n)==0
                            G(m,n) = localSum;
                        end
                          %G(m,n) = localSum;
                    end                
                end
            else                
                if G(i,j) == 0
                	G(i,j) =localSum;
                else
                    if localSum< G(m,n)
                       G(i,j) =localSum;
                    end
                end
            end
            

        end
    end
    
    
end

