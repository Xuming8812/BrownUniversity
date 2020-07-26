function [E, G] = LossAndGradient(W, X, Y, C)

prod = X * W;
prod_hat = prod;
[m, n] = size(prod);
ind = sub2ind([m, n], (1 : m)', Y + 1);
prod_hat(ind) = -Inf;
[max_val, y_hat] = max(prod_hat, [], 2);
L = max_val - prod(ind) + 1;
L_mask = (L >= 0);
L = L .* L_mask;
E = 0.5 * sum(sum(W.^2)) + C * sum(L);

% Compute gradient
G = W;
for i = find(L ~= 0)
        y = Y(i);
        G(:, y + 1) = G(:, y + 1) - C * X(i, :)';
        G(:, y_hat(i)) = G(:, y_hat(i)) + C * X(i, :)';
end