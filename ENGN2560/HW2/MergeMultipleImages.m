function [newImage] = MergeMultipleImages(images,params)
    numImages = size(images,1);
    
    %merge first two images
    newImage = MergeImages(images{1},images{2},params);

    %merge other images into the newly generated image
    for i = 3: numImages
        newImage = MergeImages(newImage,images{i},params);
        %imshow(newImage)
    end
    
end

