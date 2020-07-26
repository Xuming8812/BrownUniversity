function [D] = SelectWindow(I,s)
    %Function :     SelectWindow
    %Description:   Automatically select a suitable window for element (i,j)
    %Input:         I----Type: matrix of double; Meaning: the input matrix
    %               i----Type: int; Meaning: row number of the element
    %               j----Type: int; Meaning: column number of the element
    %               s----Type: int; Meaning: the given window size   
    %Output:        D----Type: matrix of int; Meaning: the suitable window
    %                    for each element of I

    %get the size of the input matrix
    [rowNum_I,colNum_I] = size(I);
    
    D = zeros(rowNum_I,colNum_I,4);
    
    Threshold = 20;
    for i = 1:rowNum_I
        for j = 1:colNum_I
            
                y1 = i - s;
                x1 = j - s;
                y2 = i + s;
                x2 = j + s;

                isUpper = false;
                isLeft = false;
                isBottom = false;
                isRight = false;

                %if the window is out of boundary, determine which coordinate is out of
                %boundary
                if i-s<1
                   y1=1;
                   isUpper = true;      
                end

                if j-s<1
                    x1 = 1;
                    isLeft = true;
                end

                if i + s>rowNum_I
                    y2 = rowNum_I;
                    isBottom = true;
                end

                if j + s>colNum_I
                    x2 = colNum_I;
                    isRight = true;
                end

                %get all the elements from Matrix I within the window
                %currentRow = y2 - y1 + 1;
                %currentCol = x2 - x1 + 1;
                %temp = zeros(currentRow,currentCol);
                temp = I(y1:y2,x1:x2);

                %divide the window into 4 parts and see which part has most texture

                   xx = round(x2/2+x1/2);
                   yy = round(y2/2+y1/2);

                   part1 = I(y1:yy,x1:xx);%upper left
                   part2 = I(y1:yy,xx:x2);%upper right
                   part3 = I(yy:y2,x1:xx);%bottom left
                   part4 = I(yy:y2,xx:x2);%bottom right

                   std_part = zeros(4,1);
                   std_part(1) = std2(part1);
                   std_part(2) = std2(part2);
                   std_part(3) = std2(part3);
                   std_part(4) = std2(part4);

                   [maxValue, indexMax] = max(std_part);
                   [minValue, indexMin] = min(std_part);       


                currentSigma = std2(temp);

                if currentSigma < Threshold
                    while currentSigma< Threshold
                        %determine in which direction the window should be expanded
                        switch indexMax
                            case 1
                                %if upperleft part has more texture
                                if isUpper
                                    y2=y2+1;
                                else
                                    if y1>1
                                       y1 = y1-1;
                                    else
                                        isUpper =true;
                                        y2 = y2+1;
                                    end                        
                                end

                                if isLeft
                                    x2 = x2+1;
                                else
                                    if x1>1
                                        x1 = x1-1;
                                    else
                                        isLeft = true;
                                        x2 = x2+1;
                                    end
                                end

                            case 2
                                %if upper right part has more texture
                                if isUpper
                                    y2=y2+1;
                                else
                                    if y1>1
                                       y1 = y1-1;
                                    else
                                        isUpper =true;
                                        y2 = y2+1;
                                    end                        
                                end 

                                if isRight
                                    x1 = x1-1;
                                else
                                    if x2 <colNum_I
                                        x2 = x2+1;
                                    else
                                        isRight = true;
                                        x1 = x1-1;
                                    end
                                end

                            case 3
                                %if bottom left part has more texture
                                if isLeft
                                    x2 = x2+1;
                                else
                                    if x1>1
                                        x1 = x1-1;
                                    else
                                        isLeft = true;
                                        x2 = x2+1;
                                    end
                                end 

                                if isBottom
                                    y1 = y1-1;
                                else
                                    if y2<rowNum_I
                                        y2 = y2+1;
                                    else
                                        isBottom = true;
                                        y1 = y1-1;
                                    end
                                end  

                            case 4
                                if isRight
                                    x1 = x1-1;
                                else
                                    if x2 <colNum_I
                                        x2 = x2+1;
                                    else
                                        isRight = true;
                                        x1 = x1-1;
                                    end
                                end

                                if isBottom
                                    y1 = y1-1;
                                else
                                    if y2<rowNum_I
                                        y2 = y2+1;
                                    else
                                        isBottom = true;
                                        y1 = y1-1;
                                    end
                                end  

                        end

                        if y2 - y1>2*s || x2 -x1>2*s
                             break;
                        end

                        clear temp;

                        temp = I(y1:y2,x1:x2);
                        currentSigma = std2(temp);

                    end
                else
                    while currentSigma> Threshold
                         %determine in which direction the window should be shrinked
                        switch indexMin
                            case 1
                                x1 = x1+1;
                                isLeft = false;
                                y1 = y1+1;
                                isUpper = false;

                            case 2
                                y1 = y1+1;
                                isUpper = false;
                                x2 = x2-1;
                                isRight = false;

                            case 3
                                x1 = x1+1;
                                isLeft = false;
                                y2 = y2 -1;
                                isBottom = false;

                            case 4
                                x2 = x2-1;
                                isRight = false;
                                y2 = y2 -1;
                                isBottom = false;                                        
                        end


                        clear temp;           
                        temp = I(y1:y2,x1:x2);
                        currentSigma = std2(temp);

                        if y2 - y1<2 || x2 -x1<2
                             break;
                        end

                    end       
                end
                
                D(i,j,1) =x1;
                D(i,j,2) =y1;
                D(i,j,3) =x2;
                D(i,j,4) =y2;
        end
    end
    %assign initial values, a square centered with £¨i,j£©
end

