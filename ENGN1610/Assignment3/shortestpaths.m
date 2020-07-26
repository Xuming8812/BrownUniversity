function [dist,prev] = shortestpaths(E, s, k);
    
    %get the length of set of Edges£¬actually is the number of vectexes
    n = size(E,1);  
    
    %a max value
    infinity = 1e10;
    
    %distance vector for each vertex in graph
    dist = infinity*ones(n,1);
    
    %path for the shortest path
    prev = zeros(n,1);
    
    
    dist(s) = 0;
    
    
    for t = 1:k
        
        %loop all vertexes
        for v = 1:n
            
            %loop all adjacent neighbours
            for j = 1:size(E{v},1)
                %u is the index of neighbouring vertex
                u = E{v}(j,1);
                %w is the weight of the edge connecting current 
                w = E{v}(j,2);
                if dist(v)+w < dist(u)
                    dist(u) = dist(v)+w;
                    prev(u) = v;
                end                
            end
        end
    end
end
