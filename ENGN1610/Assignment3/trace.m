function coords = trace(prev,v)
    if prev(v) > 0
        coords = [trace(prev, prev(v));v];
    else
        coords = v;
    end
end