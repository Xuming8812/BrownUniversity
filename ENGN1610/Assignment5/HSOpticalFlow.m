function [u,v] = HSOpticalFlow(frame1,frame2,lambda);
    %Function :     HSOpticalFlow
    %Description:   Calculate the optical flow based on 2 input images and
    %                       the given parameter lambda
    %Input:         frame1----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %               frame2----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %               lambda----Type: double; Meaning: parameter for
    %                       smoothing part
    %Output:        u----Type: matrix of double; Meaning: the image
    %                       storing the x component of optical flow
    %               v----Type: matrix of double; Meaning: the image
    %                       storing the y component of optical flow 
    
    
    %get the size of input image
    [row,col] = size(frame1);
    
    %show the two input images
    %figure;
    %imshow(frame1);
    %figure;
    %imshow(frame2);

    %set the default value of lambda
    if nargin <3
        lambda = 1;
    end
    
    %calculate the derivatives, Ix,Iy and It
    [Ix,Iy,It] = Derivatives(frame1,frame2);

    %set the initial value to u and v
    u = zeros(row,col);
    v = zeros(row,col);

    %the matrix to calculate the mean of one pixel`s 8 neighboring pixels
    mean=[1/6 1/12 1/6;1/6 0 1/6;1/6 1/12 1/6];

    %total loop numbers
    loopNum = 20;

    for i = 1;loopNum
        
        %in each iteration, first calculate the uMean and vMean
        uMean=conv2(u,mean,'same');
        vMean=conv2(v,mean,'same');
        %update u and v, based on Ix,Iy,It,uMean and vMean, these equations
        %are calculated in part I in the pdf document
        u= uMean - ( Ix .* ( ( Ix .* uMean ) + ( Iy .* vMean ) + It ) ) ./ ( lambda + Ix.^2 + Iy.^2); 
        v= vMean - ( Iy .* ( ( Ix .* uMean ) + ( Iy .* vMean ) + It ) ) ./ ( lambda + Ix.^2 + Iy.^2);
    end

    %calculate the magnitude of optical flow of each pixel
    magnitude = u.^2 + v.^2;

    figure;
    imagesc(magnitude,[0,1]);
    colormap(gray);
end


