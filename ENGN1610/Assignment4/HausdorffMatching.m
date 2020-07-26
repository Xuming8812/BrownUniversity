function [] = HausdorffMatching(I,T,distance,coefficient);
    %Function :     HausdorffMatching
    %Description:   Implementation of Hausdorff Matching of given image
    %               with given template
    %Input:         I----Type: matrix of int; Meaning: the matrix
    %                       storing the input image
    %               T----Type: matrix of int; Meaning: the matrix
    %                       storing the template image
    %               distance----Type: int; Meaning: the width of the
    %                       dilated image
    %               cofficient----Type: double; Meaning: parameter of
    %                       threshold. The threshold value will be
    %                       calculate by multiplying the max value of
    %                       correaltion matrix with the coefficient

%set the default parameter value if those parameters are not given
    if nargin <4
        distance = 6;
        coefficient = 0.95;
    end

%dilate the I
D = Dilate(I,distance);

% get the template
%T = im2double(I(181:216,87:126));

%imshow(T);

%calculate the correlation of J and T
F = imfilter(D,T,'same','symmetric');

%get the threshold value by 96% of the max value
threshold = max(max(F))*coefficient;

%find local maxima and threshold with the input threshold
[rowNum_T,colNum_T] = size(T);

%threshold the image and find local maximum
J = LocalMaximaAndThreshold(F,threshold,colNum_T/2,rowNum_T/2);

%draw the rectangle centered at the local maximum with the size of template
M = DrawRectangle(J,I,colNum_T,rowNum_T);

%show the image with rectangles
imshow(M);

end

