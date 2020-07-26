function [sum] = BoxFilterSum(J,x1,y1,x2,y2)
	%Function :     BoxFilterSum
    %Description:   Calculate the Integral Image of given matrices I.
    %Input:         J----Type: matrix of integers; Meaning: the input
    %                    integral image
    %               x1----Type: integer; Meaning: x coordinate of upperleft
    %                     corner of the window
    %               y1----Type: integer; Meaning: y coordinate of upperleft
    %                     corner of the window
    %               x2----Type: integer; Meaning: x coordinate of bottom right 
    %                     corner of the window
    %               y2----Type: integer; Meaning: y coordinate of bottom right               
    %                     corner of the window 
    %Output:        sum----Type: integer; Meaning: sum of the whole window
    
    %note that the x coordinate is actually the column num
    %           the y coordinate is actually the row num
    
    %get the size of the input matrix
    [rowNum_J,colNum_J] = size(J); 
    
    %set the value of upperleft value
    %if it`s out of boundary then set it by 0
    %otherwise set it by J(y1 - 1,x1 - 1);
    if x1 - 1 < 1 || y1 - 1<1
        upperLeft = 0;
    else
        upperLeft = J(y1 - 1,x1 - 1);
    end
    
    %set the value of bottom left value, 
    %if it`s out of left boundary then set it by 0
    %if it`s out ot the bottom boundary then set it by J(end,x1 - 1);
    %otherwise set it by J(y2,x1 - 1)
    if x1 - 1 < 1
        bottomLeft = 0;
    elseif y2<=rowNum_J
        bottomLeft = J(y2,x1 - 1);
    elseif y2>rowNum_J
        bottomLeft = J(end,x1 - 1);   
    end
    
    %set the value of upper Right value, 
    %if it`s out of upper boundary then set it by 0
    %if it`s out ot right boundary then set it by J(end,x1 - 1);
    %otherwise set it by J(y1-1,x2)   
    if y1-1<1
        upperRight = 0;
    elseif x2<=colNum_J
        upperRight = J(y1-1,x2);
    else
        upperRight = J(y1-1,end);
    end
    
    %set the value of bottom Right value, 
    %if it`s out of bottom boundary then set it by J(end,x2)
    %if it`s out ot right boundary then set it to J(y2,end)
    %otherwise set it by J(y2,x2)  
    
    if x2>colNum_J && y2>rowNum_J
        bottomRight = J(end,end);
    elseif x2>colNum_J
        bottomRight = J(y2,end);
    elseif y2>rowNum_J
        bottomRight = J(end,x2);
    else
        bottomRight = J(y2,x2);
    end
                
    sum = bottomRight + upperLeft-bottomLeft-upperRight;    
end

