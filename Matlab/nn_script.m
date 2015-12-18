close all; clc;

% sample input data
input_data = cell(1,1);
output_data = cell(1,1);

for pair = 1 : length(input_data)
    
    inputs = rand(13,12);
    outputs = rand(13,12);
    
    input_data{pair} = inputs;
    output_data{pair} = outputs;
    
end

network = create_neural_network(13,12,5);
network = train_neural_network(network, input_data, output_data, 50, 50);