function [w,Loss] = gradientDescent(x,y,C,r,T)
    %generate a random w matrix
    w = rand(785,10,'double');
    Loss = [];
    d = 1.01; 
    
    %iteration for T times
    for i = 1:T
        %calculate Loss and gradient of the loss
        [E, G] = calculateEw(w,x,y,C);
        %save loss for further visulization
        Loss = [Loss, E];
        %update w
        w = w - r * G;
        %decrease stepsize
        r = r / d;
    end   
end

