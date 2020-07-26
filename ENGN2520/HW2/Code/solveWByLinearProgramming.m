function [w] = solveWByLinearProgramming(x,y,deg)
    %get size
    [rowNum, col] = size(x);

    deg = deg + 1;
    %initialization
    A = zeros(2*rowNum, rowNum+deg);
    b = zeros(2*rowNum,1);
    C = zeros(1,rowNum+deg);
    
    %generate C
    index = deg+1:rowNum+deg;
    C(index) = 1;
    
    %generate b
    index = 1:2:2*rowNum-1;
    b(index) = y;
    index = 2:2:2*rowNum;
    b(index) = -y;
    
    %generate A
    for row = 1:2:2*rowNum-1
       for col = 1:deg
           A(row,col) = x(ceil(row/2),1).^(col-1);
       end
       
       A(row,deg+ceil(row/2))=-1;
    end
    
    for row = 2:2:2*rowNum
        A(row,:) = -A(row-1,:);
        A(row,deg+ceil(row/2))=-1;
    end
    %calculate w by linear program
    result = linprog(C,A,b);
    
    w = result(1:deg);
end

