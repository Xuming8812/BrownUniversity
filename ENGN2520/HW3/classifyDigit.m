function [classifyResult] = classifyDigit(testData,models)
    %initialization
    [dataCount,~] = size(testData); 
    result = zeros(dataCount,10);  
    classifyResult = zeros(1,10);
    
    %loop all testing data
    for row = 1:dataCount
        %loop each class to calculate probability
        for col =  1:10
            result(row,col) = calculateProbability(testData(row,:),models(col,:));
        end
        %find the max value and index of the probability
        [~, index] = max(result(row,:));
        
        %classify
        classifyResult(1,index) = classifyResult(1,index) + 1;
    end
end

