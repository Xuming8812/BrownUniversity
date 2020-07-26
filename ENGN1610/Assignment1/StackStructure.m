classdef StackStructure < handle
    properties (Access = private)
        buffer      
        pos         
        capacity    
    end
   
    methods
        %constructor
        function obj = StackStructure()
            obj.buffer = cell(100, 1);
            obj.capacity = 100;
            obj.pos = 0;
        end
        %return the size of the stack
        function s = size(obj)
            s = obj.pos;
        end
        %return if the stack is empty     
        function b = isEmpty(obj)            
            b = ~logical(obj.pos);
        end
        %push element into stack
        function push(obj, el)
            if obj.pos >= obj.capacity
                obj.buffer(obj.capacity+1:2*obj.capacity) = cell(obj.capacity, 1);
                obj.capacity = 2*obj.capacity;
            end
            obj.pos = obj.pos + 1;
            obj.buffer{obj.pos} = el;
        end
        %pop the top element of the stack      
        function el = pop(obj)
            if obj.pos == 0
                el = [];
            else
                el = obj.buffer{obj.pos};
                obj.pos = obj.pos - 1;
            end        
        end        
    end
end

