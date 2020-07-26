function [p] = CenterlineDetection(I,x1,y1,x2,y2)
    %Function :     CenterlineDetection
    %Description:   Calculate the centerline from (x1,y1) to (x2,y2) by calculating
    %               the shortest path between those two pixels.
    %Input:         I----Type: matrix of integers; Meaning: the input image
    %                       stored in a matrix
    %               x1---Type:int; Meaning: the x coordinate of the
    %                       starting pixel
    %               y1---Type:int; Meaning: the y coordinate of the
    %                       starting pixel
    %               x2---Type:int; Meaning: the x coordinate of the
    %                       ending pixel
    %               y2---Type:int; Meaning: the y coordinate of the
    %                       ending pixel
    %Output:        p----Type: vector of int; Meaning: the path from starting 
    %                       point to ending point      

    %open the given image and store the gray values in matrix I
    %I = imread(path);
    
     %calculate size of matrix I
    [rowNum_I,colNum_I] = size(I);
    
    %smooth the image with gaussian filter
    
    G1 = GaussianSmooth(I,1);
    G2 = GaussianSmooth(I,3);
    G = G1-G2;
    
    %G = GaussianSmooth(I,1);
    
    %calculate the gradient magnitude of each element of I and save it in
    %Matrix J
    J = GradientCalculation(G);
    
    %generate graph and its set of edges
    E = GenerateGraph(G,J,1);
    
    % set the value of k
    k = rowNum_I+colNum_I;
    
    %turn start pixel and end pixel to vertex index in graph
    s = (y1-1)*rowNum_I+x1;
    
    v = (y2-1)*rowNum_I+x2;
    
    %call the shortestpaths function to calculate shortest part taking at
    %most k steps
    %[dist,prev] = shortestpaths(E,s,k);
    
    [prev] = DijkstraShortestPaths(E, s);
    
    %trace the shortest path end at given ending pixel
    p = trace(prev,v);        
end

