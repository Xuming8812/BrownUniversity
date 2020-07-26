function [finalHomographyMatrix] = RANSAC(matchMatrix,pointNum,iterations,threshold)
    %rng('shuffle')
    %set initial values
    finalHomographyMatrix = [0 0 0;0 0 0;0 0 0];
    maxInliers = 0;
    
    for i = 1:iterations 
        %get the length of the matching matrix
        matchNum = size(matchMatrix, 2);

        %get four index randomly
        selectIndex = randperm(matchNum, pointNum); 
        points1 = matchMatrix(:,selectIndex,1);
        points2 = matchMatrix(:,selectIndex,2);
             
        %create matrix A and b
        A = double (zeros(2*pointNum,2*pointNum));
        b = double (zeros(2*pointNum, 1));   
        %set the equation for each row
        for j = 1:pointNum
            A(2*j-1,:) = [points2(1,j) points2(2,j) 1.0 0 0 0 -points2(1,j)*points1(1,j) -points2(2,j)*points1(1,j)];
            A(2*j,:)   = [0 0 0 points2(1,j) points2(2,j) 1.0 -points2(1,j)*points1(2,j) -points2(2,j)*points1(2,j)];
            b(2*j-1) = points1(1,j);
            b(2*j)   = points1(2,j);
        end
        
        %solve the equation
        tanslate = A \ b;
               
        %get the current homography matrix
        homographyMatrix = [tanslate(1) tanslate(2) tanslate(3); tanslate(4) tanslate(5) tanslate(6); tanslate(7) tanslate(8) 1];
        %estimate the candidates
        
        estimate = HomographyTranform(matchMatrix(:,:,2),homographyMatrix);
        %get the norm of the translation vecter
        distance = (matchMatrix(:,:,1) - estimate).^2;
        distance = sum(distance);       
        %find matches with norm smaller than threshold
        inliners = find(distance<threshold);
        
        %count the good match
        inlinerNum = size(inliners,2);
        
        %save the maxInliner number and homographyMatrix
        if inlinerNum>maxInliers
            maxInliers = inlinerNum;
            finalHomographyMatrix = homographyMatrix;
        end           
    end
end



