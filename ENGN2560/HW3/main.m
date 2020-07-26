% ------------------------------------------------------------------------
% ENGN2560: Computer Vision
%      HW3: Image Formation & 3D Reconstruction
% ------------------------------------------------------------------------

%% Question 1
clc; clear all; close all;

% Load the colored point cloud
load('./data/Question1/scenePointCloud.mat');

% Load the camera poses
load('./data/Question1/cameraPoses.mat');

%load intrinsic matrix
load('./data/Question1/cameraIntrinsicMatrix.mat')

% Show the point cloud and cameras
axes1 = pcshow(scenePointCloud); 
hold on;
plotCamera('Location',-R1' * T1,'Orientation',R1,'Opacity',0, 'Size', 20);
plotCamera('Location',-R2' * T2,'Orientation',R2,'Opacity',0, 'Size', 20); 
grid(axes1,'on');
axis(axes1,'tight');
set(axes1,'CameraPosition',...
    [5264.74608400312 -1534.61734696361 128.670524332434],'CameraUpVector',...
    [-0.0833474512990768 0.0254818730835091 -0.996194698091746],...
    'DataAspectRatio',[1 1 1]);
hold off;

% TODO: Project 3D points onto image planes

I1 = ConstructImage(scenePointCloud,K,R1,T1,1200,1600);
I2 = ConstructImage(scenePointCloud,K,R2,T2,1200,1600);

imshow(I1);
figure;
imshow(I2);

%% Question 2
clc; close all;

% Set the random number generator seed to get the same results at each run
rng(0);

% Algorithm parameters
params = [];
params.RANSACIterations = 5000;                         % 5000 iterations
params.reprojectionErrorThreshold = 2;                  % 2 pixels
params.bidirectionalMatchConsistencyThreshold = 2;      % 2 pixels
params.correspondenceDensificationFactor = 4;           % every 4 pixels


run('VLFEATROOT/toolbox/vl_setup');

% TODO: Reconstruct the 3D scene
load('./data/Question2/cameraIntrinsicMatrix.mat')

path1='data/Question2/1.jpg';
path2='data/Question2/2.jpg';

%read in two images
I2 = imread(path1);
I1 = imread(path2);

%use one channel to calculate E
I1 = I1(:,:,1);
I2 = I2(:,:,1);

%get and match features
matchMatrix = MatchFeatures(I1,I2);

%calculate essential matrix and best inliers based on matched features
[E,bestInliers] = RANSAC(matchMatrix,K,params.RANSACIterations,params.reprojectionErrorThreshold);

%read in RGB images
I1 = imread(path2);
I2 = imread(path1);

%DrawPointAndLine(I1,I2,E,K);

%calculate R and T based on E
[R,T] = Decompose(E,K,bestInliers);

%densify and triangulate
ptCloud = Trianglation(I1,K,E,R,T,bestInliers,params.correspondenceDensificationFactor,params.bidirectionalMatchConsistencyThreshold);

axes1 = pcshow(ptCloud); 