
%% Preprocess dataset
clear;clc;
load('digits');
x = []; 
y = [];
for i = 1 : 10
    x = [x; ones(500,1), eval(['train' num2str(i-1)])];
    y = [y; ones(500,1) * i];
end
%% Objective function value vs iteration time
r = 0.1;
T = 1000;
C = 0.01;
[w,Loss] = gradientDescent(x,y,C,r,T);
plot(Loss);  
xlabel('Iteration');
ylabel('Objection function value');

%% Do experiments of different values of C and find minimum classification erros
figure();
hold on;
acc_max = 0;
C = [0.0001,0.001,0.01, 0.1, 1, 10, 100];
r = 0.1;
T = 1000;
for i = 1 : size(C, 2)
    [w,Loss] = gradientDescent(x,y,C(i),r,T);
    
    [acc, classification_map] = Test(w, 10, 500);
    fprintf('C = %f, accuracy = %f \n', C(i), acc);
    if acc > acc_max
        acc_max = acc;
        c_best = C(i);
        W_best = w;
        result = classification_map;
    end
end
%% Visualize W
figure();
for i = 1 : 10
    subplot(2,5,i);
    w_i = normalize(W_best(2 : end, i), 'range');
    imagesc(reshape(w_i,28,28)');
end