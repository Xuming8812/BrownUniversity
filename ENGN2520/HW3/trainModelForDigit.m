function [model] = trainModelForDigit(trainSet)
    [rowNum, ~] = size(trainSet);
    model = sum(trainSet)/rowNum;
end

