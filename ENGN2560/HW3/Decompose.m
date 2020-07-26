function [R,T] = Decompose(E,K,bestInliers)

    %use SVD method to decompose
    [U,S,V] = svd(E);
        
    X = [0,-1,0;1,0,0;0,0,1];
    
    Rs = zeros(3,3,2);
    %get two possible R
    Rs(:,:,1) = U*X'*V';
    Rs(:,:,2) = U*X*V';

    %calculate T
    TT = 1/2 * trace(E * E')* eye(3)- E * E';
    
    for i = 1:3
        TT(i,:) = TT(i,:) / sqrt(TT(i,i));
    end
    
    Ts = zeros(3,1,2);
    %get two possible T
    Ts(:,:,1) = TT(1,:)';
    Ts(:,:,2) = -TT(1,:)';
        
    matchNum = size(bestInliers, 2);
        
    maxCount = 0;
    
    %turn pixel to metric unit
    gamma = K^-1*bestInliers(:,:,1);
    gammaBar = K^-1*bestInliers(:,:,2);
    
    
    for i = 1:2
        for j = 1:2
            count = 0;
            
            R0 = Rs(:,:,i);
            T0 = Ts(:,:,j);
            
            %loop every inliers
            for k = 1:matchNum
                
                p1 = gamma(:,k);
                p2 = gammaBar(:,k); 
                
                %solve for rho
                p = [p2, - R0 * p1];
                rho = p \ T0;
                
                %count the number of both positive
                if(rho(1)>0 && rho(2)>0)
                    count = count+1;
                end
            end
            
            %save for R and T
            if count>maxCount
               R = R0;
               T = T0;
               maxCount = count;
            end
            
        end
    end
end

