function [matches] = MatchDescriptor(d1, d2,ratio)

    %get length of input d1 and d2
    sizeD1 = size(d1,2);
    sizeD2 = size(d2,2);
    
    rowNum = size(d1,1);
       
    matches=[];
    
    %loop all descriptor from d1
    for i = 1:sizeD1
        %copy d2
        currentD2 = d2;
        %get the current column(descriptor) of d1
        newD1 = d1(:,i);
        %duplicate this column to gain a matrix
        newD1 = repmat(newD1,1,sizeD2);
        
        %calculate the distance from each descriptor of d2 to this
        %descriptor from d1
        distance = (currentD2-newD1).^2;
        distance = sum(distance);
        
        %find the smallest distance
        [minValue,minIndex] = min(distance);
        %delete smallest distance to find second smallest
        distance(minIndex) = [];
        [secondMinValue,SecondMinIndex] = min(distance);
        
        %the smallest distance should be smaller than second smallest value
        %multiplied by a given ratio
        if minValue<secondMinValue*ratio 
            %add the current match to results
            result = [i;minIndex];
            matches = [matches,result];
            %update the corresponding column in d2 so that no other
            %features can match this one            
            d2(1:rowNum,minIndex) = 255;            
        end      
    end
end

