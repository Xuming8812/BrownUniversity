function [tranformedImage] = MergeImages(I1,I2,params)
    %check if input is rgb format
    if (size(I1, 3) == 3)&&(size(I2, 3) == 3)
        channels = size(I1, 3);
              
        img1 = I1(:,:,1);
        img2 = I2(:,:,1);       
        
        %determine which kind of features will be used 
        if params.featureType == "Harris"
            matchMatrix = MatchHarris(img1,img2,params.ratioTestRatio);
        elseif params.featureType == "SURF"
            matchMatrix = MatchSURF(img1,img2,params.ratioTestRatio);
        else
            matchMatrix = Match(img1,img2,params.ratioTestRatio);
        end
                      
        %calculate the homographyMatrix
        homographyMatrix = RANSAC(matchMatrix,4,params.RANSACIterations,params.RANSACInlierDistanceThreshold);
        
        %need blending or not
        if params.isBlending == 1
            channel1 = TransformImageWithBlending(img2,homographyMatrix,img1);
        else
            channel1 = TransformImage(img2,homographyMatrix,img1);
        end
        
        %get the new size of merged image
        [newRowSize,newColSize] = size(channel1);
        
        %initialize the final result
        tranformedImage = zeros(newRowSize,newColSize,channels);
        
        tranformedImage(:,:,1) = channel1;
        
        %deal with each channel
        for i = 2:channels
            img1 = I1(:,:,i);
            img2 = I2(:,:,i);
            
            if params.isBlending == 1
                tranformedImage(:,:,i) = TransformImageWithBlending(img2,homographyMatrix,img1);
            else
                tranformedImage(:,:,i) = TransformImage(img2,homographyMatrix,img1);
            end
        end
        
        tranformedImage = uint8(tranformedImage);
    else
       
        matchMatrix = Match(I1,I2,params.ratioTestRatio);
        
        %calculate the homographyMatrix
        homographyMatrix = RANSAC(matchMatrix,4,params.RANSACIterations,params.RANSACInlierDistanceThreshold);

        %need blending or not
        if params.isBlending == 1
            tranformedImage = TransformImageWithBlending(img2,homographyMatrix,img1);
        else
            tranformedImage = TransformImage(I2,homographyMatrix,I1);
        end
                      
        tranformedImage = uint8(tranformedImage);
    end  
end

