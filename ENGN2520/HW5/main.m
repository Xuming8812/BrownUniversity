clc;clear;
numIterations = 20;
tolForInteration = 1e-7;
thresholdForCovMatrix = 1;
%% 2 Gaussian
load data2;
K = 2;
[mu, sigma,pi,likelyhood] = EM_Algorithm(data, K, numIterations, tolForInteration, thresholdForCovMatrix);
pi
for i = 1:K
   mu(i,:)
   squeeze(sigma(i,:,:))
end
plot(likelyhood)
title('log-likelihood over time')
xlabel('iteration')
ylabel('log-likelihood ')
visualization(data, K, mu , sigma); 

%% 3 Gaussian
load data3;
K = 3;
[mu, sigma,pi,likelyhood] = EM_Algorithm(data, K, numIterations, tolForInteration, thresholdForCovMatrix);
pi
for i = 1:K
   mu(i,:)
   squeeze(sigma(i,:,:))
end
plot(likelyhood)
title('log-likelihood over time')
xlabel('iteration')
ylabel('log-likelihood ')
visualization(data, K, mu , sigma);  