function [newImage] = TransformImageWithBlending(image,homographyMatrix,referenceImage)
    %get the row number and column number fo the input image
    [rowNum, colNum] = size(image);
    [refRowNum, refColNum] = size(referenceImage);
    
    %get the boundary of the input image
    bounds = [1 rowNum 1 colNum];
    
    % homogeneous coordinates of the corners,note that the (x,y) = (col,row)
    corners = [bounds(3) bounds(4) bounds(4) bounds(3);bounds(1) bounds(1) bounds(2) bounds(2);1 1 1 1];
    
    %get the coordinates of the corners after tansforming by homography
    %matrix
    newCorners = round(transform(corners,homographyMatrix));
    
    %get the new boundaries,
    newBounds = [min(newCorners(2,:)) max(newCorners(2,:)) min(newCorners(1,:)) max(newCorners(1,:))];
    startRow = newBounds(1);
    endRow = newBounds(2);
    startCol = newBounds(3);
    endCol = newBounds(4);

%     %if mapping to a minus coordinate need to calcuate the offset
    if startRow<0
        offsetRow = 1-startRow;
    else
        offsetRow = 0;
    end
    
    if startCol <0
        offsetCol = 1-startCol;
    else
        offsetCol = 0;
    end
    
%     offsetRow = 1-startRow;
%     offsetCol = 1-startCol;
    %calculate the inverse matrix of the homography matrix for further
    %mapping from grid to the image
    inverseT = inv(homographyMatrix);
            
    %calculate the current row number and column number
    newRowNum = newBounds(2)-newBounds(1)+1;
    newColNum = newBounds(4)-newBounds(3)+1;
    
    %calculate the size big enough for two images
    gridRowNum = max([newBounds(2),newRowNum,refRowNum-startRow]);
    gridColNum = max([newBounds(4),newColNum,refColNum-startCol]);
      
    %declare the new image
    newImage = zeros(gridRowNum,gridColNum);
    
    %get the X and y coordinates of the new grid
    [newX,newY] = meshgrid(1:gridColNum,1:gridRowNum);
    
    %mapping the coordinate according to the previous offset to deal with
    %negative row indexes and column indexes
    newX = newX - offsetCol;
    newY = newY - offsetRow;
    
    %use the previous inverse homography matrix to mapping grid to the
    %input image
    coordinates = [newX(:)';newY(:)';ones(1,gridColNum*gridRowNum)];
    coordinates = transform(coordinates,inverseT);
    
    %reset the X and Y to mesh grid format
    newX = reshape(coordinates(1,:),gridRowNum,gridColNum);
    newY = reshape(coordinates(2,:),gridRowNum,gridColNum);
    
    %get the X and Y in mesh grid format for interpolation
    [oldX,oldY] = meshgrid(1:colNum,1:rowNum);
    
    %turn the image into double type for interpolation
    doubleImage = double(image);
   
    %interpolate, if the coordinate is out of boundary of the input image,
    %the value will be nan
    newImage = interp2(oldX,oldY,doubleImage,newX,newY);
    
    % replace all nans to zero
    newImage(isnan(newImage))=0;   
    %loop all pixels in the new grid
    
    %imagesc(newImage);
    referenceImage = double(referenceImage);
    
    for x = 1:gridColNum
       for y = 1:gridRowNum
           %mapping the coordinate according to the previous offset to deal with
           %negative row indexes and column indexes
           xCoor = x-offsetCol;
           yCoor = y-offsetRow;

           %if the pixel is in the other image 
           if xCoor>=1 && xCoor<refColNum && yCoor>=1 && yCoor<refRowNum
               %if current pixel is zero, means mapping to only one image
               if newImage(y,x) == 0
                   newImage(y,x)= referenceImage(yCoor,xCoor);
               else
                   %if the pixel mapping to both images
                   
                   %the shortest distance to reference
                   distanceRef = min([xCoor,refColNum-xCoor,yCoor,refRowNum-yCoor]);
                   %the shortest distance to tranformed image
                   newCorners=newCorners(1:2,:);                  
                   d1 = getDistance(newCorners(:,1),newCorners(:,2),[x;y]);
                   d2 = getDistance(newCorners(:,2),newCorners(:,3),[x;y]);
                   d3 = getDistance(newCorners(:,4),newCorners(:,1),[x;y]);
                   d4 = getDistance(newCorners(:,3),newCorners(:,4),[x;y]);
                   
                   distanceImage = min([d1,d2,d3,d4]);
                   
                   intensityImage = newImage(y,x);
                   intensityRef = referenceImage(yCoor,xCoor);
                   
                   newIntensity = (intensityImage*distanceImage + intensityRef*distanceRef)/(distanceRef+distanceImage);
                                 
                   newImage(y,x) =  newIntensity;
               end
           end
       end
    
    end     
end

function d = getDistance(Q1,Q2,P)
    d = abs(det([Q2-Q1,P-Q1]))/norm(Q2-Q1);
end

%use the given homography matrix to transform coordinate
function [transformedMatrix] = transform(matrix,homographyMatrix)
    
    %get the size of the input coordinate matrix
    [rowNum, colNum] = size(matrix);

    %transform the matrix by left multiplying it by homographyMatrix
    transformedMatrix = homographyMatrix*matrix;
    
    %get the scales
    scales = transformedMatrix(3,:);
    
    %divide x and y coordinates by corresponding scale to get homogenous
    %matrix back
    transformedMatrix = [transformedMatrix(1,:)./scales; transformedMatrix(2,:)./scales;ones(1,colNum)];
    
end

