function [fx] = calculateFxByGivingW(x,w)
    %get degree
    [deg, col] = size(w);
    %get size
    [rowNum, col] = size(x);
    %initialize fx
    fx = zeros(rowNum, col);
    %calculate fx by usuing polynomial function defined by w
    for row = 1:rowNum
        for i = 1:deg
            fx(row,1) = fx(row,1) + w(i)*x(row,1)^(i-1);
        end 
    end
end

