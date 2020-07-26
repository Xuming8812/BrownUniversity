function [M] = RidgeDetection(M_magnitude,M_dfx,M_dfy)

[rowNum,colNum] = size(M_magnitude);

M = zeros(rowNum,colNum);

    for i = 1:rowNum                                                        %threshold the M_magnitude by replacing the element smaller than threshold by 0
        for j = 1: colNum
            
            delta_x = round(M_dfx(i,j));                                    %calculate the int value of dx and dy
            delta_y = round(M_dfy(i,j));

            if i-delta_x>=1 && j-delta_y>=1 && i-delta_x<=rowNum && j-delta_y<=colNum
                edge1 = M_magnitude(i-delta_x,j-delta_y);                   %get the pixel whose coordinate is (i-dx,j-dy)
            else
                edge1 =0;
            end

            if i+delta_x<=rowNum && j+delta_y<=colNum && i+delta_x>=1 && j+delta_y>=1
                edge2 = M_magnitude(i+delta_x,j+delta_y);                    %get the pixel whose coordinate is (i+dx,j+dy)
            else
                edge2 =0;
            end

            if(M_magnitude(i,j)>edge1 && M_magnitude(i,j)>=edge2)           %if the pixel is a local maximum pixel, then save it in the result matrix
                M(i,j)= M_magnitude(i,j);    
            end            
        end
    end

end

