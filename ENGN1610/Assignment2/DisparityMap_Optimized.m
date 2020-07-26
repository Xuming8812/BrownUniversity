function [Disp]=DisparityMap_Optimized(pathLeft,pathRight,windowSize,direction)
	%Function :     DisparityMap
    %Description:   Take two input images and the window size to calculate 
    %               the disparity map for the first input image based on the second input image.
    %Input:         pathLeft-----Type: string; Meaning: the path and name of the given first input image
    %               pathRight----Type: string; Meaning: the path and name of the given second input image
    %               windowSize---Type: int; Meaning: the window size of the box filter
    %Output:        Disp---------Type: matrix of double; Meaning: the disparity map for the fisrt(left) image
    
    if nargin <4
        direction = true;
    end
    %open the given left image and store the gray values in matrix I
    I = imread(pathLeft);
    %open the given right image and store the gray values in matrix J
    J = imread(pathRight);

    %calculate size of matrix I
    [rowNum_I,colNum_I] = size(I);
    %calculate size of matrix J
    %[rowNum_J,colNum_J] = size(J);
    
    l = round(windowSize -1)/2;
    
    WindowCoordinate = SelectWindow(I,l);
    %a parameter to determine the limit of disparity "d"
    maxD = 30;

    
    %initialize the Disparity Map
    D = zeros(maxD,rowNum_I,colNum_I);
    %loop each element in matrix I to calculate d(0)(x,y)
    if direction
        for i = 1:rowNum_I
            for j = 1:colNum_I
                for d = 1:maxD
                    if j-d>0                    
                        %D(d,i,j) = (I(i,j) - J(i-d,j))^2;                    
                        D(d,i,j) = (double(I(i,j)) - double(J(i,j-d)))^2;
                    else
                        D(d,i,j) = (double(I(i,j)) - double(J(i,1)))^2;
                        %D(d,i,j) = (double(I(i,j)) - double(J(i,j+d)))^2;                    
                    end                 
                end
            end
        end
    else
        for i = 1:rowNum_I
            for j = 1:colNum_I
                for d = 1:maxD
                    if j+d<colNum_I                           
                        %D(d,i,j) = (double(I(i,j)) - double(J(i,j-d)))^2;
                        D(d,i,j) = (double(I(i,j+d)) - double(J(i,j)))^2;
                    else
                        D(d,i,j) = (double(I(i,colNum_I)) - double(J(i,j)))^2;
                    end                 
                end
            end
        end
    end

    
    
        
    value = D;
        
    for d = 1:maxD
        temp = zeros(rowNum_I,colNum_I);
        for i = 1 : rowNum_I
            for j = 1:colNum_I
                temp(i,j) = D(d,i,j);
            end
        end
        
        %value(d,:,:) = BoxFilterConvolution(temp,l);
        %value(d,:,:) = FastBoxFilter(temp,l);
        %localSum = FastBoxFilter_Optimized(temp,l,WindowCoordinate);
                        
        value(d,:,:) = FastBoxFilter_Optimized(temp,l,WindowCoordinate);
    end
    
    Disp = zeros(rowNum_I,colNum_I);
    
    for i = 1 : rowNum_I
        for j = 1:colNum_I
            argu = value(:,i,j);            
            [maxValue index] = min(argu);
            Disp(i,j) = index;            
        end
    end
        
    figure;
    
    %Disp = GaussianSmooth(Disp,1);
    
    Temp = Disp/max(max(Disp));
    imshow(Temp);

end

