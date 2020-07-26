%% Canny Edge Detection Method
%Parameters:1.sigma for gaussian filter for smoothing;
%           2.Treshold M for finding the edge
%Purpose : Try find thin edge for a given picture


%% Declare parameters for test
Sigma = 0.5;
Threshold = 8;

%% load the image
I = imread('elephants.pgm');
% I = imread('bear.pgm');
% I = imread('boat.pgm');
% I = imread('tsukuba.pgm');
[rowNum,colNum] = size(I);
imagesc(I)

%% Smooth by a gaussian

gaussian_2D = fspecial('gaussian',5,0.5);
J = conv2(I,gaussian_2D,'same'); 
imagesc(J)         % show the picture after smoothing

%% Calculate Gradient
pdxFilter = [1 0 -1];
pdyFilter = [1;0;-1];
M_pdx = conv2(J,pdxFilter,'same');
M_pdy = conv2(J,pdyFilter,'same');
M_magnitude = sqrt(M_pdx.^2+M_pdy.^2);
M_pdx = M_pdx./M_magnitude;
M_pdy = M_pdy./M_magnitude;

%% Threshold the Gradient Magnitude
for i = 1:rowNum
    for j = 1: colNum
        if M_magnitude<Threshold
        M_magnitude(i,j) = 0;
        end
    end
end
