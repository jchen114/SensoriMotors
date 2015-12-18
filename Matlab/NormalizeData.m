function [normalized_value] = NormalizeData(min, max, value)
    normalized_value = (value - min)/(max - min);
end

