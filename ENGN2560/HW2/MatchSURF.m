function [matchMatrix] = MatchSURF(I1,I2,ratio)
        
    % extract SIFT keypoints
    points1 = detectSURFFeatures(I1);
    points2 = detectSURFFeatures(I2);
    
    [f1,vpts1] = extractFeatures(I1,points1);
    [f2,vpts2] = extractFeatures(I2,points2);
    
    %get matches
    indexPairs = matchFeatures(f1,f2) ;
    matchedPoints1 = vpts1(indexPairs(:,1));
    matchedPoints2 = vpts2(indexPairs(:,2));
    
    %get matched frames 
    f1_matched = transpose(matchedPoints1.Location);
    f2_matched = transpose(matchedPoints2.Location);
    
    %show matches
%     imshow(I1)
%     h1 = vl_plotframe(f1_matched) ;
%     set(h1,'color','g','linewidth',2) ;
% 
%     figure;
%     imshow(I2)
%     h2 = vl_plotframe(f2_matched) ;
%     set(h2,'color','g','linewidth',2) ;

    %save the matches into one matrix for RANSAC function
    matchNum = size(indexPairs,1);

    matchMatrix = zeros(3,matchNum,2);
    
    %padding 1 under the coordinate for further tranlation calculation
    matchMatrix(:,:,1) = [f1_matched(1,:);f1_matched(2,:);ones(1,matchNum)];
    matchMatrix(:,:,2) = [f2_matched(1,:);f2_matched(2,:);ones(1,matchNum)];  
end

