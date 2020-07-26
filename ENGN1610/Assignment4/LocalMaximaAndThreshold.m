function [J] = LocalMaximaAndThreshold(I,threshold,length,width)
    %Function :     LocalMaximaAndThreshold
    %Description:   Threshold the image and find the local maxima. The rectangle 
    %               area is given by its length and width. Within a rectangle, only one
    %               maxima exsits
    %Input:         I----Type: matrix of double; Meaning: the matrix
    %                       storing the input image
    %               threshold----Type: double; Meaning: threshold parameter
    %               length-------Type: int; Meaning: length of rectangle
    %               width--------Type: int; Meaning: width of rectangle
    %Output:        J----Type: matrix of int; Meaning: the matrix
    %                       storing the local maximas

    
    %get the size of input image
    [rowNum_I,colNum_I] = size(I);
    
    J = zeros(rowNum_I,colNum_I);
    %the matrix storing the neighboring coodinates
    Direction = [-1,0;1,0;0,-1;0,1;-1,1;-1,-1;1,1;1,-1];
    
    %count of local maximas
    count = 0;
    
    for i = 1 : rowNum_I
        for j = 1 : colNum_I
            %check whether it`s above the threshold
            if I(i,j)>threshold
                
                isLocalMaxima = 0;
                %loop all directions to find local maximum
                for k = 1:8
                    row = Direction(k,1);
                    col = Direction(k,2);
                    
                    %check if the current pixel is above its neighbor
                   if  i + row>0 && i + row<=rowNum_I && j + col>0 && j + col<colNum_I
                        if I(i,j)>=I(i + row,j + col)
                           isLocalMaxima = 1;
                        else
                            isLocalMaxima = 0;
                            break;
                        end           
                   end
                end

                %if the local maxima is found
                if isLocalMaxima == 1
                   J(i,j) = 1;             
                   count = count +1;
                end
            end           
        end
    end
    
    
    %save all the local maximums in a matrix
    initialMaximum = zeros(count,2);
    
    index = 1;
    
    for i = 1 : rowNum_I 
        for j = 1 : colNum_I
            if J(i,j) == 1
                initialMaximum(index,1) = i;
                initialMaximum(index,2) = j;
                index = index +1;
            end                               
        end
    end
    
    
    %find the local maximum within the given width and length
    for i = 1:count
        for j = 1:count
            
            %loop every pair of local maximums to see whether they are near
            %enough
            if i ~= j
                row1 = initialMaximum(i,1);
                col1 = initialMaximum(i,2);
                row2 = initialMaximum(j,1);
                col2 = initialMaximum(j,2);
                
                
                if J(row1,col1) == 1 && J(row2,col2) == 1
                    if abs(row1-row2)<width && abs(col1-col2)<length
                        
                        %only preserve the bigger local maximum with the
                        %given width and length
                        if J(row1,col1) > J(row2,col2)
                            J(row2,col2) = 0;
                        else
                            J(row1,col1) = 0;
                        end
                    end
                end
            end
        end
    end   
end

