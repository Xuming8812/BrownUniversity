function [I] = DrawRectangle_DifferentSizes(I,R);
    %Function :     DrawRectangle
    %Description:   Draw rectangles on the original image to display
    %               matching results
    %Input:         I----Type: matrix of integers; Meaning: the matrix
    %                       storing the original images
    %               R----Type: matrix of integers; Meaning: the matrix
    %                       storing the matching results
    %Output:        I----Type: matrix of integers; Meaning: the image after
    %                       drawing rectangles 
    
    %get the size of original image
    [rowNum_I,colNum_I] = size(I);
    %get the size of result matrix
    [rowNum_R,colNum_R] = size(R);
    
    %loop every detection result in input results
    for i = 1:rowNum_R
        %get size of the rectangle
       length = 2 * R(i,4);
       width = 2 * R(i,5);
       %get center of the rectangle
       row = R(i,2);
       col = R(i,3);
       
       %get the left coordinate of the retangle
       left = col - round(length/2);
        if left<1
            left =1;                        
        end
         %get the right coordinate of the retangle
        right = col+round(length/2);
        if right>colNum_I
           right = colNum_I;
        end
        %get the up coordinate of the retangle
        up = row - round(width/2);
        if up<1
            up =1;
        end
        %get the down coordinate of the retangle
        down = row + round(width/2);                    
        if down > rowNum_I
            down = rowNum_I;
        end
        %draw the horizontal lines
        for m = left:right
            I(up,m) = 1;
            I(down,m) = 1;
        end
        %draw the vertical lines
        for m = up:down
           I(m,left) = 1;
           I(m,right) = 1;
        end   
        
    end
    %show the image with rectangles
    imshow(I);
    
end

