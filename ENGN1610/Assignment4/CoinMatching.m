function [] = CoinMatching(I);
    %Function :     CoinMatching
    %Description:   Match the coins in the input image with different sizes
    %Input:         I----Type: matrix of double; Meaning: the matrix
    %                       storing the input image

    %set the default parameters of distance and coefficient
    distance = 4;
    coefficient = 0.9999;

    %dilate the input image
    D = Dilate(I,distance);
    
    
    firstSearch = 1;

    for i = 10:30
        %generate the T with given radius
       T = GenerateCircleTemplate(i);
        %calculate the correlation between two images
       F = imfilter(D,T,'same','symmetric');

       %get the threshold
       threshold = max(max(F))*coefficient;
       %threshold = 240;
       [rowNum_T,colNum_T] = size(T);

        %threshold the image and find local maximum
        [J,R] = LocalMaximaAndThreshold_DifferentSizes(F,threshold,colNum_T/2,rowNum_T/2);

        %compared with previous matching results
        if firstSearch == 1
            result = R;
            firstSearch = 0;
        else
            result = FindBestMatch(result,R);
        end

    end
    %draw rectangles to display matching results
    DrawRectangle_DifferentSizes(I,result);
end

