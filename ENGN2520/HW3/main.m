load 'digits';
models = zeros(10,784);

%% Train model for each digit
for i = 1:10
    traindata = sprintf('%s%d','train',i-1);
    models(i,:) = trainModelForDigit(eval(traindata));
end
%% Draw the visualization of the models
for i = 1:10
    subplot(2,5,i);
    imagesc(reshape(models(i,:),28,28)');
end

%% Classify each testing set
confusion = zeros(10,10);
correct = 0;

for i = 1:10
    testdata = sprintf('%s%d','test',i-1);
    confusion(i,:) = classifyDigit(eval(testdata),models);
    
    correct = correct + confusion(i,i);
end
    
    
    

