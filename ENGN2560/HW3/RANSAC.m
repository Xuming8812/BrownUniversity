function [essentialMatrix,bestInliers] = RANSAC(matchMatrix,K,iterations,threshold)
%UNTITLED Summary of this function goes here


    maxInliers = 0;
    
    matchNum = size(matchMatrix, 2);
    
    K1 = inv(K');
    K2 = inv(K);
    
    for i = 1 : iterations

        selectIndex = randperm(matchNum, 5); 
        points1 = matchMatrix(1:2,selectIndex,1);
        points2 = matchMatrix(1:2,selectIndex,2);
        
        roots = ComputeEssentialMatrix(points1, points2, K);
        
        for j = 1 : size(roots,3)
            E = roots{1,1,j};
            
            F = K1 * E * K2;
            
            gamma = matchMatrix(:,:,1);
            gammaBar = matchMatrix(:,:,2);
            
            epipolarLines = F * gamma;
            
            distance = abs(sum(epipolarLines .* gammaBar));
            scale = sqrt(epipolarLines(1,:).^2 + epipolarLines(2,:).^2);
            
            distance = distance./scale;
            inliers = find(distance < threshold);
            
            inlierNum = size(inliers,2);
            
            
            if inlierNum > maxInliers
                maxInliers = inlierNum;
                essentialMatrix = E;
                bestInliers = matchMatrix(:,inliers,:);
            end
        end
    end
        
%     for i = 1:iterations 
%         selectIndex = randperm(matchNum, 5); 
%                
%         points1 = f1(1:2,matches(1,selectIndex));
%         points2 = f2(1:2,matches(2,selectIndex));
%         
%         roots = ComputeEssentialMatrix(points1,points2,K);
%         
%         for j = 1:size(roots,3)
%             E0 = roots{j};
%             
%             F = K1 * E0 * K2;
%             
%             s = [f1(1,matches(1,:));f1(1,matches(1,:));ones(1,matchNum)];
%             t = [f2(1,matches(2,:));f2(2,matches(2,:));ones(1,matchNum)];
%             
%             s_ = F*s;
%             
%             distance = abs(sum(s_ .* t)) ./ sqrt(s_(1,:).^2+s_(2,:).^2);
%             
%             inliers = find(distance<=threshold);
%             
%             count = size(inliers,2);
%             
%             if count>maxInliers
%                 maxInliers = count;
%                 essentialMatrix = E0;
%                 bestInliers = inliers;
%             end
%                        
%         end
%         
%         %get the length of the matching matrix
%         
%         %get four index randomly
% %         selectIndex = randperm(matchNum, 5); 
% %         points1 = matches(1:2,selectIndex,1);
% %         points2 = matches(1:2,selectIndex,2);
% %         %calculate essential matrix by calling given function
% %         roots = ComputeEssentialMatrix(points1,points2,K);
% %         %get the number of possible roots
% %         sizeE = size(roots,3);
% %         
% %         %loop all roots to find best essential matrix
% %         for j = 1:sizeE
% %             %get current E
% %             E = roots{1,1,j};
% %             
% %             F = K1*E*K2;
% %             
% %             epipolarLines = F*matches(:,:,1);
% %             %calculate reprojection error
% %             distance = abs(sum(epipolarLines.*matches(:,:,2)));
% %             
% %             scale = epipolarLines(1:2,:);
% %             
% %             scale = sum(scale.^2);
% %             scale = sqrt(scale);
% %             
% %             distance = distance./scale;
% %             
% %             inliers = find(distance<=threshold);
% %         
% %             %count the good match
% %             inlierNum = size(inliers,2);
% % 
% %             %save the maxInliner number and homographyMatrix
% %             if inlierNum>maxInliers
% %                 maxInliers = inlierNum;
% %                 essentialMatrix = E;
% %                 bestInliers = inliers;
% %             end    
% %             
% %            
% %         end    
%     end
end

