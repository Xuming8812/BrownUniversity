function [J] = EdgeDetectionCanny(path,sigma,threshold)
	%Function :     EdgeDetectionCanny
    %Description:   Smooth the given image by gaussian filter, which is 
    %               defined by the given parameter "sigma". Then use canny
    %               method to detect the edge. One threshold parameters are
    %               needed while another threshold parameter is optional.
    %               If two threshold parameters are given, then a
    %               two-threshold canny method will be used to detect the
    %               edges.
    %Input:         path--------type: string; meaning:the path of the input image
    %               sigma-------type: doulbe; meaning:parameter for gaussian smooth
    %               threshold --type: vector of double; meaning;threshold parameter for detecting edge
    %Output:        J-----------type: matrix of double; meaning: the image after edge detection

    I = imread(path);                                                           %open the given image and store the gray values in matrix I
    
    G = GaussianSmooth(I,sigma);                                                %smooth the image by 2D gaussian filter
       
    [M_x,M_y,M] = GradientCalculation(G);                                       %calculate the gradient value of the smoothed image
    
    [row,col] = size(threshold); 
    
    M_peak = RidgeDetection(M,M_x,M_y);                                         %detect ridge in the image
    
    if row + col == 2
        J = EdegDetect_1threshold(G,M_peak,threshold);                          %edge detection with one threshold input
    else
        J = EdegDetect_2thresholds(G,M_peak,threshold(1,1),threshold(1,2));     %edge detection with two threshold inputs
    end
        
    subplot(1,2,1);                                                             %show the origin image and final image together
    imshow(I);    
    subplot(1,2,2);
    imshow(J);
    
end

