%loal data
load Xtrain
load Ytrain

%plot showing the training data and degree 2 polynomial estimated from the
%data
w1 = solveW(Xtrain,Ytrain,4);
w2 = solveWByLinearProgramming(Xtrain,Ytrain,4);
scatter(Xtrain,Ytrain,'DisplayName','training data'); 
hold on;
x = 0:0.01:1;
x = x';
fx1 = calculateFxByGivingW(x,w1);
fx2 = calculateFxByGivingW(x,w2);
plot(x,fx1,'b--','DisplayName','least square');
plot(x,fx2,'DisplayName','least absolute');
legend;

