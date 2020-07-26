% ------------------------------------------------------------------------
% ENGN2560: Computer Vision
%      HW2: Image Stitching
% ------------------------------------------------------------------------

%% Question1-1
% Set the random number generator seed to get the same results at each run
clc; clear all; close all;
rng(0);

% Define parameters
params = [];
params.ratioTestRatio = 0.75;
params.RANSACIterations = 1000;
params.RANSACInlierDistanceThreshold = 0.5;
params.isBlending = 0;
params.featureType = "SIFT";

%run vl-feat library
%run('VLFEATROOT/toolbox/vl_setup');

%For Set 1
path1='data/set1/goldengate-02.png';
path2='data/set1/goldengate-03.png';

%read in two images
I1 = imread(path1);
I2 = imread(path2);

%merge two images
newImage = MergeImages(I1,I2,params);
figure;
imshow(newImage);

%% Question1-2
% Set the random number generator seed to get the same results at each run
clc; clear all; close all;
rng(0);

% Define parameters
params = [];
params.ratioTestRatio = 0.75;
params.RANSACIterations = 10000;
params.RANSACInlierDistanceThreshold = 0.5;
params.isBlending = 0;
params.featureType = "SIFT";

%run vl-feat library
%run('VLFEATROOT/toolbox/vl_setup');
%For Set 2
path1='data/set2/lems-01.png';
path2='data/set2/lems-02.png';
%read in two images
I1 = imread(path1);
I2 = imread(path2);
%merge two images
newImage = MergeImages(I1,I2,params);
imshow(newImage);

%% Question2-1
clc; clear all; close all;
rng(0);

% Define parameters
params = [];
params.ratioTestRatio = 0.75;
params.RANSACIterations = 1000;
params.RANSACInlierDistanceThreshold = 0.5;
params.isBlending = 0;
params.featureType = "SIFT";

%run vl-feat library
%run('VLFEATROOT/toolbox/vl_setup');

%For Set 3
path1='data/set3/halfdome-05.png';
path2='data/set3/halfdome-06.png';
path3='data/set3/halfdome-07.png';

%read in all images
I1 = imread(path1);
I2 = imread(path2);
I3 = imread(path3);

images = {I1;I2;I3};

%merge all images
newImage = MergeMultipleImages(images,params);

imshow(newImage);

%% Question2-2
clc; clear all; close all;
rng(0);

% Define parameters
params = [];
params.ratioTestRatio = 0.75;
params.RANSACIterations = 1000;
params.RANSACInlierDistanceThreshold = 0.5;
params.isBlending = 1;
params.featureType = "SIFT";

%run vl-feat library
%run('VLFEATROOT/toolbox/vl_setup');

images = {};
path1='data/set4/hotel-00.png';
path2='data/set4/hotel-01.png';
path3='data/set4/hotel-02.png';

%read in two images
I1 = imread(path1);
I2 = imread(path2);
I3 = imread(path3);

images = {I1;I2;I3};

%newImage = MergeImages(I2,I3,params);

%merge first two
newImage = MergeMultipleImages(images,params);

imshow(newImage);
%% Extra-1
clc; clear all; close all;
rng(0);

% Define parameters
params = [];
params.ratioTestRatio = 0.75;
params.RANSACIterations = 1000;
params.RANSACInlierDistanceThreshold = 0.5;
params.isBlending = 0;
params.featureType = "SIFT";

%run vl-feat library
%run('VLFEATROOT/toolbox/vl_setup');

images = {};
path1='data/extraCredit/blending/diamondhead-00.png';
path2='data/extraCredit/blending/diamondhead-01.png';
path3='data/extraCredit/blending/diamondhead-02.png';
path4='data/extraCredit/blending/diamondhead-03.png';
path5='data/extraCredit/blending/diamondhead-05.png';
path6='data/extraCredit/blending/diamondhead-06.png';
path7='data/extraCredit/blending/diamondhead-07.png';

I1 = imread(path1);
I2 = imread(path2);
I3 = imread(path3);
I4 = imread(path4);
I5 = imread(path5);
I6 = imread(path6);
I7 = imread(path7);

images = {I1;I2;I3;I4;I5;I6;I7};

%merge first two
newImage = MergeMultipleImages(images,params);
%newImage2 = MergeMultipleImages(images2,params);
%merge two images
%newImage = MergeImages(newImage1,newImage2,params);

imshow(newImage);

%use blending technique
params.isBlending = 1;
newImage1 = MergeMultipleImages(images,params);
figure;
imshow(newImage1);


%% Extra-2
clc; clear all; close all;
rng(0);

% Define parameters
params = [];
params.ratioTestRatio = 0.75;
params.RANSACIterations = 1000;
params.RANSACInlierDistanceThreshold = 0.5;
params.isBlending = 1;
params.featureType = "SIFT";

%run vl-feat library
%run('VLFEATROOT/toolbox/vl_setup');

%For Set 1
path1='data/extraCredit/composite/1900.jpg';
path2='data/extraCredit/composite/2016.jpg';

%read in two images
I1 = imread(path1);
I2 = imread(path2);

%merge two images
newImage = MergeImages(I1,I2,params);

imshow(newImage);
%% Extra-3-SURF features
% Set the random number generator seed to get the same results at each run
clc; clear all; close all;
rng(0);

% Define parameters
params = [];
params.ratioTestRatio = 0.75;
params.RANSACIterations = 1000;
params.RANSACInlierDistanceThreshold = 0.5;
params.isBlending = 0;


%run vl-feat library
%run('VLFEATROOT/toolbox/vl_setup');

%For Set 2
path1='data/set2/lems-01.png';
path2='data/set2/lems-02.png';

%read in two images
I1 = imread(path1);
I2 = imread(path2);

%merge two images using SURF features
params.featureType = "SURF";
newImage = MergeImages(I1,I2,params);
figure;
imshow(newImage);

%merge two images using Harris Corner features
params.featureType = "Harris";

newImage = MergeImages(I1,I2,params);
figure;
imshow(newImage);