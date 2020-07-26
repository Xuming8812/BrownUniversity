function [index] = OptimalWindowSize(pathLeft,pathRight)

        looplength = 50; 
        
        value = zeros(looplength,1);
        
        for i = 1:looplength
            DispLR = DisparityMap(pathLeft,pathRight,2*i+1);
            DispRL = 
        end
        
        [minValue index] = min(value);
end

