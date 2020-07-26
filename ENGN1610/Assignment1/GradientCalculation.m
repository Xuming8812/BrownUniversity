function [M_pdx,M_pdy,M_magnitude] = GradientCalculation(I)
	%Function :     GradientCalculation
    %Description:   Calculate the 2D gradient of the input matrix, save
    %               results in three matrices, namely M_magnitude, M_pdx,
    %               M_pdy.
    %Input:         I--------------Type: matrix of double; Meaning: the input matrix
    %Output:        M_magnitude----Type: matrix of double; Meaning: matrix which 
    %                              stores the magnitude of gradient of each 
    %                              element in the input matrix I
    %               M_pdx----------Type: matrix of double; Meaning: matrix 
    %                              which stores the x component of gradient
    %                              of each element in the input matrix
    %               M_pdy----------Type: matrix of double; Meaning: matrix 
    %                              which stores the y component of gradient
    %                              of each element in the input matrix 
    
    pdxFilter = [1 0 -1];                                                       %filter to calculate part differential x of I
    pdyFilter = [1;0;-1];                                                       %filter to calculate part differential y of I

    M_pdx = Convolution(I,pdxFilter);                                           %calculate the x-gradient of I
    M_pdy = Convolution(I,pdyFilter);                                           %calculate the y-gradient of I

    
    %[M_pdx,M_pdy]=gradient(I);
    
    
    M_magnitude = sqrt(M_pdx.^2+M_pdy.^2);                                      %calculate the magnitude of gradient matrix
    M_pdx = M_pdx./M_magnitude;                                                 %calculate the x direction gradient component matrix
    M_pdy = M_pdy./M_magnitude;                                                 %calculate the y direction gradient component matrix
end

