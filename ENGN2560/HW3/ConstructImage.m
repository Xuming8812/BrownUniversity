function [image] = ConstructImage(pointCloud,K,R,T,rowNum,colNum)

%calculate gamma matrix in pixel unit
gamma =double(K*(R*pointCloud.Location'+T)) ;
scale = gamma(3,:);
%transfer to pixel unit, actually divide by rho
gamma = [gamma(1,:)./scale;gamma(2,:)./scale;gamma(3,:)./scale];

%get the grid for the generated image
[x,y]=meshgrid(1:colNum,1:rowNum);

%the final rgb image
image = zeros(rowNum,colNum,3);

%loop three channels
for i= 1 : 3
    %get current channel
    chanel = double(pointCloud.Color(:,i));
    %arrange the 2D pixel matrix, column 1 is x coordinate, column 2 is y
    %coordinate, column 3 is intensity
    points = [gamma(1,:);gamma(2,:);chanel']';
    
    %call griddata to interpolate from sub pixels values to integer grid
    I = griddata(points(:,1),points(:,2),points(:,3),x,y); 
    
    %save the image in corresponding channel
    image(:,:,i) = I;
end

%type cast from double to uint8
image = uint8(image);
end

