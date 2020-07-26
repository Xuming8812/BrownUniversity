function [matchMatrix] = MatchHarris(I1,I2,ratio)
        
    % extract Harris keypoints
    points1 = detectHarrisFeatures(I1);
    points2 = detectHarrisFeatures(I2);
    
    [f1,vpts1] = extractFeatures(I1,points1);
    [f2,vpts2] = extractFeatures(I2,points2);
    
    %get matches
    indexPairs = matchFeatures(f1,f2) ;
    matchedPoints1 = vpts1(indexPairs(:,1));
    matchedPoints2 = vpts2(indexPairs(:,2));
    
    %get matched coordinates 
    f1_matched = transpose(matchedPoints1.Location);
    f2_matched = transpose(matchedPoints2.Location);
    
    %save the matches into one matrix for RANSAC function
    matchNum = size(indexPairs,1);

    matchMatrix = zeros(3,matchNum,2);
    
    %padding 1 under the coordinate for further tranlation calculation
    matchMatrix(:,:,1) = [f1_matched(1,:);f1_matched(2,:);ones(1,matchNum)];
    matchMatrix(:,:,2) = [f2_matched(1,:);f2_matched(2,:);ones(1,matchNum)];  
end

