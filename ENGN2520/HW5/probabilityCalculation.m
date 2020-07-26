function [prob] = probabilityCalculation(X,K,mu,sigma)
    [N,~] = size(X);
    prob = zeros(N, K);
    for j = 1:K
        prob(:, j) = mvnpdf(X, mu(j,:), squeeze(sigma(j,:,:)));
    end
end

