function [ ] = plot_GMM( X, mu, sigma )
    %Function to visualize mixture model after
    % fitting with the EM algorithm
    %
    % X: Input data (N x D)
    % mu: Component means (K x D)
    % sigma: Component covariances (K x D x D)
    figure
    hold on
    %Plot the dataset
    scatter(X(:,1), X(:,2))
    %Setup plot boundaries
    maxes = max(X, [], 1) + 1;
    mins = min(X, [], 1) - 1;
    %Grid for contour plots
    x1 = mins (1) :.2: maxes (1);
    x2 = mins (2) :.2: maxes (2);
    [X1,X2] = meshgrid(x1,x2);
    %For each component distribution make a contour
    % plot of the Guassian pdf
    K = size(mu, 1);
    for k = 1:K
        
        y = mvnpdf([X1(:) X2(:)],mu(k,:), squeeze(sigma(k,:,:)));
        y = reshape(y,length(x2),length(x1));
        contour(x1 ,x2 ,y ,[.0001 .001 .01 .05:.1:.95 .99 .999 .9999]);
    end
    title('Visualization of fitted mixture components ')
    hold off
end

