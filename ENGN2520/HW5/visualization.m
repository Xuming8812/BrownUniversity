function [] = visualization(data,K,mu,sigma)
    figure
    hold on
    %plot the training data
    scatter(data(:,1), data(:,2))
    maxValue = max(data, [], 1) + 1;
    minValue = min(data, [], 1) - 1;
    x1 = minValue(1) :.2: maxValue(1);
    x2 = minValue(2) :.2: maxValue(2);
    [X1,X2] = meshgrid(x1,x2);
    X = [X1(:) X2(:)];
    for k = 1:K    
        y = mvnpdf(X,   mu(k,:), squeeze(sigma(k,:,:)));
        y = reshape(y,length(x2),length(x1));
        contour(x1 ,x2 ,y ,[0.0001 0.001 0.01 0.05 0.15 0.25 0.35]);
    end  
end

