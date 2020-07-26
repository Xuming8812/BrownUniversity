function [rms] = calculateRMS(x,y,w)
    %initialize rms
    rms = 0;
    %get size of input data
    [N,col] = size(x);
    %calcuate fx based on x and w
    fx = calculateFxByGivingW(x,w);
    %calculate rms
    for i = 1:N
        rms = rms+(fx(i)-y(i)).^2;
    end
    
    rms = sqrt(rms/N);
end

