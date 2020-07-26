function keyPoints = detectCornerKeypoints(image, parameters)

% ------------------------------------------------------------------------
% This function detects and returns corner points in a grayscale image.
% 
% Inputs :
%     image      : a grayscale image
%     parameters : a struct of algorithm parameters  
% 
% Outputs :
%     keyPoints : [x y] coordinate pairs of detected corner points
% ------------------------------------------------------------------------

% ------------------------------------------------------------------------ 
%                                                                    TODO 
% Implement the corner detection algorithm using lecture notes.
% Return a N x 2 matrix of [x y] coordinate pairs. 
% ------------------------------------------------------------------------

    keyPoints = [];
    %get the size of input image;
    [rowNum,colNum] = size(image);


    %get the gaussian filter
    G = fspecial('gaussian',max(1,fix(6*parameters.sigma1+1)),  parameters.sigma1);     %get a 2D gaussian filter
    %calculate Gx, Gy
    [Gx,Gy] = gradient(G);  
    %get fx
    fx = conv2(image,Gx,'same');
    %get fy
    fy = conv2(image,Gy,'same');                 

    %get three spatial maps
    A = fx.*fx;
    B = fx.*fy;
    C = fy.*fy;
    %blur these maps with gaussian filter
    g = fspecial('gaussian',max(1,fix(6*parameters.sigma2)),  parameters.sigma2);
    A_blurred = conv2(A,g,'same');
    B_blurred = conv2(B,g,'same');
    C_blurred = conv2(C,g,'same');


    %compute tr and det
    tr = A_blurred + C_blurred;
    det = A_blurred.*C_blurred - B_blurred.*B_blurred;

    %get R
    R = det - parameters.alpha*(tr.*tr);
    %non-maximum supression
    R = nonMaximumSuppression(R);
    %get the max value of R
    maxValue = parameters.thresholdMultiplier*max(max(R));

    %threshold the image to get the corners
    for row = 1:rowNum
        for col = 1:colNum
           if R(row,col)>maxValue
               keyPoints = [keyPoints;[col,row]];
           end
        end
    end

end