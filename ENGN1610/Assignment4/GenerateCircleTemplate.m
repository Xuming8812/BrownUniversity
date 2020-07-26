function [T] = GenerateCircleTemplate(radius);
    %Function :     GenerateCircleTemplate
    %Description:   Generate a circle template with given radius
    %Input:         radius----Type: int; Meaning: the radius of the circle
    %Output:        T----Type: matrix of integers; Meaning: the template generated 
    

    T = zeros(2*radius+1,2*radius+1);

    %loop theta from 0 to 2pi
    for theta=0:0.01:2*pi
        %calculate the x y coordinate in the circle
       x = round(radius * cos(theta));
       y = round(radius * sin(theta));
       T(radius+1+x,radius+1+y) = 1;
    end

end

