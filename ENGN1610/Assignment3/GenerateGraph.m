function [E] = GenerateGraph(I,J,mode)
    %Function :     GenerateGraph
    %Description:   Generate the adjacent matrix based on the input image
    %                       and the gradient matrix
    %Input:         I----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %:              J----Type: matrix of integers; Meaning: the matrix
    %                       based on which to calculate the weight of edges
    %               mode-Type:int; Meaning: determine how to calculate the
    %                       weight of an edge, if mode == 0, then the edge
    %                       is encouraged to go along the boundary where 
    %                       pixel has high gradient magnitude;else, the edge
    %                       is encouraged to go through pixels which has low 
    %                       gradient magnitude
    %Output:        E----Type: cell of matrices; Meaning: the adjacent
    %                       matrix standing for the graph, E{v} is the set
    %                       of the edges starting from the v th vertex,
    %                       E{v}(i,1) is the i th neighbor `s vertex index
    %                       E{v}(i,2) is the weight of the edge between v
    %                       and i

    %calculate size of matrix I
    [rowNum_I,colNum_I] = size(I);
    
    %determine how to calculate weight of a edge based on the given mode
    %parameter   
    if mode == 0
    %if mode == 0, the weight of edge is (J(y1,x1)-J(y2,x2))^(-2), the edge
    %is encouraged to go along the boundary where pixel has high gradient magnitude
        order = -2;
    else
    %if mode == 1, the weight of edge is (J(y1,x1)-J(y2,x2))^2, the edge
    %is encouraged to go through pixels which has low gradient magnitude
        order = 2;
    end
    
    %a matrix to store the direction of neighbours, direction(m,1) is the
    %row offset, direction(m,2) is the column offset
    direction = [-1,-1;-1,0;-1,1;0,-1;0,1;1,-1;1,0;1,1];
    
    %get the size of the direction code, instead of using number 4 or 8
    %directly in code    
    [rowNum_D,colNum_D] = size(direction);
    
    %initialize the cell to store the edges
    E = cell(rowNum_I*colNum_I,1);
    
    
    %traversal each pixel in I to calculate its edges, the weighting can be
    %determined by the gradient magnitude of each point of a vertex
    for i = 1:rowNum_I
        for j = 1:colNum_I
            
            %transform the pixel position to vertex index
            cellIndex = (i-1)*rowNum_I+j;
            
            %initialize the index of neighbouring vertex for the current
            %vertex
            vertexIndex = 1;
            
            %traversal all directions to all those neighbouring vertexes to
            %adjacent list
            for m =  1:rowNum_D
                %get the row and col number of current neighbouring vertex
                row = direction(m,1)+i;
                col = direction(m,2)+j;
                
                %if the neigh
                if row>0 && row<=rowNum_I && col>0 && col<=colNum_I
                    
                    %transform the pixel position to vertex index
                    neighbourIndex = (row-1)*rowNum_I+col;
                    
                    %calculate the weight of the edge between current
                    %vertex and its current neighbour vertex
                    neighbourWeight = (J(row,col)-J(i,j))^order;
                    
                    E{cellIndex}(vertexIndex,1) = neighbourIndex;
                    E{cellIndex}(vertexIndex,2) = neighbourWeight;
                    
                    %increase the neighour index for next neighbour vertex
                    vertexIndex = vertexIndex+1;
                end               
            end
        end
    end
end

