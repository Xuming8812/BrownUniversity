function [matchMatrix] = MatchFeatures(I1,I2)
%turn the input image to single precision
    J1 = single(I1);
    J2 = single(I2);
    
    %get SIFT features

    [f1,d1] = vl_sift(J1);
    [f2,d2] = vl_sift(J2);

    %call vl_ubcmatch to match features
    [matches, scores] = vl_ubcmatch(d1, d2,2);


    %get matched frames 
    f1_matched = f1(:,matches(1,:));
    f2_matched = f2(:,matches(2,:));
    
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
    matchNum = size(matches,2);

    matchMatrix = zeros(3,matchNum,2);
    
    %padding 1 under the coordinate for further tranlation calculation
    matchMatrix(:,:,1) = [f1_matched(1,:);f1_matched(2,:);ones(1,matchNum)];
    matchMatrix(:,:,2) = [f2_matched(1,:);f2_matched(2,:);ones(1,matchNum)]; 
end

