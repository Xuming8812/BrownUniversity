function [Ix,Iy,It] = Derivatives(frame1,frame2)
    %Function :     Derivatives
    %Description:   Calculate the derivatives Ix, Iy and It
    %Input:         frame1----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %               frame2----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %Output:        Ix----Type: matrix of double; Meaning: the image
    %                       storing the x derivatives of each pixel
    %               Iy----Type: matrix of double; Meaning: the image
    %                       storing the y derivatives of each pixel
    %               It----Type: matrix of double; Meaning: the image
    %                       storing the t derivatives of each pixel    
    [row,col] = size(frame1);
    
    %turn input images to double format for further guassian filter convolution
    frame1 = double(frame1);
    frame2 = double(frame2);

    %gaussian smooth with sigma = 1;
    frame1 = GaussianSmooth(frame1,1);
    frame2 = GaussianSmooth(frame2,1);
    
    Ix = zeros(row,col);
    Iy = zeros(row,col);
    It = zeros(row,col);
    
    for i = 1:row
        for j = 1:col
           
            if j ~= col && i ~= row
                rightBottom1 = frame1(i+1,j+1);
                rightBottom2 = frame2(i+1,j+1);
            else
                rightBottom1 = 0;
                rightBottom2 = 0;
            end
            
            if( j == col)
                right1 = 0;
                right2 = 0;
            else
                right1 = frame1(i,j+1);
                right2 = frame2(i,j+1);
            end
            
            if i == row
                bottom1 = 0;
                bottom2 = 0;
            else
                bottom1 = frame1(i+1,j);
                bottom2 = frame2(i+1,j);
            end
                       
            Ix(i,j) = (right1-frame1(i,j)+rightBottom1-bottom1+right2-frame2(i,j)+rightBottom2-bottom2)/4;
            Iy(i,j) = (bottom1-frame1(i,j)+rightBottom1-right1+bottom2-frame2(i,j)+rightBottom2-right2)/4;
            It(i,j) = (frame2(i,j)-frame1(i,j)+rightBottom2-rightBottom1+right2-right1+bottom2-bottom1)/4;
        end
    end
    
    %calculate derivatives
    %Ix = conv2(frame1,[1 -1],'same');
    %Iy = conv2(frame1,[1; -1],'same');
    %It = frame2 - frame1;

end

