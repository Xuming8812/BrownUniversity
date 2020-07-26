function [J] = DrawRectangle(I,J,length,width);
    %Function :     DrawRectangle
    %Description:   Draw rectangles on the original image to display
    %               matching results
    %Input:         I----Type: matrix of integers; Meaning: the matrix
    %                       storing the detection results
    %               J----Type: matrix of integers; Meaning: the matrix
    %                       storing the original images
    %               length----Type: int; Meaning: length of the rectangle
    %               width----Type: int; Meaning: width of the rectangle
    %Output:        J----Type: matrix of integers; Meaning: the image after
    %                       drawing rectangles 
    
    
    %calculate the size of original image
    [rowNum_I,colNum_I] = size(I);
    
    for i = 1:rowNum_I
        for j = 1:colNum_I
                %if this pixel is the detection result
                if I(i,j) ==1
                    %get the left coordinate of the retangle
                    left = j - round(length/2);
                    if left<1
                        left =1;                        
                    end
                     %get the right coordinate of the retangle
                    right = j+round(length/2);
                    if right>colNum_I
                       right = colNum_I;
                    end
                    %get the up coordinate of the retangle
                    up = i - round(width/2);
                    if up<1
                        up =1;
                    end
                    %get the down coordinate of the retangle
                    down = i + round(width/2);                    
                    if down > rowNum_I
                        down = rowNum_I;
                    end
                    %draw the horizontal lines
                    for m = left:right
                        J(up,m) = 1;
                        J(down,m) = 1;
                    end
                    %draw the vertical lines
                    for m = up:down
                       J(m,left) = 1;
                       J(m,right) = 1;
                    end                                          
                end
        end
    end  
end

