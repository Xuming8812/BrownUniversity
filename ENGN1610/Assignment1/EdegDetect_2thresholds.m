function [J] = EdegDetect_2thresholds(I,M_magnitude,threshold,threshold2)
    
    [rowNum,colNum] = size(I);                                              %calculate the size of the input image
    J = I;
    %calculate the low threshold and high threshold
    lowlimit = min(threshold,threshold2);
    highlimit = max(threshold,threshold2);
    %define a stack to store all the strong edge pixels
    Edges = StackStructure;
     
     for i = 1:rowNum                                                        
        for j = 1: colNum
            if M_magnitude(i,j)>=highlimit
                Edges.push([i,j]);                                          %if the intensity is above high threshold, then this pixel is a strong edge and needed to be stored in the stack
                J(i,j) = 255;
            else
                J(i,j) = 0;
            end
            
            if M_magnitude(i,j)< lowlimit
                M_magnitude(i,j) = 0;                                       %if the intensity is below the low threshold, then it`s definately not a edge pixel.
            end
        end
     end
     
     %loop all the pixels in the stack 
     while Edges.size() ~=0
         %pop the top pixel in stack
         sizeElement = Edges.pop();
         %get the coordinate of the pixel
         i = sizeElement(1);
         j = sizeElement(2);
         %loop all the eight neighbors
         for m= -1:1
            for n = -1:1
                if(i+m)>=1 && i+m<=rowNum && j+n>=1 && j+n<=colNum &&(i+m)~=i && (j+n)~=j
                    %if the neighbor is a weak edge pixel then push it in
                    %the stack and consider it as a strong edge pixel
                    if M_magnitude(i+m,j+n) >= lowlimit && M_magnitude(i+m,j+n) < highlimit
                        Edges.push([i+m,j+n]);
                        %consider it as a strong edge pixel to avoid
                        %repeated check
                        J(i+m,j+n) = 255;
                        M_magnitude(i+m,j+n) = highlimit+1;
                    end
                end
            end
         end
     
     end
      
end

