function [G] = GaussianSmooth(I,sigma)
	%Function :     GaussianSmooth
    %Description:   Smooth the given Image "I" by gaussian filter, the
    %               gaussian filter is optimized by the given sigma. Implement 
    %               2D gaussian convolution as a sequence of 1D horizontal 
    %               and vertical convolutions.
    %Input:         I------Type: matrix of integers; Meaning:the input image I
    %               sigma--Type: double; Meaning: parameter of the gaussian filter
    %Output:        G------Type; matrix of double; Meaning: the image smoothed by gaussian filter     

    %sigma = 0.5;  
    
    G = I;
    
    length = round(8*sigma)+1;                                                  %calculate the size of gaussian filter size according to the given sigma                                                    
    
    x_gaussian =-round(4*sigma):round(4*sigma);                                 %(-4*sigma 4*sigma) is 
   
    for i = 1:length                                                             %calculate the value of the gaussian filter                       
        x_gaussian(i) = 1/(sqrt(2*pi)*sigma)*exp(-x_gaussian(i)^2/(2*sigma^2));
    end
   
    x_gaussian = x_gaussian/sum(x_gaussian);                                    %normalize the gaussian filter in x direction
        
    y_gaussian = x_gaussian';                                                   %generate the gaussian filter in y direction by tansposing the x direction filter
    
    G = Convolution(I,x_gaussian);                                              %implement 2D gaussian convolution as a sequence of 1D horizontal and vertical convolutions
    G = Convolution(G,y_gaussian);
    

        
end


