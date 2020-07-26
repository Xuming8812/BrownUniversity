function [maxMU,maxSigma,maxPI,likelyhood] = EM_Algorithm(data, K, numIterations , tolForInteration ,thresholdForCovMatrix)
    %get dimension of input training data;    
    [N,D] = size(data);
    %initialization
    maxLikelyhood = -inf;
    
    %iterate for certain times
    for i = 1:numIterations   
       %set initial values for mu, pi, sigma of this iteration
       %initialize mu by randomly selecting K data points
       mu = data(randsample(N, K), :);
       %initialize sigma by using  the overall data covariance.
       sigma = reshape(cov(data),1,D,D);
       sigma = repmat(sigma, K, 1, 1);
       pi = ones(1,K) / K;  
       %calculate the initial value of log-likelyhood
       lastLikelyhood = -inf;
       currentLikelyhood = sum(log(probabilityCalculation(data, K, mu , sigma) * pi'));
       allLikelyhoods = currentLikelyhood;
       %loop until likelyhood becomes stable
       while currentLikelyhood - lastLikelyhood > tolForInteration 
           lastLikelyhood = currentLikelyhood;   
           prob = probabilityCalculation( data, K, mu , sigma).*pi;
           %calculate rj and Nj
           rj = prob./sum(prob,2);
           Nj = sum(rj , 1);
           %calculate mu
           mu = (rj'*data)./(Nj');
           %calculate sigma          
           for j = 1:K
                X_mu = data-repmat(mu(j,:),N,1);
                sigmaJ = (rj(:,j).*X_mu)'*X_mu;
                sigmaJ = sigmaJ/Nj(j);
                for d = 1:D
                    sigmaJ(d,d) = max(sigmaJ(d,d), thresholdForCovMatrix);
                end
                sigma(j, :, :) = sigmaJ;
           end         
           %caculate pi
           pi = Nj/N;
           %update likelyhood
           currentLikelyhood = sum(log(probabilityCalculation(data, K, mu, sigma) * pi'));
           %save current likelyhood
           allLikelyhoods = [allLikelyhoods,currentLikelyhood];
       end
       
       %save the best likelyhood ever have
       if currentLikelyhood>maxLikelyhood && currentLikelyhood<-1000
           maxLikelyhood = currentLikelyhood ;
           maxMU = mu;
           maxSigma = sigma;
           maxPI = pi;
           likelyhood = allLikelyhoods;     
       end
    end
end

