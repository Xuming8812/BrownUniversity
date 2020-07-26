% ------------------------------------------------------------------------
% ENGN2560: Computer Vision
%      HW1: Feature Detection / Extraction
% ------------------------------------------------------------------------

%% Question 1a : Harris Corner Detection
% Implement the corner detection algorithm
clc; clear all; close all;

% define parameters
params = [];
params.sigma1 = 0.7;
params.sigma2 = 2.0;
params.alpha = 0.04;
params.thresholdMultiplier = 0.01;
params.nonMaxFilterSize = [3 3];

% read in an image
I = checkerboard(50,10,10);
imshow(I);

% extract corner keypoints
keyPoints = detectCornerKeypoints(I, params); 

% show extracted keypoints
if ( ~isempty(keyPoints) )
    figure, imshow(I), hold on, plot(keyPoints(:,1), keyPoints(:,2), 'r*');
end

%% Question 1b : Harris Corner Detection
% Extract corners
clc; clear all; close all;
% define parameters
params = [];
params.sigma1 = 0.7;
params.sigma2 = 2.0;
params.alpha = 0.04;
params.thresholdMultiplier = 0.01;
params.nonMaxFilterSize = [3 3];

% read in an image
I = imread('goldengate-02.png');

% extract corner keypoints
keyPoints = detectCornerKeypoints(I, params); 

% show extracted keypoints
if ( ~isempty(keyPoints) )
    figure, imshow(I), hold on, plot(keyPoints(:,1), keyPoints(:,2), 'r*');
end

I = imread('goldengate-03.png');

% extract corner keypoints
keyPoints = detectCornerKeypoints(I, params); 

% show extracted keypoints
if ( ~isempty(keyPoints) )
    figure, imshow(I), hold on, plot(keyPoints(:,1), keyPoints(:,2), 'r*');
end



%% Question 2a : FAST keypoints
% Extract FAST keypoints
clc; clear all; close all;
% read in an image
I = imread('goldengate-02.png');
% extract Fast keypoints
corners = detectFASTFeatures(I);
% show extracted keypoints
imshow(I); hold on;
plot(corners);
% read in another image
I = imread('goldengate-03.png');
% extract Fast keypoints
corners = detectFASTFeatures(I);
% show extracted keypoints
figure;
imshow(I); hold on;
plot(corners);


%% Question 2b : SURF keypoints
% Extract SURF keypoints
clc; clear all; close all;
% read in an image
I = imread('goldengate-02.png');
% extract SURF keypoints
points = detectSURFFeatures(I);
% show extracted keypoints
imshow(I); hold on;
plot(points);
% read in another image
I = imread('goldengate-03.png');
% extract SURF keypoints
points = detectSURFFeatures(I);
% show extracted keypoints
figure;
imshow(I); hold on;
plot(points);


%% Question 3 : SIFT keypoints and features
% Extract SIFT keypoints 
clc; clear all; close all;
% read in an image
I = imread('goldengate-02.png');
%turn the input image to single precision
J = im2single(I);
% extract SIFT keypoints
[f,d] = vl_sift(J) ;
perm = randperm(size(f,2)) ;
% show extracted keypoints
imshow(I)
h1 = vl_plotframe(f) ;
set(h1,'color','y','linewidth',2) ;
% find the feature frame near (377,145.6)
[row1,col1]=find(abs(f-377)<1);
[row2,col2]=find(abs(f-145.6)<1);
col = intersect(col1,col2);
% show extracted feature frame
h2 = vl_plotsiftdescriptor(d(:,col),f(:,col)) ;
set(h2,'color','g') ;
%% Question 4 : SIFT features extracted on SURF keypoints
% Extract SIFT features on SURF keypoints
clc; clear all; close all;
% read in an image
I = imread('goldengate-03.png');
%turn the input image to single precision
J = im2single(I);
% Extract SURF keypoints
points = detectSURFFeatures(I);
% find the keypoint near (494,441)
[row1,col1]=find(abs(points.Location-494)<1);
[row2,col2]=find(abs(points.Location-441)<1);
row = intersect(row1,row2);
%get the scale and orientation of this keypoint
x = points.Location(row,1);
y = points.Location(row,2);
scale = points.Scale(row);
angle = points.Orientation(row);
%set a custom feature frame based on the keypoint
fc = [x;y;scale;angle];
fc = double(fc);
%extract the SIFT feature 
[f,d] = vl_sift(J,'frames',fc) ;

% show the image
imshow(I);
%Display locations of interest in image
hold on;
plot(points(row));
% show extracted feature frame
h2 = vl_plotsiftdescriptor(d,fc) ;
set(h2,'color','g') ;