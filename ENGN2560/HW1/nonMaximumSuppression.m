function [output] = nonMaximumSuppression(input);
% ------------------------------------------------------------------------
% This function detects and returns corner points in a grayscale image.
% 
% Inputs :
%     image      : a grayscale image
% 
% Outputs :
%     output :  image after suppression
% ------------------------------------------------------------------------

    %get the size of input image
    [rowNum,colNum] = size(input);
    %store the image after suppression
    output = zeros(rowNum,colNum);
    %a matrix indicates the 8 neighbors
    neighbors = [-1,-1;-1,0;-1,1;0,-1;0,1;1,-1;1,0;1,1];

    %loop each row
    for row = 10:rowNum-9
        %loop each col
        for col = 10:colNum-9
            isMax = false;

            %loop all its 8 neighbors
            for i = 1:8
               %get the coordinate of the neighbor
               y = row + neighbors(i,1);
               x = col + neighbors(i,2);
               %check the current element is local maximum
               if y>=1 && y<=rowNum && x>=1 && x<=colNum
                    if input(row,col)<=input(y,x)
                        isMax = false;
                        break;
                    else
                        isMax = true;
                    end
               end
            end

            %if it`s local maxima, store it
            if isMax
               output(row,col) = input(row,col); 
            end

        end
    end



end

