function [prev] = DijkstraShortestPaths(E, s)
    %Function :     DijkstraShortestPaths
    %Description:   Calculate the shortest path starting from the given
    %               vertex
    %Input:         E------Type: cell of matrix; Meaning: the adjacent matrix of the
    %                       graph.E{v} is the set of the edges starting from the v th vertex,                    
    %                       E{v}(i,1) is the i th neighbor `s vertex index
    %                       E{v}(i,2) is the weight of the edge between v
    %                       and i
    %               s------Type:int; Meaning: the index of the starting vertex 
    %Output:        prev---Type:vecotr of integer; Meaning: vector storing
    %                       the shortest path from given vertex s

    %get the length of set of Edges£¬actually is the number of vectexes
    n = size(E,1);  
    
    %a max value
    infinity = 1e10;
    
    %distance vector for each vertex in graph
    dist = infinity*ones(n,1);
    
    %path for the shortest path
    prev = zeros(n,1);
    
    %a array to store whether the vertex has been visited
    visited = zeros(n,1);
    visited(s) = 1;
    
    %set the start vertex in dist array by 0, other vertexes by infinite.
    dist(s) = 0;
    
    %count how many vertexes have been visited
    count = 0;

    %start with the given starting vertex
    current =s;
    %loop until all vertexes are visited
   while count<n
              
       min = 1e10;
       %find the vertex which distance has been changed from last iteration but has not been visited 
       for i=1:n
          if visited(i) == 0 && dist(i) < min
              min = dist(i);
              current = i;
          end                       
       end
       
       %mark this current vertex as visited
       visited(current) = 1;
       %increase the count buffer
       count = count+1;
       %loop all the neighboring vertex      
       for j = 1:size(E{current},1)         
            %u is the index of neighbouring vertex
            u = E{current}(j,1);
            %w is the weight of the edge connecting current 
            w = E{current}(j,2);            
            %find the nearest neighbor
           if visited(u) == 0 && dist(current)+ w<dist(u)
              dist(u) =  dist(current)+ w;              
              prev(u) = current;                          
           end
       end       
   end
    
end

