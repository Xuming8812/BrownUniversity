function [Ew,gradientEw] = calculateEw(w,x,y,C)
    %k classes
    [~,k] = size(w);
    %n training datas
    [n,~] = size(x);
    %initialization
    Ew = 0; 
    gradientEw = w;
    
    %loop all training datas
    for index = 1:n
        temp = x(index,:)*w;
        y_train = y(index,1);
        
        %find yhat, make sure yhat = argmax(temp) where yhat!=y
        temp(y_train) = -Inf;
        [~,y_hat] = max(temp);
        
        %calculate w_y_x and w_y_hat_t       
        w_y_x = x(index,:)*w(:,y_train);
        w_y_hat_x = x(index,:)*w(:,y_hat);
        
        if w_y_x<w_y_hat_x+1
            %update E
            Ew = Ew+C*(w_y_hat_x+1-w_y_x);  
            %update gradient E
            gradientEw(:,y_hat) = gradientEw(:,y_hat) + C*x(index,:)';
            gradientEw(:,y_train) = gradientEw(:,y_train)-C*x(index,:)';
        end
    end
    
    for i = 1 : k
        Ew = Ew + w(i,:)*w(i,:)'/2;
    end
end

