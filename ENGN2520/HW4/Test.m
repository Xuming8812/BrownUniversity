function [acc, classification_map] = Test(W, NUM_CLASSES, NUM_SAMPLES)

load('digits');
classification_map = zeros(NUM_CLASSES, NUM_CLASSES);
for i = 1 : NUM_CLASSES
    data = [ones(NUM_SAMPLES,1), eval(['test' num2str(i-1)])];
    prob_map = data * W;
    [~, predicted] = max(prob_map, [], 2);
    predicted = predicted - 1;
    for j = 1 : NUM_CLASSES
        classification_map(i,j) = sum(predicted == j-1);
    end
end

acc = sum(sum((eye(NUM_CLASSES) .* classification_map))) / (NUM_CLASSES * NUM_SAMPLES);