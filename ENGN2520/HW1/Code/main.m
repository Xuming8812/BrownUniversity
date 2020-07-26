%loal data
load Xtrain
load Ytrain

%plot showing the training data and degree 3 polynomial estimated from the
%data
w = solveW(Xtrain,Ytrain,2);
scatter(Xtrain,Ytrain); hold on;
x = 0:0.01:1;
x = x';
fx = calculateFxByGivingW(x,w);
plot(x,fx);

%plot showing the training data and degree 10 polynomial estimated from the
%data
w = solveW(Xtrain,Ytrain,4);
scatter(Xtrain,Ytrain); hold on;
x = 0:0.01:1;
x = x';
fx = calculateFxByGivingW(x,w);
plot(x,fx);