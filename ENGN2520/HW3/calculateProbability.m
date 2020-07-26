function [probability] = calculateProbability(data,model)
    result1 = model.^data;
    model = 1-model;
    data = 1-data;
    result2 = model.^data;
    result = result1.*result2;
    probability = prod(result);  
end

