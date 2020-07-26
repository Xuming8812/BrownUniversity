function [] = DrawPointAndLine(I1,I2,E,K)
%DRAWPOINTANDLINE Summary of this function goes here
%   Detailed explanation goes here
    K1 = inv(K)';
    K2 = inv(K);

    F = K1*E*K2;
    
    point1 = [1832;1090;1];
    %get the corresponding line
    line1 = F*point1;
    b1 = -line1(3)/line1(2);
    k1 = -line1(1)/line1(2);
    x = [0,3072];
    y1 = k1*x+b1;
    
    %pick two points from the epipolar line
    xBar = [1000,2000];
    yBar = k1*xBar+b1;
    
    pointBar1 = [xBar(1),yBar(1),1];
    pointBar2 = [xBar(2),yBar(2),1];
    
    line2 = pointBar1 * F;
    line3 = pointBar2 * F;
    
    b2 = -line2(3)/line2(2);
    k2 = -line2(1)/line2(2);
    
    b3 = -line3(3)/line3(2);
    k3 = -line3(1)/line3(2);
    
    y2 = k2*x+b2;
    y3 = k3*x+b3; 
    %draw a point on image1
    imshow(I1);
    hold on
    plot(point1(1),point1(2),'r*');
    line(x,y2,'Color','blue');
    line(x,y3,'Color','blue');
    
    %draw the corresponding epipolar line
    figure;
    imshow(I2);
    hold on;
    line(x,y1,'Color','red');
    plot(xBar(1),yBar(1),'r*');
    plot(xBar(2),yBar(2),'r*');
  
end

