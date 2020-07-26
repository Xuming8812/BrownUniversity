function [] = BoundaryDetection_Main(path,x1,y1,x2,y2);
    %Function :     BoundaryDetection_Main
    %Description:   Calculate the boundary from (x1,y1) to (x2,y2) by calculating
    %               the shortest path between those two pixels. Show the
    %               image and the boundary
    %Input:         path----Type: string; Meaning: the file name of the input image
    %               x1---Type:int; Meaning: the x coordinate of the
    %                       starting pixel
    %               y1---Type:int; Meaning: the y coordinate of the
    %                       starting pixel
    %               x2---Type:int; Meaning: the x coordinate of the
    %                       ending pixel
    %               y2---Type:int; Meaning: the y coordinate of the
    %                       ending pixel
    
    %import the image and stored it in a matrix
    I = imread(path);
    
    %calculate the boundary from starting pixel to ending pixel
    p = BoundaryDetection(I,x1,y1,x2,y2);
    
    %adding the boundary onto the original image
    I = DrawLines(I,p);
    
    %show the image with the boundary    
    imshow(I);

end

