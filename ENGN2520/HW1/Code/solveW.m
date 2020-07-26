function [w] = solveW(x,y,deg)
    %initialization
    M = zeros(deg+1,deg+1);
    Z = zeros(deg+1,1);
    %contruct matrix M
    for row = 1:deg+1
       for col = 1:deg+1
            M(row,col) = sum((x.^(row-1)).*(x.^(col-1)));
       end
    end
    %construct matrix Z
    for row = 1:deg+1
        Z(row,1) = sum(y.*(x.^(row-1)));
    end
    %calculate w
    w = M\Z;
end

