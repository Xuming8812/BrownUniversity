function [ptCloud] = Trianglation(I1,K,E,R,T,bestInliers,densificationFactor,threshold)
    %get the size of the image
    rowNum = size(I1,1);
    colNum = size(I1,2);
    %create mesh grid of the sampling grid
    [xg,yg] = meshgrid(1:densificationFactor:colNum,1:densificationFactor:rowNum);
    
    %get the size of the grid
    newRowNum = size(xg,2);
    newColNum = size(xg,1);
    
    %interpolate to get the corresponding coordinate of xg and yg in I1
    x = griddata(bestInliers(1,:,1)',bestInliers(2,:,1)',bestInliers(1,:,2)',xg,yg);
    y = griddata(bestInliers(1,:,1)',bestInliers(2,:,1)',bestInliers(2,:,2)',xg,yg);
    
    %interpolate to get the corresponding coordinate of xg and yg in I2
    xBar = griddata(bestInliers(1,:,2)',bestInliers(2,:,2)',bestInliers(1,:,1)',xg,yg);
    yBar = griddata(bestInliers(1,:,2)',bestInliers(2,:,2)',bestInliers(2,:,1)',xg,yg);
    
    %transfer the coordinate in to homogenous M X 3 matrix from I1 to I2
    gamma = [xg(:)';yg(:)';ones(1,newRowNum*newColNum)];
    gammaBar = [x(:)';y(:)';ones(1,newRowNum*newColNum)];
    
    %transfer the coordinate in to homogenous M X 3 matrix from I2 to I1
    gammaPrime = [xBar(:)';yBar(:)';ones(1,newRowNum*newColNum)];
    gammaBarPrime = [xg(:)';yg(:)';ones(1,newRowNum*newColNum)]';
    
    %caculate fundamental matrix
    K1 = inv(K)';
    K2 = inv(K);
    F = K1*E*K2;
    
    %calculate the distance of gammarBar to epipolar lines in I2
    epipolarLines = F * gamma;
    distance = abs(sum(epipolarLines.*gammaBar));
    scale = sqrt(epipolarLines(1,:).^2 + epipolarLines(2,:).^2);

    distance = distance./scale;
    inliers = find(distance < threshold);
    
    %calculate the distance of gammaPrime to epipolar lines in I1
    epipolarLinesBar = gammaBarPrime * F;    
    epipolarLinesBar = epipolarLinesBar';
 
    distance = abs(sum(epipolarLinesBar.*gammaPrime));
    scale = sqrt(epipolarLinesBar(1,:).^2 + epipolarLinesBar(2,:).^2);
    
    distance = distance./scale;
    
    inliersBar = find(distance < threshold);
    
    %get intersect between bidirection correspondings
    inliers = intersect(inliers,inliersBar);
    
    %get good matches   
    gammarMatched = gamma(:,inliers);
    gammarBarMatched = gammaBar(:,inliers);
    
    %turn pixel unit to metric
    gammaCamera = K^-1 * gammarMatched;
    gammaBarCamera = K^-1 * gammarBarMatched;
    
    %get total number of matches
    numMatched = size(gammarMatched,2);
    
    %points = gammaCamera;
    
   points = zeros(3,numMatched);
    %calculate p for each point from I1
    for i = 1: numMatched
        p2 = gammaBarCamera(:,i);
        p1 = gammaCamera(:,i);
        p = [p2,-R*p1];
        rho = p \ T;
        
        points(:,i) = rho(2)*gammaCamera(:,i);
    end
     
    %get color from input image
    colors = zeros(numMatched,3);
    colors = uint8(colors);

    for i = 1:numMatched
       colors(i,1) = I1(gammarMatched(2,i),gammarMatched(1,i),1);
       colors(i,2) = I1(gammarMatched(2,i),gammarMatched(1,i),2);
       colors(i,3) = I1(gammarMatched(2,i),gammarMatched(1,i),3);
    end

    %create pointCloud based on 3d coordinates and color infomation
    ptCloud = pointCloud(points','Color',colors);    
end

