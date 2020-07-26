%use the given homography matrix to transform coordinate
function [transformedMatrix] = HomographyTranform(matrix,homographyMatrix)
    
    %get the size of the input coordinate matrix
    [rowNum, colNum] = size(matrix);
    matrix = double(matrix);
    %transform the matrix by left multiplying it by homographyMatrix
    transformedMatrix = homographyMatrix*matrix;
    
    %get the scales
    scales = transformedMatrix(3,:);
    
    %divide x and y coordinates by corresponding scale to get homogenous
    %matrix back
    transformedMatrix = [transformedMatrix(1,:)./scales; transformedMatrix(2,:)./scales;ones(1,colNum)];
    
end

